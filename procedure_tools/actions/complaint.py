"""
Complaint and claim actions for the tender, its awards and its qualifications.

    2050_tender_complaint_create_0.json               tender complaint 0
    2060_tender_complaint_patch_0_bot.json            patched by the bot
    2320_tender_award_complaint_create_0_1.json       complaint 1 of award 0
    2330_tender_award_complaint_patch_0_1_reviewer.json
    2340_tender_award_complaints_get_0.json           list the complaints of award 0
    2624_tender_award_claim_create_0_0.json           claim 0 of award 0
    2626_tender_award_claim_patch_0_0_tenderer.json   answered by the tender owner
    2639_tender_award_claims_get_1.json               list the claims of award 1

Complaints (``"type": "complaint"``) are reviewed by the bot and the reviewer;
claims (``"type": "claim"``) are answered by the tender owner and closed by
their owner, so they need no bot or reviewer token. The two are stored apart:
``tender_complaints`` / ``tender_claims``, ``award_complaints`` / ``award_claims``, ...

Roles: ``bot`` and ``reviewer`` use the tokens passed with ``--bot-token`` and
``--reviewer-token``, ``tenderer`` uses the tender token and ``complainer`` the
complaint (or claim) token. A complaint is skipped entirely when a role needed
by its patch steps has no token.
"""

import logging
from typing import Any

from procedure_tools.actions.common import (
    award,
    qualification,
    skip,
    tender_id,
    tender_token,
)
from procedure_tools.actions.registry import action
from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import get_data, get_token
from procedure_tools.utils.handlers import (
    complaints_get_success_handler,
    error,
    item_patch_success_handler,
    tender_post_complaint_success_handler,
)

logger = logging.getLogger(__name__)


ROLES = ("bot", "reviewer", "tenderer", "complainer")

KINDS: dict[str, dict[str, Any]] = {
    "tender": {"collection": None, "resolve": None},
    "award": {"collection": "awards", "resolve": award},
    "qualification": {"collection": "qualifications", "resolve": qualification},
}

TYPES = ("complaint", "claim")


def complaint_action(kind: str, kind_type: str, verb: str) -> str:
    """Action name of a step: tender_complaint_patch, tender_award_claim_create, tender_award_claims_get, ..."""
    name = f"{kind_type}s_get" if verb == "get" else f"{kind_type}_{verb}"
    return f"tender_{name}" if kind == "tender" else f"tender_{kind}_{name}"


def complaint_ref(step: Step, kind: str) -> tuple[int | None, int, str | None]:
    """(object index, complaint index, role) from the step parts."""
    object_index: int | None
    if kind == "tender":
        object_index = None
        complaint_index = step.index(0)
        role = step.part(1)
    else:
        object_index = step.index(0)
        complaint_index = step.index(1)
        role = step.part(2)
    return object_index, complaint_index, role


def complaint_label(kind: str, kind_type: str, object_index: int | None, complaint_index: int) -> str:
    """Human readable name of a complaint: ``award 0 claim 1``, ``tender complaint 2``."""
    prefix = kind if object_index is None else f"{kind} {object_index}"
    return f"{prefix} {kind_type} {complaint_index}"


def complaints_allowed(
    context: Context, kind: str, kind_type: str, object_index: int | None, complaint_index: int
) -> bool:
    """False when a patch step of this complaint needs a bot or reviewer token that was not provided."""
    roles: set[str | None] = set()
    for step in context.steps:
        if step.action != complaint_action(kind, kind_type, "patch"):
            continue
        step_object_index, step_complaint_index, role = complaint_ref(step, kind)
        if step_object_index == object_index and step_complaint_index == complaint_index:
            roles.add(role)
    missing_bot = "bot" in roles and not context.args.bot_token
    missing_reviewer = "reviewer" in roles and not context.args.reviewer_token
    return not (missing_bot or missing_reviewer)


def complaints_path(context: Context, kind: str, object_index: int | None) -> str:
    if kind == "tender":
        return f"tenders/{tender_id(context)}/complaints"
    object_data = KINDS[kind]["resolve"](context, object_index)
    return f"tenders/{tender_id(context)}/{kind}s/{object_data['id']}/complaints"


def complaint_store(
    context: Context, kind: str, kind_type: str, object_index: int | None
) -> tuple[list[Any], list[Any]]:
    """(complaints, tokens) lists of the object; stored under <kind>_<type>s[(object index)]."""
    key = f"{kind}_{kind_type}s"
    if kind == "tender":
        complaints = context.setdefault(key, [])
        tokens = context.setdefault(f"{key}_tokens", [])
    else:
        complaints = context.setdefault(key, {}).setdefault(object_index, [])
        tokens = context.setdefault(f"{key}_tokens", {}).setdefault(object_index, [])
    return complaints, tokens


