"""
Complaint actions for the tender, its awards and its qualifications.

    2050_tender_complaint_create_0.json               tender complaint 0
    2060_tender_complaint_patch_0_bot.json            patched by the bot
    2320_award_complaint_create_0_1.json              complaint 1 of award 0
    2330_award_complaint_patch_0_1_reviewer.json      patched by the reviewer
    2230_qualification_complaint_patch_1_0_tenderer.json

Roles: ``bot`` and ``reviewer`` use the tokens passed with ``--bot-token`` and
``--reviewer-token``, ``tenderer`` uses the tender token and ``complainer`` the
complaint token. Like ``procedure``, complaints of an object are skipped
entirely when a role needed by their patch steps has no token.
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


def complaint_action(kind: str, verb: str) -> str:
    """Action name of a complaint step: tender_complaint_patch, tender_award_complaint_patch, ..."""
    return f"tender_complaint_{verb}" if kind == "tender" else f"tender_{kind}_complaint_{verb}"


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


def complaints_allowed(context: Context, kind: str, object_index: int | None) -> bool:
    """False when a patch step of these complaints needs a bot or reviewer token that was not provided."""
    roles: set[str | None] = set()
    for step in context.steps:
        if step.action != complaint_action(kind, "patch"):
            continue
        step_object_index, _, role = complaint_ref(step, kind)
        if step_object_index == object_index:
            roles.add(role)
    missing_bot = "bot" in roles and not context.args.bot_token
    missing_reviewer = "reviewer" in roles and not context.args.reviewer_token
    return not (missing_bot or missing_reviewer)


def complaints_path(context: Context, kind: str, object_index: int | None) -> str:
    if kind == "tender":
        return f"tenders/{tender_id(context)}/complaints"
    object_data = KINDS[kind]["resolve"](context, object_index)
    return f"tenders/{tender_id(context)}/{kind}s/{object_data['id']}/complaints"


def complaint_store(context: Context, kind: str, object_index: int | None) -> tuple[list[Any], list[Any]]:
    """(complaints, tokens) lists of the object; stored under <kind>_complaints[(object index)]."""
    if kind == "tender":
        complaints = context.setdefault("tender_complaints", [])
        tokens = context.setdefault("tender_complaints_tokens", [])
    else:
        complaints = context.setdefault(f"{kind}_complaints", {}).setdefault(object_index, [])
        tokens = context.setdefault(f"{kind}_complaints_tokens", {}).setdefault(object_index, [])
    return complaints, tokens


def set_complaint(
    context: Context,
    kind: str,
    object_index: int | None,
    complaint_index: int,
    complaint: dict[str, Any],
    token: str | None = None,
) -> None:
    complaints, tokens = complaint_store(context, kind, object_index)
    for items in (complaints, tokens):
        while len(items) <= complaint_index:
            items.append(None)
    complaints[complaint_index] = complaint
    if token is not None:
        tokens[complaint_index] = token


def get_complaint(
    context: Context,
    kind: str,
    object_index: int | None,
    complaint_index: int,
) -> tuple[dict[str, Any] | None, str | None]:
    complaints, tokens = complaint_store(context, kind, object_index)
    if complaint_index >= len(complaints) or complaints[complaint_index] is None:
        return None, None
    return complaints[complaint_index], tokens[complaint_index]


def create_complaint(context: Context, step: Step, kind: str) -> None:
    object_index, complaint_index, _ = complaint_ref(step, kind)
    label = kind if object_index is None else f"{kind} {object_index}"
    if not complaints_allowed(context, kind, object_index):
        skip(f"Skipping {label} complaint {complaint_index}: bot and reviewer tokens are required")
        return
    if kind == "tender":
        acc_token = tender_token(context)
    else:
        # any of the suppliers can create a complaint
        bids_tokens = context.get("bids_tokens") or []
        if not bids_tokens:
            skip(f"Skipping {label} complaint {complaint_index}: no bid tokens in context")
            return
        acc_token = bids_tokens[0]
    logger.info(f"Creating {label} complaint...\n")
    data = context.load(step)
    response = context.client.post(
        complaints_path(context, kind, object_index),
        json=data,
        acc_token=acc_token,
        auth_token=context.args.token,
        success_handler=tender_post_complaint_success_handler,
    )
    set_complaint(context, kind, object_index, complaint_index, get_data(response), get_token(response))


def patch_complaint(context: Context, step: Step, kind: str) -> None:
    object_index, complaint_index, role = complaint_ref(step, kind)
    label = kind if object_index is None else f"{kind} {object_index}"
    if role is None or role not in ROLES:
        error(f"{step.filename}: expected a role part {ROLES}, got {role!r}")
        return
    if not complaints_allowed(context, kind, object_index):
        skip(f"Skipping {label} complaint {complaint_index} patch: bot and reviewer tokens are required")
        return
    complaint, complaint_token = get_complaint(context, kind, object_index, complaint_index)
    if complaint is None:
        skip(f"Skipping {label} complaint {complaint_index} patch: the complaint was not created")
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
    logger.info(f"Patching {label} complaint as {role}...\n")
    data = context.load(step)
    response = context.client.patch(
        f"{complaints_path(context, kind, object_index)}/{complaint['id']}",
        json=data,
        acc_token=acc_tokens[role],
        auth_token=auth_tokens[role],
        success_handler=item_patch_success_handler,
    )
    set_complaint(context, kind, object_index, complaint_index, get_data(response))


@action("tender_complaint_create")
def tender_complaint_create(context: Context, step: Step) -> None:
    """Create a tender complaint (POST tenders/{id}/complaints); parts: [complaint index]."""
    create_complaint(context, step, "tender")


@action("tender_complaint_patch")
def tender_complaint_patch(context: Context, step: Step) -> None:
    """Patch a tender complaint as a role; parts: [complaint index, bot|reviewer|tenderer|complainer]."""
    patch_complaint(context, step, "tender")


@action("tender_award_complaint_create")
def tender_award_complaint_create(context: Context, step: Step) -> None:
    """Create an award complaint (POST tenders/{id}/awards/{id}/complaints); parts: [award index, complaint index]."""
    create_complaint(context, step, "award")


@action("tender_award_complaint_patch")
def tender_award_complaint_patch(context: Context, step: Step) -> None:
    """Patch an award complaint as a role; parts: [award index, complaint index, bot|reviewer|tenderer|complainer]."""
    patch_complaint(context, step, "award")


@action("tender_qualification_complaint_create")
def tender_qualification_complaint_create(context: Context, step: Step) -> None:
    """Create a qualification complaint (POST tenders/{id}/qualifications/{id}/complaints); parts: [qualification index, complaint index]."""
    create_complaint(context, step, "qualification")


@action("tender_qualification_complaint_patch")
def tender_qualification_complaint_patch(context: Context, step: Step) -> None:
    """Patch a qualification complaint as a role; parts: [qualification index, complaint index, bot|reviewer|tenderer|complainer]."""
    patch_complaint(context, step, "qualification")
