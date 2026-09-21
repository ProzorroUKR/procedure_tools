"""
Contract payloads.

A contract is created by the CDB once an award goes active, so the builders
take the contract that is already there and describe the change to make to it:
sign it, price its items, amend it, pay it and close it.
"""

from __future__ import annotations

from typing import Any

from data.common import signer_info_data
from data.document import SIGNATURE_CONTENT, document_data
from data.utils import build, fake, from_date_iso, from_now_iso

# The fields a contract item keeps when its price is set. The API compares an
# item it is sent against the one already on the contract and refuses it as a
# new item unless every "main" field is identical, so the ones it names -
# classification, relatedLot, relatedBuyer, additionalClassifications and
# product - all have to be carried over. Dropping "product" is what made a
# localised item look new.
ITEM_FIELDS = (
    "additionalClassifications",
    "classification",
    "deliveryAddress",
    "deliveryDate",
    "description",
    "description_en",
    "id",
    "product",
    "quantity",
    "relatedBuyer",
    "relatedLot",
)


def contract_value(contract: dict[str, Any]) -> dict[str, Any]:
    return contract.get("value") or {}


def contract_item_data(item: dict[str, Any], amount: float, **kwargs: Any) -> dict[str, Any]:
    """One contract item with the agreed price per unit."""
    data: dict[str, Any] = {field: item[field] for field in ITEM_FIELDS if field in item}
    data["unit"] = {
        "code": item.get("unit", {}).get("code", "KGM"),
        "name": item.get("unit", {}).get("name", "кг"),
        "value": {"amount": amount, "valueAddedTaxIncluded": False},
    }
    return build(data, **kwargs)


def unit_amount(contract: dict[str, Any]) -> float:
    """The contract value spread evenly over the quantities of its items."""
    items = contract.get("items") or []
    quantity = sum(item.get("quantity", 0) for item in items) or 1
    return round(contract_value(contract).get("amount", 0) / quantity, 2)


def contract_active_data(
    contract: dict[str, Any],
    amount: float | None = None,
    item_amount: float | None = None,
    contract_number: int = 1,
    duration_days: float = 365,
    with_items: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    The signed contract: its number, the period it runs for, the agreed value
    and the price of every item.
    """
    date_signed = contract.get("dateModified") or from_now_iso()
    value = contract_value(contract)
    total = amount if amount is not None else value.get("amount", 0)
    data: dict[str, Any] = {
        "contractNumber": contract_number,
        "dateSigned": date_signed,
        "period": {
            "startDate": date_signed,
            "endDate": from_date_iso(date_signed, days=duration_days),
        },
        "status": "active",
        "value": {
            "amount": total,
            "amountNet": total,
            "valueAddedTaxIncluded": False,
        },
    }
    if with_items and contract.get("items"):
        price = item_amount if item_amount is not None else unit_amount(contract)
        data["items"] = [contract_item_data(item, amount=price) for item in contract["items"]]
    return {"data": build(data, **kwargs)}


def contract_signer_info_data(**kwargs: Any) -> dict[str, Any]:
    """The signatory of one side of the contract, ready to be sent."""
    return {"data": signer_info_data(**kwargs)}


def contract_value_data(amount: float, **kwargs: Any) -> dict[str, Any]:
    """A change of the agreed value of an active contract."""
    return {
        "data": build(
            {"value": {"amount": amount, "amountNet": amount, "valueAddedTaxIncluded": False}},
            **kwargs,
        )
    }


def contract_signature_data(title: str, **kwargs: Any) -> dict[str, Any]:
    """
    A signature on an electronic contract.

    The API reads the format from the file name, so the title keeps its
    ``.p7s`` ending; what makes it a signature rather than any attachment is
    the document type.
    """
    return document_data(title=title, document_type="contractSignature", content=SIGNATURE_CONTENT, **kwargs)


def contract_cancellation_data(reason: str, **kwargs: Any) -> dict[str, Any]:
    """Cancelling a contract, or an amendment to one, with the reason for it."""
    return {"data": build({"reason": reason}, **kwargs)}


def contract_change_data(rationale_type: str = "itemPriceChange", **kwargs: Any) -> dict[str, Any]:
    """An amendment to an active contract, with the reason for it."""
    return {
        "data": build(
            {
                "rationale": fake.sentence(nb_words=8),
                "rationaleTypes": [rationale_type],
            },
            **kwargs,
        )
    }


def contract_change_active_data(contract: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    """The signature that makes an amendment take effect."""
    return {
        "data": build(
            {
                "dateSigned": contract.get("dateModified") or from_now_iso(),
                "status": "active",
            },
            **kwargs,
        )
    }


def contract_terminated_data(amount: float, **kwargs: Any) -> dict[str, Any]:
    """Closing the contract, stating how much of it was actually paid."""
    return {
        "data": build(
            {
                "amountPaid": {"amount": amount, "amountNet": amount, "valueAddedTaxIncluded": False},
                "status": "terminated",
            },
            **kwargs,
        )
    }
