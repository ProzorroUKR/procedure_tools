"""
Cross cutting checks over every payload a keyword can produce.

The API refuses an unknown field outright, and the arguments that steer a
builder (acceleration, the document content, the lots a criterion is spread
over) look exactly like fields. These tests watch that boundary, which is the
one that has actually leaked.
"""

import pytest
from data.award import award_data, award_patch_data, award_qualification_data
from data.bid import bid_data
from data.contract import contract_active_data, contract_signer_info_data
from data.criteria import criteria_data
from data.document import document_data
from data.plan import plan_data, reporting_plan_data
from data.tender import lots_data, reporting_tender_data, tender_data

# Names a builder takes as an argument and must never pass on to the API.
# "lots" is left out on purpose: it is an argument and a real tender field.
STEERING_ARGUMENTS = (
    "acceleration",
    "submission",
    "console",
    "amounts",
    "contents",
    "document_title",
    "with_items",
    "with_signer_info",
    "identifier_id",
    "related_lot",
    "related_item",
    "procurement_method_type",
    "duration_days",
    "item_amount",
)

CONTRACT = {
    "dateModified": "2026-01-10T12:00:00+02:00",
    "value": {"amount": 1000},
    "items": [{"id": "item-1", "quantity": 1, "unit": {"code": "KGM", "name": "кг"}}],
}


def payloads():
    tender = tender_data(lots=lots_data(1), acceleration=460800)
    created = tender["data"]
    for index, item in enumerate(created["items"]):
        item["id"] = f"item-{index}"
    return {
        "plan": plan_data(acceleration=460800),
        "reporting_plan": reporting_plan_data(acceleration=460800),
        "tender": tender,
        "reporting_tender": reporting_tender_data(acceleration=460800),
        "criteria": criteria_data(lots=created["lots"]),
        "bid": bid_data(created, documents=[document_data(title="a.txt")]),
        "award": award_data(),
        "award_qualification": award_qualification_data(),
        "award_patch": award_patch_data("active"),
        "contract_active": contract_active_data(CONTRACT),
        "signer_info": contract_signer_info_data(),
        "document": document_data(),
    }


def walk(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield f"{path}.{key}" if path else key
            yield from walk(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from walk(item, f"{path}.{index}")


@pytest.mark.parametrize("name", sorted(payloads()))
def test_no_builder_argument_leaks_into_the_request(name):
    payload = payloads()[name]
    # "contents" rides alongside and is stripped before sending, so only the
    # part that is actually sent is checked
    sent = payload.get("data")
    assert sent is not None, f"{name} sends no data"
    leaked = [field for field in walk(sent) if field.split(".")[-1] in STEERING_ARGUMENTS]
    assert not leaked, f"{name} would send {leaked}"


@pytest.mark.parametrize("name", sorted(payloads()))
def test_every_payload_is_wrapped_in_data(name):
    payload = payloads()[name]
    assert set(payload) <= {"data", "config", "contents"}, f"{name} has an unexpected top level key"


@pytest.mark.parametrize("name", sorted(payloads()))
def test_every_payload_is_json(name):
    import json

    json.dumps(payloads()[name], ensure_ascii=False)
