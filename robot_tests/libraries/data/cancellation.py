"""
Cancellation payloads.

A cancellation is created as a draft, has to state why and carry the signed
report, and only then may be submitted. Where the procedure has cancellation
complaints it waits out a complaint period in ``pending``; where it has none it
goes straight to ``active`` and the tender is cancelled with it.
"""

from __future__ import annotations

from typing import Any

from data.document import document_data
from data.utils import build, fake

# What a cancellation may give as its reason, since the 2020 release.
REASON_TYPES = ("noDemand", "unFixable", "forceMajeure", "expensesCut")

# The signed report a cancellation has to carry before it can be submitted.
REPORT_DOCUMENT_TYPE = "cancellationReport"


def cancellation_data(
    reason_type: str = "noDemand",
    related_lot: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """A draft cancellation, of the whole tender or of one lot."""
    data: dict[str, Any] = {
        "reason": fake.paragraph(nb_sentences=2),
        "reasonType": reason_type,
    }
    if related_lot:
        data["relatedLot"] = related_lot
    return {"data": build(data, **kwargs)}


def cancellation_report_data(title: str = "cancellation_report.p7s", **kwargs: Any) -> dict[str, Any]:
    """The signed report without which a cancellation cannot leave draft."""
    return document_data(title=title, document_type=REPORT_DOCUMENT_TYPE, **kwargs)


def cancellation_patch_data(status: str, **kwargs: Any) -> dict[str, Any]:
    """A patch that moves the cancellation to ``status``."""
    return {"data": build({"status": status}, **kwargs)}
