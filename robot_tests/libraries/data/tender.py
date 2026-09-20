"""
Tender payloads.

``tender_data`` composes the pieces from ``common``: a procuring entity, items,
lots and milestones. Anything it builds can be replaced by passing it in, so a
test that cares about one aspect only describes that aspect::

    ${lots}=      Lots Data      2
    ${tender}=    Tender Data    lots=${lots}    value.amount=5000
"""

from __future__ import annotations

from typing import Any

from data.common import (
    item_data,
    lot_data,
    milestone_data,
    payment_milestones_data,
    procuring_entity_data,
    value_data,
)
from data.utils import build, fake, fake_en, from_now_iso

# Config of an above threshold open procedure: auction, complaints, no prequalification.
ABOVE_THRESHOLD_CONFIG: dict[str, Any] = {
    "awardComplainDuration": 5,
    "cancellationComplainDuration": 10,
    "clarificationUntilDuration": 3,
    "enquiryPeriodRegulation": 3,
    "hasAuction": True,
    "hasAwardComplaints": True,
    "hasAwardingOrder": True,
    "hasCancellationComplaints": True,
    "hasEnquiries": False,
    "hasMultiSourcing": False,
    "hasPreSelectionAgreement": False,
    "hasPrequalification": False,
    "hasQualificationComplaints": False,
    "hasTenderComplaints": True,
    "hasValueEstimation": True,
    "hasValueRestriction": False,
    "minBidsNumber": 1,
    "minEnquiriesDuration": 0,
    "minTenderingDuration": 15,
    "qualificationComplainDuration": 0,
    "qualificationDuration": 0,
    "restricted": False,
    "tenderComplainRegulation": 3,
    "valueCurrencyEquality": True,
}

# Config of a reporting procedure: no auction, no bids, no complaints.
REPORTING_CONFIG: dict[str, Any] = {
    **ABOVE_THRESHOLD_CONFIG,
    "awardComplainDuration": 0,
    "cancellationComplainDuration": 0,
    "clarificationUntilDuration": 0,
    "enquiryPeriodRegulation": 0,
    "hasAuction": False,
    "hasAwardComplaints": False,
    "hasCancellationComplaints": False,
    "hasTenderComplaints": False,
    "hasValueRestriction": True,
    "minTenderingDuration": 0,
    "tenderComplainRegulation": 0,
}

# The legal ground a reporting procedure has to name.
REPORTING_CAUSE_DETAILS: dict[str, Any] = {
    "code": "activeCombatZone",
    "description": (
        "У разі, коли державний замовник або його відокремлений підрозділ, що здійснює закупівлю, "
        "перебуває на території активних бойових дій, які не завершені на дату укладення державного "
        "контракту (договору)"
    ),
    "scheme": "DECREE1275",
    "title": "Підпункт 8 пункту 9",
}


def procurement_method_details(acceleration: float | None = None) -> str:
    """The accelerator the CDB needs to run a procedure faster than real time."""
    return f"quick, accelerator={int(acceleration)}" if acceleration else ""


def lots_data(count: int = 1, amount: float = 2500, **kwargs: Any) -> list[dict[str, Any]]:
    """``count`` lots, numbered in their titles."""
    return [lot_data(title=f"Лот №{index + 1}: {fake.word()}", amount=amount, **kwargs) for index in range(count)]


def items_data(
    count: int = 1,
    lots: list[dict[str, Any]] | None = None,
    quantity: float = 1,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """
    ``count`` items per lot, or ``count`` items with no lot binding.

    With lots the items are spread over them, which is what a multi lot tender
    needs: every lot has to hold at least one item.
    """
    if not lots:
        return [item_data(quantity=quantity, **kwargs) for _ in range(count)]
    return [item_data(quantity=quantity, related_lot=lot["id"], **kwargs) for lot in lots for _ in range(max(count, 1))]


def milestones_data(lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Payment and delivery milestones, per lot when the tender has lots."""
    if not lots:
        return payment_milestones_data()
    return [milestone for lot in lots for milestone in payment_milestones_data(related_lot=lot["id"])]


def tender_data(
    procurement_method_type: str = "aboveThreshold",
    title: str | None = None,
    lots: list[dict[str, Any]] | None = None,
    items: list[dict[str, Any]] | None = None,
    milestones: list[dict[str, Any]] | None = None,
    procuring_entity: dict[str, Any] | None = None,
    value: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
    acceleration: float | None = None,
    submission: str | None = None,
    tendering_days: float = 40,
    main_procurement_category: str = "goods",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    An open tender ready to be created.

    Everything it composes can be handed in instead: ``lots``, ``items``,
    ``milestones``, ``procuring_entity``, ``value`` and the ``config`` block.
    Remaining keyword arguments patch the ``data`` part by path.
    """
    lots = lots if lots is not None else []
    items = items if items is not None else items_data(lots=lots)
    data: dict[str, Any] = {
        "items": items,
        "mainProcurementCategory": main_procurement_category,
        "milestones": milestones if milestones is not None else milestones_data(lots),
        "mode": "test",
        "procurementMethodDetails": procurement_method_details(acceleration),
        "procurementMethodType": procurement_method_type,
        "procuringEntity": procuring_entity or procuring_entity_data(),
        "status": "draft",
        "tenderPeriod": {
            "startDate": from_now_iso(),
            "endDate": from_now_iso(acceleration=acceleration, days=tendering_days),
        },
        "title": f"{fake.sentence(nb_words=10)} (created with robot_tests)",
        "title_en": f"{fake_en.sentence(nb_words=10)} (created with robot_tests)",
        "value": value or value_data(amount=0),
    }
    if lots:
        data["lots"] = lots
    if submission:
        data["submissionMethodDetails"] = submission
    return {
        "config": config if config is not None else dict(ABOVE_THRESHOLD_CONFIG),
        "data": build(data, **kwargs),
    }


def reporting_tender_data(
    amount: float = 500000,
    acceleration: float | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    A reporting tender: a limited procedure with no bids and no auction, so it
    names the legal ground for it and goes straight to an award.
    """
    payload = tender_data(
        procurement_method_type="reporting",
        acceleration=acceleration,
        config=dict(REPORTING_CONFIG),
        value=value_data(amount=amount, value_added_tax_included=True),
        items=items_data(count=1),
        milestones=[
            milestone_data(code="prepayment", percentage=70, sequence_number=1),
            milestone_data(code="postpayment", percentage=30, sequence_number=2, duration_type="banking"),
            milestone_data(
                code="standard",
                title="signingTheContract",
                milestone_type="delivery",
                sequence_number=3,
            ),
        ],
        procuring_entity=procuring_entity_data(kind="other"),
    )
    data = payload["data"]
    data["procurementMethod"] = "limited"
    data["causeDetails"] = dict(REPORTING_CAUSE_DETAILS)
    data["description"] = fake.sentence(nb_words=8)
    data["description_en"] = fake_en.sentence(nb_words=8)
    data.pop("tenderPeriod", None)
    payload["data"] = build(data, **kwargs)
    return payload


def tender_patch_data(status: str, **kwargs: Any) -> dict[str, Any]:
    """A patch that moves the tender to ``status``."""
    return {"data": build({"status": status}, **kwargs)}
