"""
Offline run of the bundled data folders against a fake API: every step of every
folder is executed, so the action code paths, the templates and the context
hand-over between steps are exercised without a CDB instance.
"""

# fakes mirror the real client and action signatures
# pylint: disable=redefined-outer-name,unused-argument

import copy
import json
import re
from datetime import timedelta
from types import SimpleNamespace

import pytest

from procedure_tools import runner
from procedure_tools.actions import wait as wait_actions
from procedure_tools.runner import process_tools
from procedure_tools.utils.file import get_default_data_dirs

DATE = "2026-01-01T10:00:00+02:00"


def item(index, lot="lot"):
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


ORGANIZATION = {
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
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)
        self.headers = {}

    def json(self):
        return copy.deepcopy(self._payload)


class FakeDSClient:
    def __init__(self):
        self.uploads = []

    def post_document_upload(self, files):
        title = files["file"][0]
        self.uploads.append(title)
        return FakeResponse({"data": {"id": f"doc{len(self.uploads)}", "title": title, "url": "http://ds/doc"}})


class FakeCDBClient:
    """Answers every CDB endpoint used by the actions with plausible objects and records the calls."""

    client_timedelta = timedelta()

    def __init__(self):
        self.calls = []
        self.counter = 0
        self.tender = None
        self.bids = []
        self.awards = []
        self.contracts = {}
        self.changes = {}
        self.contracts_count = 12

    def new_id(self, prefix):
        self.counter += 1
        return f"{prefix}{self.counter}"

    def request(self, method, path, json=None, acc_token=None, auth_token=None, success_handler=None, **kwargs):
        self.calls.append((method, path))
        payload = self.respond(method, path, json or {})
        response = FakeResponse(payload)
        if success_handler:
            success_handler(response)
        return response

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, json=None, **kwargs):
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path, json=None, **kwargs):
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path, json=None, **kwargs):
        return self.request("PATCH", path, json=json, **kwargs)

    # --- objects

    def obj(self, prefix, body=None, path=None, **fields):
        """A plausible object; an existing object keeps the id taken from the last path segment."""
        object_id = path.rsplit("/", 1)[-1] if path else self.new_id(prefix)
        data = {"id": object_id, "status": "draft", "dateModified": DATE}
        data.update(fields)
        body_data = (body or {}).get("data", {})
        if isinstance(body_data, dict):
            data.update(body_data)
        return {"data": data, "access": {"token": f"{prefix}-token"}}

    def make_tender(self, body):
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

    def make_awards(self):
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

    def make_contract(self, contract_id):
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

    def respond(self, method, path, body):
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
        if re.fullmatch(r"tenders/[^/]+/(awards|qualifications)/[^/]+/complaints", path):
            return self.obj("complaint", body)
        if re.fullmatch(r"tenders/[^/]+/(awards|qualifications)/[^/]+/complaints/[^/]+", path):
            return self.obj("complaint", body, path=path)
        if re.fullmatch(r"tenders/[^/]+/complaints", path):
            return self.obj("complaint", body)
        if re.fullmatch(r"tenders/[^/]+/complaints/[^/]+", path):
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


def make_args(data_dir, **overrides):
    args = SimpleNamespace(
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
        debug=False,
        debug_request=False,
        debug_json_level=None,
    )
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


@pytest.fixture
def fake_api(monkeypatch):
    client, ds_client = FakeCDBClient(), FakeDSClient()
    monkeypatch.setattr(runner, "build_clients", lambda args, session=None: (client, ds_client))
    monkeypatch.setattr(wait_actions, "wait_until_date", lambda *args, **kwargs: None)
    monkeypatch.setattr(wait_actions, "wait_auction_participation_urls", lambda *args, **kwargs: None)
    monkeypatch.setattr(wait_actions, "sleep", lambda seconds: None)

    def wait_tender_status(client, args, context, tender_id, delay, status, fail_status=None):
        client.tender["status"] = status[0] if isinstance(status, list) else status
        return client.get(f"tenders/{tender_id}")

    monkeypatch.setattr(wait_actions, "wait_tender_status", wait_tender_status)
    return client, ds_client


@pytest.mark.parametrize("data_dir", sorted(get_default_data_dirs()))
def test_bundled_data_dirs_run_offline(fake_api, data_dir):
    client, ds_client = fake_api
    context = process_tools(make_args(data_dir))
    assert context.step.action == "tender_wait_status"
    assert context["tender"]["status"] == "complete"
    assert any(path.startswith("contracts") for _, path in client.calls)
    assert ds_client.uploads


def test_above_threshold_offline_flow(fake_api):
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
    # tender and award complaints were created and patched by roles
    assert len(context["tender_complaints"]) == 6
    assert len(context["award_complaints"][0]) == 6
    assert sum(1 for m, p in calls if m == "PATCH" and "/complaints/" in p) == 26
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


def test_reporting_offline_flow(fake_api):
    client, _ = fake_api
    context = process_tools(make_args("reporting"))
    calls = client.calls
    assert ("POST", f"tenders/{context['tender']['id']}/awards") in calls
    assert "tender_complaints" not in context
    assert ("PATCH", "contracts/contract0/credentials") in calls
    assert not any(p.endswith("signer_info") for _, p in calls)
    assert context["contracts"][0]["status"] == "terminated"


def test_ifi_offline_flow(fake_api):
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


def test_stop_after_step(fake_api):
    client, _ = fake_api
    with pytest.raises(SystemExit) as e:
        process_tools(make_args("reporting", stop="tender_patch.json"))
    assert e.value.code == 0
    assert client.calls[-1] == ("PATCH", f"tenders/{client.tender['id']}")


def test_complaints_skipped_without_role_tokens(fake_api):
    client, _ = fake_api
    context = process_tools(make_args("aboveThreshold", bot_token=None, reviewer_token=None))
    assert not any("/complaints" in p for _, p in client.calls)
    assert "tender_complaints" not in context
    assert context["tender"]["status"] == "complete"
