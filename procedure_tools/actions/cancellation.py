"""
Tender and lot cancellations.

    2060_tender_cancellation_create_0.json                 draft cancellation 0 (reason, reasonType, relatedLot)
    2061_tender_cancellation_patch_0.json                  e.g. {"data": {"reasonType": "forceMajeure"}}
    2062_tender_cancellation_0_document_report.p7s         the signed cancellation report
    2063_tender_cancellation_document_attach_0_report.json {"data": {"documentType": "cancellationReport", "title": "..."}}
    2064_tender_cancellation_patch_0.json                  {"data": {"status": "pending"}}
    2065_tender_cancellation_wait_status_0.json            {"status": "active"}: wait for the complaint period to end

Cancellations are stored in ``cancellations[i]``. A pending cancellation becomes
active on its own when its complaint period ends without a satisfied complaint;
a satisfied complaint lets the tender owner switch it to ``unsuccessful``.
"""

import logging
from typing import Any

from procedure_tools.actions import wait as wait_actions
from procedure_tools.actions.common import (
    attach_document,
    refresh_list,
    tender_id,
    tender_token,
)
from procedure_tools.actions.registry import action
from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import get_data
from procedure_tools.utils.handlers import (
    error,
    item_create_success_handler,
    item_patch_success_handler,
)

logger = logging.getLogger(__name__)

POLL_SECONDS = 10


def refresh_cancellations(context: Context) -> list[dict[str, Any]]:
    return refresh_list(
        context, "cancellations", f"tenders/{tender_id(context)}/cancellations", "Checking cancellations..."
    )


def cancellation(context: Context, index: int) -> dict[str, Any]:
    item: dict[str, Any] = context.item("cancellations", index, hint=f"run tender_cancellation_create_{index} first")
    return item


def cancellation_path(context: Context, index: int) -> str:
    return f"tenders/{tender_id(context)}/cancellations/{cancellation(context, index)['id']}"


@action("tender_cancellation_create")
def tender_cancellation_create(context: Context, step: Step) -> None:
    """Create a draft cancellation (POST tenders/{id}/cancellations); parts: [cancellation index]; sets cancellations[i]."""
    index = step.index(0)
    logger.info(f"Creating cancellation {index}...\n")
    data = context.load(step)
    response = context.client.post(
        f"tenders/{tender_id(context)}/cancellations",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_create_success_handler,
    )
    context.set_item("cancellations", index, get_data(response))


@action("tender_cancellation_patch")
def tender_cancellation_patch(context: Context, step: Step) -> None:
    """Patch a cancellation (PATCH tenders/{id}/cancellations/{id}), e.g. to pending or unsuccessful; parts: [cancellation index]."""
    index = step.index(0)
    logger.info(f"Patching cancellation {index}...\n")
    data = context.load(step)
    response = context.client.patch(
        cancellation_path(context, index),
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    context.set_item("cancellations", index, get_data(response))


@action("tender_cancellation_document_attach")
def tender_cancellation_document_attach(context: Context, step: Step) -> None:
    """Attach a document to a cancellation (POST tenders/{id}/cancellations/{id}/documents); parts: [cancellation index, free label]."""
    index = step.index(0)
    logger.info(f"Uploading cancellation {index} document...\n")
    attach_document(
        context,
        step,
        f"{cancellation_path(context, index)}/documents",
        acc_token=tender_token(context),
    )
    refresh_cancellations(context)


@action("tender_cancellations_get")
def tender_cancellations_get(context: Context, step: Step) -> None:
    """Refresh the tender cancellations in context (GET tenders/{id}/cancellations)."""
    context.load(step)
    refresh_cancellations(context)


@action("tender_cancellation_wait_status")
def tender_cancellation_wait_status(context: Context, step: Step) -> None:
    """
    Wait for a cancellation to reach a status: {"status": "active"}; parts: [cancellation index].

    A pending cancellation is waited for until the end of its complaint period, then polled.
    """
    index = step.index(0)
    data = context.load(step)
    status = data.get("status", "active")
    statuses = [status] if isinstance(status, str) else list(status)
    current = cancellation(context, index)
    period_end = (current.get("complaintPeriod") or {}).get("endDate")
    if current.get("status") not in statuses and period_end:
        wait_actions.wait_until_date(
            period_end,
            client_timedelta=context["client_timedelta"],
            date_info_str=f"end of cancellation {index} complaint period",
        )
    logger.info(f"Waiting for cancellation {index} to become {', '.join(statuses)}...\n")
    while True:
        response = context.client.get(cancellation_path(context, index), auth_token=context.args.token)
        current = get_data(response)
        context.set_item("cancellations", index, current)
        if current.get("status") in statuses:
            logger.info(f"Cancellation {index} is {current.get('status')}\n")
            refresh_cancellations(context)
            return
        if current.get("status") in ("unsuccessful", "active") and current.get("status") not in statuses:
            error(f"{step.filename}: cancellation {index} is {current.get('status')}, expected {statuses}")
        wait_actions.sleep(POLL_SECONDS)