def set_complaint(
    context: Context,
    kind: str,
    kind_type: str,
    object_index: int | None,
    complaint_index: int,
    complaint: dict[str, Any],
    token: str | None = None,
) -> None:
    complaints, tokens = complaint_store(context, kind, kind_type, object_index)
    for items in (complaints, tokens):
        while len(items) <= complaint_index:
            items.append(None)
    complaints[complaint_index] = complaint
    if token is not None:
        tokens[complaint_index] = token


def get_complaint(
    context: Context,
    kind: str,
    kind_type: str,
    object_index: int | None,
    complaint_index: int,
) -> tuple[dict[str, Any] | None, str | None]:
    complaints, tokens = complaint_store(context, kind, kind_type, object_index)
    if complaint_index >= len(complaints) or complaints[complaint_index] is None:
        return None, None
    return complaints[complaint_index], tokens[complaint_index]


def object_bid_token(context: Context, kind: str, object_index: int | None) -> str | None:
    """
    Token of the bidder of an unsuccessful award or qualification, if it is known.

    A claim on an unsuccessful award or qualification is accepted only from the bidder it
    rejected; on an active one any bidder may complain, so the first bid token is used then.
    """
    if kind == "tender" or object_index is None:
        return None
    object_data = KINDS[kind]["resolve"](context, object_index)
    if object_data.get("status") != "unsuccessful":
        return None
    bid_id = object_data.get("bid_id") or object_data.get("bidID")
    bids = context.get("bids") or []
    bids_tokens = context.get("bids_tokens") or []
    for bid_index, bid_data in enumerate(bids):
        if bid_data and bid_data.get("id") == bid_id and bid_index < len(bids_tokens) and bids_tokens[bid_index]:
            token: str = bids_tokens[bid_index]
            return token
    return None


def create_complaint(context: Context, step: Step, kind: str, kind_type: str) -> None:
    object_index, complaint_index, _ = complaint_ref(step, kind)
    label = complaint_label(kind, kind_type, object_index, complaint_index)
    if not complaints_allowed(context, kind, kind_type, object_index, complaint_index):
        skip(f"Skipping {label}: bot and reviewer tokens are required")
        return
    if kind == "tender":
        acc_token = tender_token(context)
    else:
        bids_tokens = context.get("bids_tokens") or []
        if not bids_tokens:
            skip(f"Skipping {label}: no bid tokens in context")
            return
        acc_token = object_bid_token(context, kind, object_index) or bids_tokens[0]
    logger.info(f"Creating {label}...\n")
    data = context.load(step)
    data["data"].setdefault("type", kind_type)
    response = context.client.post(
        complaints_path(context, kind, object_index),
        json=data,
        acc_token=acc_token,
        auth_token=context.args.token,
        success_handler=tender_post_complaint_success_handler,
    )
    set_complaint(context, kind, kind_type, object_index, complaint_index, get_data(response), get_token(response))


def patch_complaint(context: Context, step: Step, kind: str, kind_type: str) -> None:
    object_index, complaint_index, role = complaint_ref(step, kind)
    label = complaint_label(kind, kind_type, object_index, complaint_index)
    if role is None or role not in ROLES:
        error(f"{step.filename}: expected a role part {ROLES}, got {role!r}")
        return
    if not complaints_allowed(context, kind, kind_type, object_index, complaint_index):
        skip(f"Skipping {label} patch: bot and reviewer tokens are required")
        return
    complaint, complaint_token = get_complaint(context, kind, kind_type, object_index, complaint_index)
    if complaint is None:
        skip(f"Skipping {label} patch: the {kind_type} was not created")
        return
    auth_tokens = {
        "bot": context.args.bot_token,
        "reviewer": context.args.reviewer_token,
        "tenderer": context.args.token,
        "complainer": context.args.token,
    }
    acc_tokens = {
        "bot": None,
        "reviewer": None,
        "tenderer": tender_token(context),
        "complainer": complaint_token,
    }
    if not auth_tokens[role]:
        error(f"{step.filename}: no auth token for role {role!r}")
    logger.info(f"Patching {label} as {role}...\n")
    data = context.load(step)
    response = context.client.patch(
        f"{complaints_path(context, kind, object_index)}/{complaint['id']}",
        json=data,
        acc_token=acc_tokens[role],
        auth_token=auth_tokens[role],
        success_handler=item_patch_success_handler,
    )
    set_complaint(context, kind, kind_type, object_index, complaint_index, get_data(response))


def get_complaints(context: Context, step: Step, kind: str, kind_type: str) -> None:
    """List the complaints or claims of an object and refresh the stored ones (their status may change server side)."""
    object_index = None if kind == "tender" else step.index(0)
    label = kind if object_index is None else f"{kind} {object_index}"
    logger.info(f"Getting {label} {kind_type}s...\n")
    context.load(step)
    response = context.client.get(complaints_path(context, kind, object_index), auth_token=context.args.token)
    listed: list[dict[str, Any]] = response.json()["data"]
    listed = [complaint for complaint in listed if complaint.get("type", "complaint") == kind_type]
    complaints_get_success_handler(kind_type, listed)
    complaints, _ = complaint_store(context, kind, kind_type, object_index)
    by_id = {complaint["id"]: complaint for complaint in listed}
    for complaint_index, stored in enumerate(complaints):
        if stored is not None and stored["id"] in by_id:
            complaints[complaint_index] = by_id[stored["id"]]


