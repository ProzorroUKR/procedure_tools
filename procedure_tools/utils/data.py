from __future__ import absolute_import

ACCELERATION_DEFAULT = 460800
TENDER_SECONDS_BUFFER = 5

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


def get_id(response):
    return response.json()["data"]["id"]


def get_token(response):
    return response.json()["access"]["token"]


def get_next_check(response):
    return response.json()["data"]["next_check"]


def get_procurement_method_type(response):
    return response.json()["data"]["procurementMethodType"]


def get_submission_method_details(response):
    return response.json()["data"].get("submissionMethodDetails")


def get_data(response):
    return response.json().get("data", {})


def get_access(response):
    return response.json().get("access", {})


def get_config(response):
    return response.json().get("config", {})


def get_complaint_period_end_dates(response):
    return [item["complaintPeriod"]["endDate"] for item in response.json()["data"]]


def get_contract_period_clarif_date(response):
    return response.json()["data"]["contractPeriod"]["clarificationsUntil"]


def get_contracts_bids_ids(response):
    return [i["bidID"] for i in response.json()["data"]]


def get_items(response):
    return response.json()["data"]["items"]


def get_ids(response, status_exclude=None):
    if not status_exclude:
        status_exclude = []
    elif not isinstance(status_exclude, list):
        status_exclude = [status_exclude]
    return [
        item["id"]
        for item in response.json()["data"]
        if item["status"] not in status_exclude
    ]


def get_ids_with_status(response, status):
    return [item["id"] for item in response.json()["data"] if item["status"] == status]


def get_bid_ids(response):
    return [item["bid_id"] for item in response.json()["data"]]


def get_award_id(response):
    return response.json()["data"]["awardID"]


def get_contracts_bid_tokens(response, bids_ids, bids_tokens, contracts_award_ids):
    contracts_bid_tokens = []
    awards = response.json()["data"]
    for contracts_award_id in contracts_award_ids:
        for award in awards:
            if award["id"] == contracts_award_id:
                for bids_id, bids_token in zip(bids_ids, bids_tokens):
                    if bids_id == award["bid_id"]:
                        contracts_bid_tokens.append(bids_token)
                        break
                break
    return contracts_bid_tokens
