"""
Plan payloads.

A plan is what a tender is created from; it carries the budget and names the
procedure that will spend it.
"""

from __future__ import annotations

from typing import Any

from data.common import address_data, classification_data, item_data, organization_data
from data.utils import build, fake, from_now_iso


def budget_data(
    amount: float = 10000,
    amount_net: float = 12222,
    breakdown_amount: float = 1500,
    currency: str = "UAH",
    budget_id: str = "12303111000-2",
    **kwargs: Any,
) -> dict[str, Any]:
    return build(
        {
            "amount": amount,
            "amountNet": amount_net,
            "currency": currency,
            "description": fake.sentence(nb_words=10),
            "id": budget_id,
            "breakdown": [
                {
                    "description": fake.sentence(nb_words=10),
                    "title": "other",
                    "value": {"amount": breakdown_amount, "currency": currency},
                }
            ],
            "period": {"startDate": "2019-01-01T00:00:00", "endDate": "2019-12-31T00:00:00"},
            "project": {"id": "123", "name": fake.sentence(nb_words=5)},
        },
        **kwargs,
    )


def plan_organization_data(identifier_id: str = "21725150", **kwargs: Any) -> dict[str, Any]:
    """A buyer or procuring entity of a plan; unlike a tender, a plan takes no contact point."""
    organization = organization_data(identifier_id=identifier_id, address=address_data())
    organization.pop("contactPoint", None)
    return build(organization, **kwargs)


def plan_item_data(quantity: float = 1000, **kwargs: Any) -> dict[str, Any]:
    """An item of a plan: no delivery address, no lot and no English description."""
    item = item_data(quantity=quantity)
    for field in ("deliveryAddress", "additionalClassifications", "description_en"):
        item.pop(field, None)
    item["deliveryDate"] = {"endDate": "2019-10-16T01:00:00+03:00"}
    return build(item, **kwargs)


def plan_data(
    procurement_method_type: str = "aboveThreshold",
    procurement_method: str = "open",
    budget: dict[str, Any] | None = None,
    buyers: list[dict[str, Any]] | None = None,
    items: list[dict[str, Any]] | None = None,
    procuring_entity: dict[str, Any] | None = None,
    acceleration: float | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    A draft plan for ``procurement_method_type``.

    ``acceleration`` only shortens the dates of the plan, it is not a field of
    its own; the API rejects anything it does not know.
    """
    data: dict[str, Any] = {
        "budget": budget or budget_data(),
        "buyers": buyers or [plan_organization_data(identifier_id="111983")],
        "classification": classification_data(),
        "items": items if items is not None else [plan_item_data()],
        "mode": "test",
        "procuringEntity": procuring_entity or plan_organization_data(),
        "status": "draft",
        "tender": {
            "procurementMethod": procurement_method,
            "procurementMethodType": procurement_method_type,
            "tenderPeriod": {"startDate": from_now_iso(acceleration=acceleration)},
        },
    }
    return {"data": build(data, **kwargs)}


def reporting_plan_data(**kwargs: Any) -> dict[str, Any]:
    """A plan for a reporting procedure, which is a limited method."""
    return plan_data(procurement_method_type="reporting", procurement_method="limited", **kwargs)


def plan_patch_data(status: str = "scheduled", **kwargs: Any) -> dict[str, Any]:
    return {"data": build({"status": status}, **kwargs)}