# --- complaints


@action("tender_complaint_create")
def tender_complaint_create(context: Context, step: Step) -> None:
    """Create a tender complaint (POST tenders/{id}/complaints); parts: [complaint index]."""
    create_complaint(context, step, "tender", "complaint")


@action("tender_complaint_patch")
def tender_complaint_patch(context: Context, step: Step) -> None:
    """Patch a tender complaint as a role; parts: [complaint index, bot|reviewer|tenderer|complainer]."""
    patch_complaint(context, step, "tender", "complaint")


@action("tender_complaints_get")
def tender_complaints_get(context: Context, step: Step) -> None:
    """List the tender complaints (GET tenders/{id}/complaints) and refresh them in context."""
    get_complaints(context, step, "tender", "complaint")


@action("tender_award_complaint_create")
def tender_award_complaint_create(context: Context, step: Step) -> None:
    """Create an award complaint (POST tenders/{id}/awards/{id}/complaints); parts: [award index, complaint index]."""
    create_complaint(context, step, "award", "complaint")


@action("tender_award_complaint_patch")
def tender_award_complaint_patch(context: Context, step: Step) -> None:
    """Patch an award complaint as a role; parts: [award index, complaint index, bot|reviewer|tenderer|complainer]."""
    patch_complaint(context, step, "award", "complaint")


@action("tender_award_complaints_get")
def tender_award_complaints_get(context: Context, step: Step) -> None:
    """List the complaints of an award (GET tenders/{id}/awards/{id}/complaints); parts: [award index]."""
    get_complaints(context, step, "award", "complaint")


@action("tender_qualification_complaint_create")
def tender_qualification_complaint_create(context: Context, step: Step) -> None:
    """Create a qualification complaint (POST tenders/{id}/qualifications/{id}/complaints); parts: [qualification index, complaint index]."""
    create_complaint(context, step, "qualification", "complaint")


@action("tender_qualification_complaint_patch")
def tender_qualification_complaint_patch(context: Context, step: Step) -> None:
    """Patch a qualification complaint as a role; parts: [qualification index, complaint index, bot|reviewer|tenderer|complainer]."""
    patch_complaint(context, step, "qualification", "complaint")


@action("tender_qualification_complaints_get")
def tender_qualification_complaints_get(context: Context, step: Step) -> None:
    """List the complaints of a qualification (GET tenders/{id}/qualifications/{id}/complaints); parts: [qualification index]."""
    get_complaints(context, step, "qualification", "complaint")


# --- claims


@action("tender_claim_create")
def tender_claim_create(context: Context, step: Step) -> None:
    """Create a tender claim (POST tenders/{id}/complaints with type claim); parts: [claim index]."""
    create_complaint(context, step, "tender", "claim")


@action("tender_claim_patch")
def tender_claim_patch(context: Context, step: Step) -> None:
    """Patch a tender claim as a role; parts: [claim index, tenderer|complainer]."""
    patch_complaint(context, step, "tender", "claim")


@action("tender_claims_get")
def tender_claims_get(context: Context, step: Step) -> None:
    """List the tender claims (GET tenders/{id}/complaints, type claim) and refresh them in context."""
    get_complaints(context, step, "tender", "claim")


@action("tender_award_claim_create")
def tender_award_claim_create(context: Context, step: Step) -> None:
    """Create an award claim (POST tenders/{id}/awards/{id}/complaints with type claim); parts: [award index, claim index]."""
    create_complaint(context, step, "award", "claim")


@action("tender_award_claim_patch")
def tender_award_claim_patch(context: Context, step: Step) -> None:
    """Patch an award claim as a role; parts: [award index, claim index, tenderer|complainer]."""
    patch_complaint(context, step, "award", "claim")


@action("tender_award_claims_get")
def tender_award_claims_get(context: Context, step: Step) -> None:
    """List the claims of an award (GET tenders/{id}/awards/{id}/complaints, type claim); parts: [award index]."""
    get_complaints(context, step, "award", "claim")


@action("tender_qualification_claim_create")
def tender_qualification_claim_create(context: Context, step: Step) -> None:
    """Create a qualification claim (POST tenders/{id}/qualifications/{id}/complaints with type claim); parts: [qualification index, claim index]."""
    create_complaint(context, step, "qualification", "claim")


@action("tender_qualification_claim_patch")
def tender_qualification_claim_patch(context: Context, step: Step) -> None:
    """Patch a qualification claim as a role; parts: [qualification index, claim index, tenderer|complainer]."""
    patch_complaint(context, step, "qualification", "claim")


@action("tender_qualification_claims_get")
def tender_qualification_claims_get(context: Context, step: Step) -> None:
    """List the claims of a qualification (GET tenders/{id}/qualifications/{id}/complaints, type claim); parts: [qualification index]."""
    get_complaints(context, step, "qualification", "claim")
