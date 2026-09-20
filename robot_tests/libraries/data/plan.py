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


def plan_data(
    procurement_method_type: str = "aboveThreshold",
    procurement_method: str = "open",
    budget: dict[str, Any] | None = None,
    buyers: list[dict[str, Any]] | None = None,
    items: list[dict[str, Any]] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """A draft plan for ``procurement_method_type``."""
    item = item_data(quantity=1000)
    # a plan item carries no delivery address and no lot
    item.pop("deliveryAddress", None)
    item.pop("additionalClassifications", None)
    item.pop("description_en", None)
    item["deliveryDate"] = {"endDate": "2019-10-16T01:00:00+03:00"}
    data: dict[str, Any] = {
        "budget": budget or budget_data(),
        "buyers": buyers or [organization_data(identifier_id="111983", address=address_data())],
        "classification": classification_data(),
        "items": items if items is not None else [item],
        "mode": "test",
        "procuringEntity": organization_data(),
        "status": "draft",
        "tender": {
            "procurementMethod": procurement_method,
            "procurementMethodType": procurement_method_type,
            "tenderPeriod": {"startDate": from_now_iso()},
        },
    }
    return {"data": build(data, **kwargs)}


def reporting_plan_data(**kwargs: Any) -> dict[str, Any]:
    """A plan for a reporting procedure, which is a limited method."""
    return plan_data(procurement_method_type="reporting", procurement_method="limited", **kwargs)


def plan_patch_data(status: str = "scheduled", **kwargs: Any) -> dict[str, Any]:
    return {"data": build({"status": status}, **kwargs)}
