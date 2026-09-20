from typing import Any

import requests

ACCELERATION_DEFAULT = 460800
SECONDS_BUFFER = 5

EDR_FILENAME = "edr_identification.yaml"

WAIT_EDR_QUAL = "edr-qualification"
WAIT_EDR_PRE_QUAL = "edr-pre-qualification"
WAIT_EVENTS = (WAIT_EDR_QUAL, WAIT_EDR_PRE_QUAL)

SUBMISSION_QUICK = "quick"
SUBMISSION_QUICK_NO_AUCTION = "quick(mode:no-auction)"
SUBMISSION_QUICK_FAST_AUCTION = "quick(mode:fast-auction)"
SUBMISSION_QUICK_FAST_FORWARD = "quick(mode:fast-forward)"

SUBMISSIONS = [
    SUBMISSION_QUICK,
    SUBMISSION_QUICK_NO_AUCTION,
    SUBMISSION_QUICK_FAST_AUCTION,
    SUBMISSION_QUICK_FAST_FORWARD,
]


def get_id(response: requests.Response) -> str:
    value: str = response.json()["data"]["id"]
    return value


def get_token(response: requests.Response) -> str:
    value: str = response.json()["access"]["token"]
    return value


def get_next_check(response: requests.Response) -> str | None:
    value: str | None = response.json()["data"].get("next_check")
    return value


def get_procurement_method_type(response: requests.Response) -> str:
    value: str = response.json()["data"]["procurementMethodType"]
    return value


def get_procurement_method(response: requests.Response) -> str:
    value: str = response.json()["data"]["procurementMethod"]
    return value


def get_submission_method_details(response: requests.Response) -> str | None:
    value: str | None = response.json()["data"].get("submissionMethodDetails")
    return value


def get_data(response: requests.Response) -> dict[str, Any]:
    value: dict[str, Any] = response.json().get("data", {})
    return value


def get_access(response: requests.Response) -> dict[str, Any]:
    value: dict[str, Any] = response.json().get("access", {})
    return value


def get_config(response: requests.Response) -> dict[str, Any]:
    value: dict[str, Any] = response.json().get("config", {})
    return value


def get_complaint_period_end_dates(response: requests.Response) -> list[str]:
    return [item["complaintPeriod"]["endDate"] for item in response.json()["data"] if "complaintPeriod" in item]


def get_contract_period_clarif_date(response: requests.Response) -> str:
    value: str = response.json()["data"]["contractPeriod"]["clarificationsUntil"]
    return value


def get_contracts_bids_ids(response: requests.Response) -> list[str]:
    return [i["bidID"] for i in response.json()["data"]]


def get_items(response: requests.Response) -> list[dict[str, Any]]:
    value: list[dict[str, Any]] = response.json()["data"]["items"]
    return value


def get_ids(response: requests.Response, status_exclude: str | list[str] | None = None) -> list[str]:
    if not status_exclude:
        status_exclude = []
    elif not isinstance(status_exclude, list):
        status_exclude = [status_exclude]
    return [item["id"] for item in response.json()["data"] if item["status"] not in status_exclude]


def get_ids_with_status(response: requests.Response, status: str) -> list[str]:
    return [item["id"] for item in response.json()["data"] if item["status"] == status]


def get_bid_ids(response: requests.Response) -> list[str]:
    return [item["bid_id"] for item in response.json()["data"]]


def get_award_id(response: requests.Response) -> str:
    value: str = response.json()["data"]["awardID"]
    return value


def get_contracts_bid_tokens(
    response: requests.Response,
    bids_ids: list[str],
    bids_tokens: list[str],
    contracts_award_ids: list[str | None],
) -> list[str | None]:
    contracts_bid_tokens: list[str | None] = []
    awards = response.json()["data"]
    for contracts_award_id in contracts_award_ids:
        if contracts_award_id is None:
            contracts_bid_tokens.append(None)
            continue
        for award in awards:
            if award["id"] == contracts_award_id:
                for bids_id, bids_token in zip(bids_ids, bids_tokens):
                    if bids_id == award["bid_id"]:
                        contracts_bid_tokens.append(bids_token)
                        break
                break
    return contracts_bid_tokens
