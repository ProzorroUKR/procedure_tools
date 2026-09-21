"""
Bid payloads.

A bid answers the tender it is submitted to, so the builders take the tender
itself and read the items and lots out of it instead of repeating them.
"""

from __future__ import annotations

from typing import Any

from data.common import tenderer_data, unit_data, value_data
from data.document import merge_contents
from data.utils import build, fake

# The document containers a bid can carry, in the order the API lists them.
DOCUMENT_CONTAINERS = (
    "documents",
    "eligibilityDocuments",
    "financialDocuments",
    "qualificationDocuments",
)


def bid_item_data(tender_item: dict[str, Any], amount: float = 100, **kwargs: Any) -> dict[str, Any]:
    """The bidder's price for one item of the tender."""
    return build(
        {
            "id": tender_item["id"],
            "description": tender_item.get("description"),
            "description_en": tender_item.get("description_en"),
            "quantity": tender_item.get("quantity", 1),
            "unit": unit_data(
                code=tender_item.get("unit", {}).get("code", "KGM"),
                name=tender_item.get("unit", {}).get("name", "кг"),
                value=value_data(amount=amount),
            ),
        },
        **kwargs,
    )


def item_unit_amount(
    item: dict[str, Any],
    tender: dict[str, Any],
    offered: dict[str, float],
    total: float | None,
) -> float:
    """
    The price the bidder puts on one unit of ``item``.

    The offer for the lot the item belongs to is spread over the quantities of
    that lot, so the item prices add up to roughly what was offered.
    """
    related_lot = item.get("relatedLot")
    if related_lot and related_lot in offered:
        items = [other for other in tender.get("items", []) if other.get("relatedLot") == related_lot]
        amount = offered[related_lot]
    else:
        items = list(tender.get("items", []))
        amount = total if total is not None else 0
    quantity = sum(other.get("quantity", 0) for other in items) or 1
    return round(amount / quantity, 2)


def lot_values_data(
    lots: list[dict[str, Any]],
    amounts: list[float] | None = None,
    with_subcontracting: bool = True,
) -> list[dict[str, Any]]:
    """
    One offer per lot.

    Without ``amounts`` each lot is offered at 80% of its own value, which
    keeps the bid under the ceiling whatever the lots are worth.
    """
    values: list[dict[str, Any]] = []
    for index, lot in enumerate(lots):
        if amounts and index < len(amounts):
            amount = amounts[index]
        else:
            amount = round(lot.get("value", {}).get("amount", 1000) * 0.8, 2)
        lot_value: dict[str, Any] = {
            "relatedLot": lot["id"],
            "value": {"amount": amount},
        }
        if with_subcontracting:
            lot_value["subcontractingDetails"] = f"{fake.company()}, Україна, м. Київ, {fake.street_address()}"
        values.append(lot_value)
    return values


def bid_data(
    tender: dict[str, Any],
    amount: float | None = None,
    amounts: list[float] | None = None,
    tenderers: list[dict[str, Any]] | None = None,
    documents: list[dict[str, Any]] | None = None,
    eligibility_documents: list[dict[str, Any]] | None = None,
    financial_documents: list[dict[str, Any]] | None = None,
    qualification_documents: list[dict[str, Any]] | None = None,
    parameters: list[dict[str, Any]] | None = None,
    lot_ids: list[str] | None = None,
    with_items: bool = True,
    identifier_id: str = "00137256",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    A draft bid for ``tender``.

    With lots the offer is split into ``lotValues``, one per lot; without lots
    it is a single ``value``, and ``lot_ids`` narrows the offer to the lots the
    bidder wants. The document arguments take document payloads,
    whose files the keyword that creates the bid uploads first.
    """
    lots = tender.get("lots") or []
    if lot_ids is not None:
        # a bidder need not want every lot
        wanted = set(lot_ids)
        lots = [lot for lot in lots if lot["id"] in wanted]
    data: dict[str, Any] = {
        "status": "draft",
        "tenderers": tenderers or [tenderer_data(identifier_id=identifier_id)],
        "subcontractingDetails": f"{fake.company()}, Україна, м. Київ, {fake.street_address()}",
    }
    if lots:
        data["lotValues"] = lot_values_data(lots, amounts=amounts if amounts is not None else None)
    else:
        tender_amount = tender.get("value", {}).get("amount", 1000)
        data["value"] = {"amount": amount if amount is not None else round(tender_amount * 0.8, 2)}
    if parameters:
        data["parameters"] = parameters
    if with_items and tender.get("items"):
        offered = {value["relatedLot"]: value["value"]["amount"] for value in data.get("lotValues", [])}
        total = data.get("value", {}).get("amount")
        # an item of a lot the bidder passed over has no price to give
        priced = [item for item in tender["items"] if not lot_ids or item.get("relatedLot") in offered]
        data["items"] = [bid_item_data(item, amount=item_unit_amount(item, tender, offered, total)) for item in priced]
    payload: dict[str, Any] = {}
    containers = dict(
        zip(
            DOCUMENT_CONTAINERS,
            (documents, eligibility_documents, financial_documents, qualification_documents),
        )
    )
    for container, container_documents in containers.items():
        if not container_documents:
            continue
        data[container] = [document["data"] for document in container_documents]
        merge_contents(payload, container_documents)
    payload["data"] = build(data, **kwargs)
    return payload


def bid_patch_data(status: str = "pending", **kwargs: Any) -> dict[str, Any]:
    return {"data": build({"status": status}, **kwargs)}
