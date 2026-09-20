"""
Award payloads.

In an open procedure the awards are produced by the auction and only patched;
in a limited procedure such as reporting the procuring entity creates the award
itself, naming the supplier it picked.
"""

from __future__ import annotations

from typing import Any

from data.common import supplier_data, value_data
from data.utils import build, new_id


def award_data(
    amount: float = 475000,
    suppliers: list[dict[str, Any]] | None = None,
    status: str = "pending",
    value_added_tax_included: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """An award a procuring entity creates for a supplier it chose."""
    return {
        "data": build(
            {
                "id": new_id(),
                "status": status,
                "suppliers": suppliers or [supplier_data()],
                "value": value_data(amount=amount, value_added_tax_included=value_added_tax_included),
            },
            **kwargs,
        )
    }


def award_qualification_data(qualified: bool = True, eligible: bool | None = True, **kwargs: Any) -> dict[str, Any]:
    """The decision that the bidder meets the criteria."""
    data: dict[str, Any] = {"qualified": qualified}
    if eligible is not None:
        data["eligible"] = eligible
    return {"data": build(data, **kwargs)}


def award_patch_data(status: str, **kwargs: Any) -> dict[str, Any]:
    """A patch that moves the award to ``status`` (``active`` or ``unsuccessful``)."""
    return {"data": build({"status": status}, **kwargs)}
