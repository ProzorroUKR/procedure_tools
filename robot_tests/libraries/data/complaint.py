"""
Claim and complaint payloads.

The two live in the same collection and are told apart by ``type``:

- a **claim** is pre-trial and addressed to the tender owner, who answers it
  with a resolution; the claimant then says whether that satisfied them,
- a **complaint** is escalated to the reviewers, carries the objections that
  say what is being challenged and what remedy is asked for, and is decided by
  the reviewers rather than by the tender owner.

Which of the two a procedure has is config: ``hasTenderComplaints`` and
``hasAwardComplaints``. belowThreshold and requestForProposal have claims only.
"""

from __future__ import annotations

from typing import Any

from data.question import question_author_data
from data.utils import build, fake

CLAIM = "claim"
COMPLAINT = "complaint"

# What a claim answer can conclude.
RESOLUTION_TYPES = ("invalid", "resolved", "declined")

# Endings the reviewers reach without deciding the complaint on its merits.
REJECTED_STATUSES = ("stopped", "invalid")

# Who a post is addressed to. A reviewer writes to one of the two sides, and
# either side writes back to the reviewers.
COMPLAINT_OWNER = "complaint_owner"
TENDER_OWNER = "tender_owner"
REVIEWERS = "aboveThresholdReviewers"

# What an objection says it is about, and what it asks for.
VIOLATION_SCHEME = "violation_amcu"
DEFAULT_VIOLATION = "corruptionDescription"
DEFAULT_REMEDY = "setAsideAward"


def objection_data(
    related_item: str,
    relates_to: str = "tender",
    violation: str = DEFAULT_VIOLATION,
    remedy: str = DEFAULT_REMEDY,
    sequence_number: int = 1,
    **kwargs: Any,
) -> dict[str, Any]:
    """One objection of a complaint: what is wrong, and what should be done."""
    return build(
        {
            "title": fake.sentence(nb_words=4),
            "description": fake.paragraph(nb_sentences=2),
            "relatesTo": relates_to,
            "relatedItem": related_item,
            "classification": {
                "scheme": VIOLATION_SCHEME,
                "id": violation,
                "description": "Опис порушення",
            },
            "requestedRemedies": [{"type": remedy, "description": fake.sentence(nb_words=6)}],
            "arguments": [{"description": fake.paragraph(nb_sentences=2)}],
            "sequenceNumber": sequence_number,
        },
        **kwargs,
    )


def claim_data(author: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    """A draft claim, addressed to the tender owner."""
    return {
        "data": build(
            {
                "author": author or question_author_data(),
                "title": fake.sentence(nb_words=4),
                "description": fake.paragraph(nb_sentences=2),
                "status": "draft",
                "type": CLAIM,
            },
            **kwargs,
        )
    }


def complaint_data(
    related_item: str,
    relates_to: str = "tender",
    author: dict[str, Any] | None = None,
    objections: list[dict[str, Any]] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    A draft complaint, for the reviewers.

    ``related_item`` is what the objection is about - the tender id for a
    tender complaint, the award id for an award complaint.
    """
    return {
        "data": build(
            {
                "author": author or question_author_data(),
                "title": fake.sentence(nb_words=4),
                "description": fake.paragraph(nb_sentences=2),
                "status": "draft",
                "type": COMPLAINT,
                "objections": objections
                if objections is not None
                else [objection_data(related_item, relates_to=relates_to)],
            },
            **kwargs,
        )
    }


def claim_submit_data(**kwargs: Any) -> dict[str, Any]:
    """The claimant submits the draft, which starts the owner's clock."""
    return {"data": build({"status": CLAIM}, **kwargs)}


def claim_answer_data(resolution_type: str = "resolved", **kwargs: Any) -> dict[str, Any]:
    """The tender owner answers, saying what they concluded and why."""
    if resolution_type not in RESOLUTION_TYPES:
        raise ValueError(f"a claim is answered with one of {RESOLUTION_TYPES}, not {resolution_type!r}")
    return {
        "data": build(
            {
                "status": "answered",
                "resolutionType": resolution_type,
                "resolution": fake.paragraph(nb_sentences=3, variable_nb_sentences=False),
            },
            **kwargs,
        )
    }


def claim_resolution_data(satisfied: bool = True, **kwargs: Any) -> dict[str, Any]:
    """
    The claimant says whether the answer settled it.

    Saying yes closes the claim as ``resolved``. Saying no only records that:
    the claim stays where it is, so no status is sent with it.
    """
    data: dict[str, Any] = {"satisfied": satisfied}
    if satisfied:
        data["status"] = "resolved"
    return {"data": build(data, **kwargs)}


def claim_cancel_data(**kwargs: Any) -> dict[str, Any]:
    """The claimant withdraws the claim."""
    return {"data": build({"status": "cancelled"}, **kwargs)}


def complaint_submit_data(**kwargs: Any) -> dict[str, Any]:
    """The bot moves a paid complaint on to the reviewers."""
    return {"data": build({"status": "pending"}, **kwargs)}


def complaint_accept_data(review_place: str = "Place of review", **kwargs: Any) -> dict[str, Any]:
    """A reviewer takes the complaint on and says where it will be reviewed."""
    return {
        "data": build(
            {
                "status": "accepted",
                "reviewDate": "2020-05-01T01:00:00+03:00",
                "reviewPlace": review_place,
            },
            **kwargs,
        )
    }


def complaint_decision_data(status: str = "satisfied", **kwargs: Any) -> dict[str, Any]:
    """The reviewers decide: satisfied, declined or stopped."""
    return {"data": build({"status": status}, **kwargs)}


def complaint_resolution_data(action: str = "Внесено зміни", **kwargs: Any) -> dict[str, Any]:
    """The tender owner says what they did about a satisfied complaint."""
    return {"data": build({"status": "resolved", "tendererAction": action}, **kwargs)}


def complaint_rejection_data(status: str, reject_reason: str, **kwargs: Any) -> dict[str, Any]:
    """
    The reviewers end the complaint without deciding it on its merits.

    ``stopped`` and ``invalid`` both have to say why, and the reason is part of
    the contract: ``buyerViolationsCorrected`` when the owner fixed what was
    complained about, ``alreadyExists`` when the same complaint is already in
    front of them.
    """
    if status not in REJECTED_STATUSES:
        raise ValueError(f"a rejection is one of {REJECTED_STATUSES}, not {status!r}")
    return {"data": build({"status": status, "rejectReason": reject_reason}, **kwargs)}


def complaint_mistaken_data(**kwargs: Any) -> dict[str, Any]:
    """The complainant withdraws it as raised by mistake."""
    return {"data": build({"status": "mistaken"}, **kwargs)}


def complaint_post_data(
    related_objection: str,
    recipient: str = COMPLAINT_OWNER,
    related_post: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    One message in the exchange around a complaint.

    A post is addressed to somebody - the complainant or the reviewers - and
    answers either an objection or an earlier post, which is what
    ``related_post`` says.
    """
    data: dict[str, Any] = {
        "title": fake.sentence(nb_words=5),
        "description": fake.paragraph(nb_sentences=2),
        "relatedObjection": related_objection,
        "recipient": recipient,
    }
    if related_post:
        data["relatedPost"] = related_post
    return {"data": build(data, **kwargs)}
