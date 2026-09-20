"""
Offline run of the bundled data folders against a fake API: every step of every
folder is executed, so the action code paths, the templates and the context
hand-over between steps are exercised without a CDB instance.
"""

# fakes mirror the real client and action signatures
# pylint: disable=redefined-outer-name,unused-argument

import argparse
import copy
import json
import re
from collections.abc import Callable
from datetime import timedelta
from typing import Any

import pytest

from procedure_tools import runner
from procedure_tools.actions import wait as wait_actions
from procedure_tools.context import Context
from procedure_tools.runner import process_tools
from procedure_tools.utils.file import get_default_data_dirs

DATE = "2026-01-01T10:00:00+02:00"


def item(index: int, lot: str = "lot") -> dict[str, Any]:
    return {
        "id": f"item{index}",
        "description": f"item {index}",
        "description_en": f"item {index} en",
        "additionalClassifications": [{"description": "add", "id": "28.23.23", "scheme": "ДКПП"}] * 2,
        "classification": {"description": "cls", "id": "42000000-6", "scheme": "ДК021"},
        "deliveryAddress": {
            "countryName": "Україна",
            "locality": "м. Київ",
            "postalCode": "79000",
            "region": "м. Київ",
            "streetAddress": "street",
        },
        "deliveryDate": {"startDate": DATE, "endDate": DATE},
        "relatedLot": lot,
        "unit": {
            "code": "KGM",
            "name": "кг",
            "value": {"amount": 1, "currency": "UAH", "valueAddedTaxIncluded": False},
        },
        "relatedBuyer": "buyer1",
    }


ORGANIZATION: dict[str, Any] = {
    "name": "org",
    "name_en": "org en",
    "kind": "general",
    "scale": "micro",
    "contract_owner": "broker",
    "address": {
        "countryName": "Україна",
        "locality": "м. Київ",
        "postalCode": "01220",
        "region": "м. Київ",
        "streetAddress": "street",
    },
    "identifier": {"id": "1", "scheme": "UA-EDR", "legalName": "legal", "legalName_en": "legal en", "uri": "http://x"},
    "signerInfo": {
        "authorizedBy": "statute",
        "email": "a@b.c",
        "iban": "1",
        "name": "signer",
        "position": "director",
        "telephone": "+380000000000",
    },
}


class FakeResponse:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)
        self.headers: dict[str, str] = {}

    def json(self) -> dict[str, Any]:
        return copy.deepcopy(self._payload)


class FakeDSClient:
    def __init__(self) -> None:
        self.uploads: list[str] = []

    def post_document_upload(self, files: dict[str, Any]) -> FakeResponse:
        title = files["file"][0]
        self.uploads.append(title)
        return FakeResponse({"data": {"id": f"doc{len(self.uploads)}", "title": title, "url": "http://ds/doc"}})


