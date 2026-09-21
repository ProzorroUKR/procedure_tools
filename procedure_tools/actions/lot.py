"""
Lot actions.

Lots can be added to, changed in and removed from a tender while it is still
being prepared. They matter beyond that too: what blocks a lot, and what a
block on one lot does to the others, is a rule worth exercising.
"""

import logging
from typing import Any

from procedure_tools.actions.common import refresh_tender, tender_id, tender_token
from procedure_tools.actions.registry import action
from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import get_data
from procedure_tools.utils.handlers import (
    default_success_handler,
    item_create_success_handler,
    item_patch_success_handler,
)

logger = logging.getLogger(__name__)


def lot(context: Context, index: int) -> dict[str, Any]:
    """The lot at ``index`` of the tender in context."""
    lots = (context.get("tender") or {}).get("lots") or []
    if index >= len(lots):
        raise IndexError(f"the tender has no lot {index}")
    item: dict[str, Any] = lots[index]
    return item


@action("tender_lot_create")
def tender_lot_create(context: Context, step: Step) -> None:
    """Add a lot to the tender (POST tenders/{id}/lots); refreshes the tender."""
    logger.info("Creating lot...\n")
    data = context.load(step)
    response = context.client.post(
        f"tenders/{tender_id(context)}/lots",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_create_success_handler,
    )
    context["lot"] = get_data(response)
    refresh_tender(context)


@action("tender_lot_patch")
def tender_lot_patch(context: Context, step: Step) -> None:
    """Patch a lot (PATCH tenders/{id}/lots/{id}); parts: [lot index]."""
    index = step.index(0)
    logger.info(f"Patching lot {index}...\n")
    data = context.load(step)
    response = context.client.patch(
        f"tenders/{tender_id(context)}/lots/{lot(context, index)['id']}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    context["lot"] = get_data(response)
    refresh_tender(context)


@action("tender_lot_delete")
def tender_lot_delete(context: Context, step: Step) -> None:
    """Remove a lot from the tender (DELETE tenders/{id}/lots/{id}); parts: [lot index]."""
    index = step.index(0)
    logger.info(f"Deleting lot {index}...\n")
    context.load(step)
    context.client.delete(
        f"tenders/{tender_id(context)}/lots/{lot(context, index)['id']}",
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=default_success_handler,
    )
    refresh_tender(context)
