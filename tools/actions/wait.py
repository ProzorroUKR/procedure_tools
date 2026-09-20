"""
Technical actions that wait for the procedure to move on. The data file holds
the parameters, an empty file (or ``{}``) uses the defaults.

    2160_wait_status.json      {"status": ["active.qualification", "active.awarded"], "fail_status": "unsuccessful"}
    2150_wait_next_check.json  {}
    2380_wait_date.json        {"date": "{{ tender.contractPeriod.clarificationsUntil }}", "description": "..."}
"""

import logging

from procedure.actions import wait as wait_until_date
from procedure.actions import (
    wait_auction_participation_urls,
    wait_edr_pre_qual,
    wait_edr_qual,
)
from procedure.actions import wait_status as wait_tender_status
from procedure.procedure import WAIT_EDR_PRE_QUAL, WAIT_EDR_QUAL
from procedure.utils.data import (
    get_complaint_period_end_dates,
    get_data,
    get_next_check,
)
from procedure.utils.handlers import error
from tools.actions.common import (
    ensure_awards,
    refresh_awards,
    refresh_tender,
    skip,
    sleep,
    tender_id,
)
from tools.actions.registry import action


@action("tender_wait_status")
def tender_wait_status(context, step):
    """Wait for a tender status: {"status": "x" or [...], "fail_status": "y" (optional), "delay": seconds (default 1)}."""
    data = context.load(step)
    status = data.get("status")
    if not status:
        error(f'{step.filename}: "status" is required, e.g. {{"status": "active.tendering"}}')
    response = wait_tender_status(
        context.client,
        context.args,
        context,
        tender_id(context),
        delay=data.get("delay", 1),
        status=status,
        fail_status=data.get("fail_status"),
    )
    context["tender"] = get_data(response)


@action("tender_wait_next_check")
def tender_wait_next_check(context, step):
    """Wait for the next chronograph check of the tender (its next_check date), if any."""
    context.load(step)
    response = refresh_tender(context)
    next_check = get_next_check(response)
    if not next_check:
        logging.info("No next check date, nothing to wait for\n")
        return
    wait_until_date(
        next_check,
        client_timedelta=context["client_timedelta"],
        date_info_str="next chronograph check",
    )


@action("wait_date")
def wait_date(context, step):
    """Wait until a date: {"date": "<iso date, templates allowed>", "description": "<optional log text>"}."""
    data = context.load(step)
    date = data.get("date")
    if not date:
        error(f'{step.filename}: "date" is required, e.g. {{"date": "{{{{ tender.tenderPeriod.endDate }}}}"}}')
    wait_until_date(
        date,
        client_timedelta=context["client_timedelta"],
        date_info_str=data.get("description"),
    )


@action("wait_seconds")
def wait_seconds(context, step):
    """Sleep for a number of seconds: {"seconds": 5}."""
    data = context.load(step)
    seconds = data.get("seconds", 0)
    logging.info(f"Waiting {seconds} seconds...\n")
    sleep(seconds)


@action("tender_awards_wait_complaint_period")
def tender_awards_wait_complaint_period(context, step):
    """Wait for the end of the complaint period of all awards."""
    context.load(step)
    refresh_awards(context)
    response = context.client.get(f"tenders/{tender_id(context)}/awards")
    end_dates = get_complaint_period_end_dates(response)
    if not end_dates:
        logging.info("No award complaint periods, nothing to wait for\n")
        return
    wait_until_date(
        max(end_dates),
        client_timedelta=context["client_timedelta"],
        date_info_str="end of award complaint period",
    )


@action("tender_wait_auction")
def tender_wait_auction(context, step):
    """Wait for the auction participation urls of the active bids; skipped for mode:no-auction submissions."""
    context.load(step)
    tender = refresh_tender(context).json()["data"]
    submission_method_details = tender.get("submissionMethodDetails") or ""
    if "mode:no-auction" in submission_method_details:
        skip("Skipping auction: submissionMethodDetails has mode:no-auction")
        return
    if (context.get("tender_config") or {}).get("hasAuction") is False:
        skip("Skipping auction: the tender config has no auction")
        return
    bids = context.get("bids") or []
    tokens = context.get("bids_tokens") or []
    if not bids or not tokens:
        skip("Skipping auction: no bids with tokens in context")
        return
    bids_jsons = [{"data": bid, "access": {"token": token}} for bid, token in zip(bids, tokens) if bid and token]
    wait_auction_participation_urls(context.client, context.args, tender_id(context), bids_jsons)
    ensure_awards(context)


@action("tender_qualifications_wait_edr")
def tender_qualifications_wait_edr(context, step):
    """Wait for the EDR identification documents of the qualifications; runs only with --wait edr-pre-qualification."""
    context.load(step)
    if WAIT_EDR_PRE_QUAL not in (context.args.wait or []):
        skip(f"Skipping EDR wait: pass --wait {WAIT_EDR_PRE_QUAL} to enable")
        return
    wait_edr_pre_qual(context.client, context.args, context, tender_id(context))


@action("tender_awards_wait_edr")
def tender_awards_wait_edr(context, step):
    """Wait for the EDR identification documents of the awards; runs only with --wait edr-qualification."""
    context.load(step)
    if WAIT_EDR_QUAL not in (context.args.wait or []):
        skip(f"Skipping EDR wait: pass --wait {WAIT_EDR_QUAL} to enable")
        return
    wait_edr_qual(context.client, context.args, context, tender_id(context))