class FakeCDBClient:
    """Answers every CDB endpoint used by the actions with plausible objects and records the calls."""

    client_timedelta = timedelta()

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.counter = 0
        self.tender: dict[str, Any] | None = None
        self.bids: list[str] = []
        self.awards: list[dict[str, Any]] = []
        self.complaints: dict[str, list[dict[str, Any]]] = {}
        self.questions: dict[str, dict[str, Any]] = {}
        self.contracts: dict[str, dict[str, Any]] = {}
        self.changes: dict[str, list[dict[str, Any]]] = {}
        self.contracts_count = 12

    def new_id(self, prefix: str) -> str:
        self.counter += 1
        return f"{prefix}{self.counter}"

    def request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        acc_token: str | None = None,
        auth_token: str | None = None,
        success_handler: Callable[[FakeResponse], None] | None = None,
        **kwargs: Any,
    ) -> FakeResponse:
        self.calls.append((method, path))
        payload = self.respond(method, path, json or {})
        response = FakeResponse(payload)
        if success_handler:
            success_handler(response)
        return response

    def get(self, path: str, **kwargs: Any) -> FakeResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, json: dict[str, Any] | None = None, **kwargs: Any) -> FakeResponse:
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: dict[str, Any] | None = None, **kwargs: Any) -> FakeResponse:
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: dict[str, Any] | None = None, **kwargs: Any) -> FakeResponse:
        return self.request("PATCH", path, json=json, **kwargs)

    # --- objects

    def obj(
        self, prefix: str, body: dict[str, Any] | None = None, path: str | None = None, **fields: Any
    ) -> dict[str, Any]:
        """A plausible object; an existing object keeps the id taken from the last path segment."""
        object_id = path.rsplit("/", 1)[-1] if path else self.new_id(prefix)
        data = {"id": object_id, "status": "draft", "dateModified": DATE}
        data.update(fields)
        body_data = (body or {}).get("data", {})
        if isinstance(body_data, dict):
            data.update(body_data)
        return {"data": data, "access": {"token": f"{prefix}-token"}}

    def make_tender(self, body: dict[str, Any]) -> dict[str, Any]:
        payload = self.obj(
            "tender",
            body,
            items=[item(i) for i in range(8)],
            next_check=DATE,
            stage2TenderID="stage2",
            agreements=[{"id": "agreement1"}],
            contractPeriod={"clarificationsUntil": DATE},
        )
        payload["config"] = body.get("config", {})
        self.tender = payload["data"]
        return payload

    def make_awards(self) -> list[dict[str, Any]]:
        if not self.awards:
            bids = self.bids or ["bid-none"]
            self.awards = [
                {
                    "id": f"award{i}",
                    "status": "pending",
                    "bid_id": bids[i % len(bids)],
                    "complaintPeriod": {"endDate": DATE},
                }
                for i in range(12)
            ]
        return self.awards

    def make_contract(self, contract_id: str) -> dict[str, Any]:
        if contract_id not in self.contracts:
            index = int(contract_id[len("contract") :])
            award = self.make_awards()[[0, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11][index % 12]]
            self.contracts[contract_id] = {
                "id": contract_id,
                "status": "pending",
                "awardID": award["id"],
                "dateModified": DATE,
                "items": [item(i) for i in range(8)],
                "buyer": copy.deepcopy(ORGANIZATION),
                "suppliers": [copy.deepcopy(ORGANIZATION), copy.deepcopy(ORGANIZATION)],
                "contractTemplateName": "template",
                "tender_id": self.tender["id"] if self.tender else "tender",
                "changes": self.changes.setdefault(contract_id, []),
            }
        return {"data": self.contracts[contract_id]}

    def respond(self, method: str, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if path == "constants":
            return {"SIGNATURE_VERIFICATION_ENABLED": False}
        if path == "plans":
            return self.obj("plan", body)
        if re.fullmatch(r"plans/[^/]+", path):
            return self.obj("plan", body)
        if path == "tenders" or re.fullmatch(r"plans/[^/]+/tenders", path):
            return self.make_tender(body)
        if path == "frameworks":
            return self.obj("framework", body, agreementID="agreement1")
        if re.fullmatch(r"frameworks/[^/]+", path):
            return self.obj("framework", body, path=path, agreementID="agreement1")
        if path == "submissions":
            return self.obj("submission", body)
        if re.fullmatch(r"submissions/[^/]+", path):
            return self.obj("submission", body, path=path, qualificationID=self.new_id("fq"))
        if re.fullmatch(r"qualifications/[^/]+", path):
            return self.obj("fq", body, path=path)
        if re.fullmatch(r"qualifications/[^/]+/documents", path):
            return self.obj("doc", body)
        if re.fullmatch(r"agreements/[^/]+", path):
            return self.obj("agreement", body, path=path, items=[item(i) for i in range(8)])
        if re.fullmatch(r"tenders/[^/]+", path):
            assert self.tender is not None, "tender was not created"
            self.tender.update(body.get("data", {}))
            return {"data": self.tender, "config": {"hasAuction": True}}
        if re.fullmatch(r"tenders/[^/]+/credentials", path):
            return self.make_tender({})
        if re.fullmatch(r"tenders/[^/]+/agreements", path):
            return {"data": [{"id": "agreement1", "status": "pending"}]}
        if re.fullmatch(r"tenders/[^/]+/agreements/[^/]+", path):
            return self.obj("agreement", body, path=path)
        if re.fullmatch(r"tenders/[^/]+/agreements/[^/]+/documents", path):
            return self.obj("doc", body)
        if re.fullmatch(r"tenders/[^/]+/agreements/[^/]+/contracts", path):
            return {
                "data": [
                    {"id": f"acontract{i}", "bidID": bid_id, "status": "active"} for i, bid_id in enumerate(self.bids)
                ]
            }
        if re.fullmatch(r"tenders/[^/]+/agreements/[^/]+/contracts/[^/]+", path):
            return self.obj("acontract", body, path=path)
        if re.fullmatch(r"tenders/[^/]+/documents(/[^/]+)?", path):
            return self.obj("doc", body)
        if re.fullmatch(r"tenders/[^/]+/criteria", path):
            return {"data": [{"id": "criterion1", "classification": {"id": "CRITERION.OTHER"}}]}
        if re.fullmatch(r"tenders/[^/]+/plans", path):
            return {"data": [{"id": body["data"]["id"]}]}
        if re.fullmatch(r"tenders/[^/]+/bids", path):
            if method == "POST":
                payload = self.obj("bid", body)
                self.bids.append(payload["data"]["id"])
                return payload
            return {"data": [{"id": bid_id, "status": "active"} for bid_id in self.bids]}
        if re.fullmatch(r"tenders/[^/]+/bids/[^/]+", path):
            return self.obj("bid", body, path=path, documents=[{"id": "doc1", "title": "bid_document_file.txt"}])
        if re.fullmatch(r"tenders/[^/]+/bids/[^/]+/(documents|requirement_responses)", path):
            return self.obj("doc", body)
        if re.fullmatch(r"tenders/[^/]+/awards", path):
            if method == "POST":
                self.make_awards()
                return self.obj("award", body)
            return {"data": self.make_awards()}
        if re.fullmatch(r"tenders/[^/]+/awards/[^/]+", path):
            return self.obj("award", body, path=path)
        if re.fullmatch(r"tenders/[^/]+/awards/[^/]+/documents", path):
            return self.obj("doc", body)
        if re.fullmatch(r"tenders/[^/]+/qualifications", path):
            return {"data": [{"id": f"qualification{i}", "status": "pending"} for i in range(8)]}
        if re.fullmatch(r"tenders/[^/]+/qualifications/[^/]+", path):
            return self.obj("qualification", body, path=path)
        if re.fullmatch(r"tenders/[^/]+/questions", path):
            payload = self.obj("question", body)
            self.questions[payload["data"]["id"]] = payload["data"]
            return payload
        if re.fullmatch(r"tenders/[^/]+/questions/[^/]+", path):
            question = self.questions.setdefault(path.rsplit("/", 1)[-1], self.obj("question", path=path)["data"])
            question.update(body.get("data", {}))
            return {"data": question}
        if re.fullmatch(r"tenders/[^/]+/((awards|qualifications)/[^/]+/)?complaints/[^/]+/posts", path):
            collection, _, complaint_id = path.rsplit("/", 1)[0].rpartition("/")
            post = self.obj("post", body)["data"]
            for complaint in self.complaints.get(collection, []):
                if complaint["id"] == complaint_id:
                    complaint.setdefault("posts", []).append(post)
            return {"data": post}
        if re.fullmatch(r"tenders/[^/]+/((awards|qualifications)/[^/]+/)?complaints", path):
            if method == "GET":
                return {"data": self.complaints.get(path, [])}
            payload = self.obj("complaint", body)
            self.complaints.setdefault(path, []).append(payload["data"])
            return payload
        if re.fullmatch(r"tenders/[^/]+/((awards|qualifications)/[^/]+/)?complaints/[^/]+", path):
            collection, _, complaint_id = path.rpartition("/")
            for complaint in self.complaints.get(collection, []):
                if complaint["id"] == complaint_id:
                    complaint.update(body.get("data", {}))
                    return {"data": complaint}
            return self.obj("complaint", body, path=path)
        if path == "contracts":
            self.contracts_count += 1
            return self.make_contract(f"contract{self.contracts_count - 1}")
        if re.fullmatch(r"tenders/[^/]+/contracts", path):
            return {"data": [{"id": f"contract{i}", "status": "pending"} for i in range(self.contracts_count)]}
        if re.fullmatch(r"contracts/[^/]+", path):
            contract_id = path.split("/")[1]
            self.make_contract(contract_id)["data"].update(body.get("data", {}))
            return self.make_contract(contract_id)
        if re.fullmatch(r"contracts/[^/]+/credentials", path):
            contract_id = path.split("/")[1]
            return {"data": self.make_contract(contract_id)["data"], "access": {"token": f"{contract_id}-token"}}
        if re.fullmatch(r"contracts/[^/]+/access", path):
            return {"data": body["data"], "access": {"token": "access-token"}}
        if re.fullmatch(r"contracts/[^/]+/(buyer|suppliers)/signer_info", path):
            return {"data": body["data"]}
        if re.fullmatch(r"contracts/[^/]+/changes", path):
            contract_id = path.split("/")[1]
            change = self.obj("change", body)["data"]
            self.changes.setdefault(contract_id, []).append(change)
            return {"data": change}
        if re.fullmatch(r"contracts/[^/]+/changes/[^/]+", path):
            return self.obj("change", body, path=path)
        if re.fullmatch(r"contracts/[^/]+/(documents|signatories|cancellations)", path):
            return self.obj("doc", body)
        if re.fullmatch(r"contracts/[^/]+/changes/[^/]+/(documents|signatories|cancellations)", path):
            return self.obj("doc", body)
        raise AssertionError(f"unexpected request {method} {path}")


def make_args(data_dir: str, **overrides: Any) -> argparse.Namespace:
    args = argparse.Namespace(
        host="http://cdb",
        token="token",
        path="/api/0/",
        ds_host="http://ds",
        ds_username="u",
        ds_password="p",
        acceleration=100,
        submission="quick(mode:no-auction)",
        data=data_dir,
        stop=None,
        pause=None,
        wait=[],
        reviewer_token="reviewer",
        bot_token="bot",
        disable_complaints=False,
        disable_claims=False,
        disable_questions=False,
        debug=False,
        debug_request=False,
        debug_json_level=None,
    )
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


@pytest.fixture
def fake_api(monkeypatch: pytest.MonkeyPatch) -> tuple[FakeCDBClient, FakeDSClient]:
    client, ds_client = FakeCDBClient(), FakeDSClient()
    monkeypatch.setattr(runner, "build_clients", lambda args, session=None: (client, ds_client))
    monkeypatch.setattr(wait_actions, "wait_until_date", lambda *args, **kwargs: None)
    monkeypatch.setattr(wait_actions, "wait_auction_participation_urls", lambda *args, **kwargs: None)
    monkeypatch.setattr(wait_actions, "sleep", lambda seconds: None)

    def wait_tender_status(
        client: FakeCDBClient,
        args: argparse.Namespace,
        context: Context,
        tender_id: str,
        delay: float,
        status: str | list[str],
        fail_status: str | list[str] | None = None,
    ) -> FakeResponse:
        assert client.tender is not None, "tender was not created"
        client.tender["status"] = status[0] if isinstance(status, list) else status
        return client.get(f"tenders/{tender_id}")

    monkeypatch.setattr(wait_actions, "wait_tender_status", wait_tender_status)
    return client, ds_client


@pytest.mark.parametrize("data_dir", sorted(get_default_data_dirs()))
def test_bundled_data_dirs_run_offline(fake_api: tuple[FakeCDBClient, FakeDSClient], data_dir: str) -> None:
    client, ds_client = fake_api
    context = process_tools(make_args(data_dir))
    assert context.step is not None
    assert context.step.action == "tender_wait_status"
    assert context["tender"]["status"] == "complete"
    assert any(path.startswith("contracts") for _, path in client.calls)
    assert ds_client.uploads


def test_above_threshold_offline_flow(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, ds_client = fake_api
    context = process_tools(make_args("aboveThreshold"))
    calls = client.calls
    # plan then tender under the plan
    assert ("POST", "plans") in calls
    assert ("POST", f"plans/{context['plan']['id']}/tenders") in calls
    # documents, criteria and bids
    assert ds_client.uploads[:3] == [
        "tender_document_file.txt",
        "tender_document_contract_proforma.txt",
        "tender_document_notice.p7s",
    ]
    assert len(context["bids"]) == 2 and len(context["bids_tokens"]) == 2
    # tender and award complaints were created and patched by roles; claims were added on awards 0, 1 and 2
    assert len(context["tender_complaints"]) == 6
    assert len(context["award_complaints"][0]) == 6
    assert sum(1 for m, p in calls if m == "PATCH" and "/complaints/" in p) == 33
    assert [len(context["award_claims"][index]) for index in (0, 1, 2)] == [2, 1, 1]
    award0_claims = context["award_claims"][0]
    assert [claim["type"] for claim in award0_claims] == ["claim", "claim"]
    assert [claim["status"] for claim in award0_claims] == ["resolved", "cancelled"]
    assert context["award_claims"][1][0]["status"] == "answered"
    assert context["award_claims"][2][0]["status"] == "answered"
    assert context["award_claims"][2][0]["satisfied"] is False
    # the claims of the cancelled award 1 and the unsuccessful award 2 are listed after their last patch
    for award_id in ("award1", "award2"):
        assert ("GET", f"tenders/{context['tender']['id']}/awards/{award_id}/complaints") in calls
    # award complaints follow the last step of award 0 and precede the award 1 steps
    award_paths = [p for m, p in calls if m == "PATCH" and re.fullmatch(r"tenders/[^/]+/awards/award[01]$", p)]
    complaint_index = next(i for i, (m, p) in enumerate(calls) if "/awards/award0/complaints" in p)
    award1_index = next(i for i, (m, p) in enumerate(calls) if p.endswith("/awards/award1") and m == "PATCH")
    assert award_paths and complaint_index < award1_index
    # legacy contract flow: credentials, signer info, patches and a change on contracts 0 and 2
    assert context["contracts_tokens"][0] == "contract0-token"
    assert context["contracts_tokens"][2] == "contract2-token"
    assert ("PUT", "contracts/contract0/buyer/signer_info") in calls
    assert ("PUT", "contracts/contract2/suppliers/signer_info") in calls
    assert ("POST", "contracts/contract0/changes") in calls
    assert (
        "PATCH",
        "contracts/contract0/changes/change" + str(context["contracts"][0]["changes"][0]["id"][6:]),
    ) in calls
    assert context["contracts"][0]["status"] == "terminated"


def test_below_threshold_offline_claims(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("belowThreshold", bot_token=None, reviewer_token=None))
    calls = client.calls
    # claims need no bot or reviewer token: two on award 0, two on award 1, one on award 2
    assert "award_complaints" not in context
    assert [len(context["award_claims"][index]) for index in (0, 1, 2)] == [2, 2, 1]
    assert all(claim["type"] == "claim" for claims in context["award_claims"].values() for claim in claims)
    assert context["award_claims"][0][0]["status"] == "resolved"
    assert context["award_claims"][0][1]["status"] == "cancelled"
    assert context["award_claims"][2][0]["satisfied"] is False
    # the claims of award 1 are listed again after the award is cancelled
    cancel_index = next(i for i, (m, p) in enumerate(calls) if m == "PATCH" and p.endswith("/awards/award1"))
    get_index = next(i for i, (m, p) in enumerate(calls) if m == "GET" and p.endswith("/awards/award1/complaints"))
    assert cancel_index < get_index


def test_above_threshold_eu_offline_claims(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("aboveThresholdEU", bot_token=None, reviewer_token=None))
    calls = client.calls
    # qualification claims: one on an active qualification, one on the unsuccessful one
    assert context["qualification_claims"][1][0]["status"] == "resolved"
    assert context["qualification_claims"][5][0]["satisfied"] is False
    # award claims: two on award 3, one each on award 1 (cancelled later) and award 2 (unsuccessful)
    assert [len(context["award_claims"][index]) for index in (1, 2, 3)] == [1, 1, 2]
    assert context["award_claims"][3][0]["status"] == "resolved"
    assert context["award_claims"][3][1]["status"] == "cancelled"
    assert context["award_claims"][1][0]["status"] == "answered"
    cancel_index = next(i for i, (m, p) in enumerate(calls) if m == "PATCH" and p.endswith("/awards/award1"))
    get_index = next(i for i, (m, p) in enumerate(calls) if m == "GET" and p.endswith("/awards/award1/complaints"))
    assert cancel_index < get_index


def test_close_framework_agreement_offline_claims(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    process_tools(make_args("closeFrameworkAgreementUA", bot_token=None, reviewer_token=None))
    # the context is cleared before the selection stage, so check what the fake API stored
    stored = {path.split("/", 2)[-1]: claims for path, claims in client.complaints.items()}
    # qualification claims on qualification 1 in the pre-qualification stand-still
    qualification_claims = stored["qualifications/qualification1/complaints"]
    assert [claim["status"] for claim in qualification_claims] == ["resolved", "answered"]
    assert qualification_claims[1]["satisfied"] is False
    # award claims on awards 1 and 2 in the awarding stand-still
    assert [claim["status"] for claim in stored["awards/award1/complaints"]] == ["resolved", "cancelled"]
    assert [claim["status"] for claim in stored["awards/award2/complaints"]] == ["answered"]
    claim_collections = (
        "qualifications/qualification1/complaints",
        "awards/award1/complaints",
        "awards/award2/complaints",
    )
    assert all(claim["type"] == "claim" for key in claim_collections for claim in stored[key])
    assert any(m == "GET" and p.endswith("qualifications/qualification1/complaints") for m, p in client.calls)
    assert any(m == "GET" and p.endswith("awards/award2/complaints") for m, p in client.calls)


@pytest.mark.parametrize("data_dir", ["competitiveDialogueEU", "competitiveDialogueUA"])
def test_competitive_dialogue_offline_claims(fake_api: tuple[FakeCDBClient, FakeDSClient], data_dir: str) -> None:
    client, _ = fake_api
    context = process_tools(make_args(data_dir, bot_token=None, reviewer_token=None))
    calls = client.calls
    # stage 2 award claims: award 1 (cancelled later), award 2 (unsuccessful), award 3 (active)
    assert [len(context["award_claims"][index]) for index in (1, 2, 3)] == [1, 1, 2]
    assert context["award_claims"][1][0]["status"] == "answered"
    assert context["award_claims"][2][0]["satisfied"] is False
    assert [claim["status"] for claim in context["award_claims"][3]] == ["resolved", "cancelled"]
    cancel_index = next(i for i, (m, p) in enumerate(calls) if m == "PATCH" and p.endswith("/awards/award1"))
    get_index = next(i for i, (m, p) in enumerate(calls) if m == "GET" and p.endswith("/awards/award1/complaints"))
    assert cancel_index < get_index
    # qualification claims: stage 1 in both procedures, stage 2 only in EU (the context is reset between stages)
    qualification_claims = {
        path: [claim for claim in complaints if claim.get("type") == "claim"]
        for path, complaints in client.complaints.items()
        if "/qualifications/" in path
    }
    qualification_claims = {path: claims for path, claims in qualification_claims.items() if claims}
    assert len(qualification_claims) == (3 if data_dir == "competitiveDialogueEU" else 2)
    statuses = [claim["status"] for claims in qualification_claims.values() for claim in claims]
    assert "resolved" in statuses and "answered" in statuses


@pytest.mark.parametrize("data_dir", ["negotiation", "negotiation.quick", "negotiation.local"])
def test_negotiation_offline_complaints(fake_api: tuple[FakeCDBClient, FakeDSClient], data_dir: str) -> None:
    client, _ = fake_api
    context = process_tools(make_args(data_dir))
    # award complaints are filed by the broker: negotiation has no bids, so no bid token is involved
    assert "tender_complaints" not in context and "bids_tokens" not in context
    award_complaints = context["award_complaints"][0]
    assert [complaint["type"] for complaint in award_complaints] == ["complaint"] * 6
    assert [complaint["status"] for complaint in award_complaints[:5]] == [
        "resolved",
        "stopped",
        "declined",
        "invalid",
        "mistaken",
    ]
    award_id = context["awards"][0]["id"]
    assert ("POST", f"tenders/{context['tender']['id']}/awards/{award_id}/complaints") in client.calls


def test_competitive_ordering_long_offline_complaints(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    _, _ = fake_api
    context = process_tools(make_args("dynamicPurchasingSystem.competitiveOrdering.long"))
    assert [complaint["type"] for complaint in context["tender_complaints"]] == ["complaint"] * 6
    assert [complaint["type"] for complaint in context["award_complaints"][0]] == ["complaint"] * 6
    assert [claim["status"] for claim in context["award_claims"][0]] == ["resolved", "cancelled"]


def test_disable_complaints_and_claims(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("aboveThreshold", disable_complaints=True))
    assert "tender_complaints" not in context and "award_complaints" not in context
    assert [claim["status"] for claim in context["award_claims"][0]] == ["resolved", "cancelled"]
    posted = [p for m, p in client.calls if m == "POST" and p.endswith("/complaints")]
    assert posted and all("/awards/" in p for p in posted)  # only the award claims were posted
    assert context["tender"]["status"] == "complete"


def test_disable_claims(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("belowThreshold", disable_claims=True))
    assert "award_claims" not in context
    assert not any("/complaints" in p for _, p in client.calls)
    assert context["tender"]["status"] == "complete"


def test_questions_and_complaint_posts(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("aboveThreshold"))
    tender_path = f"tenders/{context['tender']['id']}"
    # two questions asked by the broker and answered by the tender owner, before the complaints
    assert [question["questionOf"] for question in context["questions"]] == ["tender", "item"]
    assert all(question["answer"] for question in context["questions"])
    question_index = client.calls.index(("POST", f"{tender_path}/questions"))
    complaint_index = client.calls.index(("POST", f"{tender_path}/complaints"))
    assert question_index < complaint_index
    # every complaint carries an objection; complaint 0 got two reviewer threads with replies while pending
    assert all(complaint["objections"] for complaint in context["tender_complaints"])
    posts = context["tender_complaints"][0]["posts"]
    assert [post["recipient"] for post in posts] == [
        "complaint_owner",
        "aboveThresholdReviewers",
        "tender_owner",
        "aboveThresholdReviewers",
    ]
    assert [bool(post.get("relatedPost")) for post in posts] == [False, True, False, True]
    assert "posts" not in context["tender_complaints"][1]


def test_disable_questions(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("aboveThreshold", disable_questions=True))
    assert "questions" not in context
    assert not any("/questions" in p for _, p in client.calls)
    assert context["tender"]["status"] == "complete"


def test_reporting_offline_flow(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("reporting"))
    calls = client.calls
    assert ("POST", f"tenders/{context['tender']['id']}/awards") in calls
    assert "tender_complaints" not in context
    assert ("PATCH", "contracts/contract0/credentials") in calls
    assert not any(p.endswith("signer_info") for _, p in calls)
    assert context["contracts"][0]["status"] == "terminated"


def test_ifi_offline_flow(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, ds_client = fake_api
    context = process_tools(make_args("internationalFinancialInstitutions.requestForProposal"))
    calls = client.calls
    assert ("POST", "frameworks") in calls
    assert len(context["submissions"]) == 3
    assert len(context["framework_qualifications"]) == 3
    assert context["agreement"]["id"] == "agreement1"
    # the tender is created without a plan and references the agreement
    tender_create = next(i for i, (m, p) in enumerate(calls) if (m, p) == ("POST", "tenders"))
    assert tender_create > calls.index(("GET", "agreements/agreement1"))
    assert ds_client.uploads[:3] == [f"framework_qualification_{i}_document_evaluation_report.p7s" for i in range(3)]
    assert ("PATCH", "contracts/contract2/credentials") in calls


def test_stop_after_step(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    with pytest.raises(SystemExit) as e:
        process_tools(make_args("reporting", stop="tender_patch.json"))
    assert e.value.code == 0
    assert client.tender is not None
    assert client.calls[-1] == ("PATCH", f"tenders/{client.tender['id']}")


def test_complaints_skipped_without_role_tokens(fake_api: tuple[FakeCDBClient, FakeDSClient]) -> None:
    client, _ = fake_api
    context = process_tools(make_args("aboveThreshold", bot_token=None, reviewer_token=None))
    # complaints whose patch steps need the bot or reviewer are skipped, one by one
    tender_complaints = context["tender_complaints"]
    assert [complaint is None for complaint in tender_complaints] == [True, True, True, True, False, False]
    assert all(complaint["type"] == "complaint" for complaint in tender_complaints if complaint is not None)
    tender_complaint_patches = [
        p for m, p in client.calls if m == "PATCH" and re.fullmatch(r"tenders/[^/]+/complaints/[^/]+", p)
    ]
    assert len(tender_complaint_patches) == 1  # complaint 4 set to mistaken by the complainer
    # claims only involve the tenderer and the complainer, so they run
    award_complaints = context["award_complaints"][0]
    assert [complaint is None for complaint in award_complaints] == [True] * 4 + [False] * 2
    award_claims = context["award_claims"][0]
    assert [claim["type"] for claim in award_claims] == ["claim", "claim"]
    assert [claim["status"] for claim in award_claims] == ["resolved", "cancelled"]
    assert context["tender"]["status"] == "complete"
