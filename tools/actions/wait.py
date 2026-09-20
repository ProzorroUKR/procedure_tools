"""
Technical actions that wait for the procedure to move on. The data file holds
the parameters, an empty file (or ``{}``) uses the defaults.

    2620_tender_wait_status.json      {"status": ["active.qualification", "active.awarded"], "fail_status": "unsuccessful"}
    2230_tender_wait_next_check.json  {}
    3300_wait_date.json               {"date": "{{ tender.contractPeriod.clarificationsUntil }}", "description": "..."}
"""

import logging
import math
from datetime import timedelta
from functools import partial

from tools.actions.common import (
    ensure_awards,
    refresh_awards,
    refresh_qualifications,
    refresh_tender,
    skip,
    sleep,
    tender_id,
)
from tools.actions.registry import action
from tools.utils.data import (
    EDR_FILENAME,
    SECONDS_BUFFER,
    WAIT_EDR_PRE_QUAL,
    WAIT_EDR_QUAL,
    get_complaint_period_end_dates,
    get_data,
    get_next_check,
)
from tools.utils.date import fix_datetime, get_utcnow, parse_date
from tools.utils.handlers import (
    auction_multilot_participation_url_success_handler,
    auction_participation_url_success_handler,
    error,
    response_handler,
    tender_check_status_invalid_handler,
    tender_check_status_success_handler,
)
from tools.utils.runtime import get_controller

# --- waiting primitives


def wait_until_date(date_str, client_timedelta=timedelta(), date_info_str=None):
    now = fix_datetime(get_utcnow(), client_timedelta)
    delta_seconds = (parse_date(date_str) - now).total_seconds()
    date_seconds = math.ceil(delta_seconds) if delta_seconds > 0 else 0
    info_str = f" for {date_info_str}" if date_info_str else ""
    logging.info(f"Waiting {date_seconds} seconds{info_str} - {date_str}...\n")
    controller = get_controller()
    if controller:
        controller.set_activity(None, f"waiting {date_seconds}s")
    sleep(date_seconds)


def wait_tender_status(client, args, context, tender_id, delay, status, fail_status=None):
    logging.info(f"Waiting for {status}...\n")
    status = [status] if not isinstance(status, list) else status
    fail_status = [fail_status] if fail_status and not isinstance(fail_status, list) else fail_status
    controller = get_controller()
    if controller:
        controller.set_activity(None, f"waiting for {', '.join(status)}")
    while True:
        response = client.get(f"tenders/{tender_id}")
        current_status = response.json()["data"]["status"]
        if current_status in status:
            response_handler(response, success_handler=tender_check_status_success_handler)
            return response
        if fail_status and current_status in fail_status:
            response_handler(response, success_handler=tender_check_status_invalid_handler)
            error("Terminated.")
        sleep(delay)


def wait_auction_participation_urls(client, args, tender_id, bids):
    logging.info("Waiting for the auction participation urls...\n")
    active_bids = [bid for bid in bids if bid["data"].get("status") != "unsuccessful"]
    active_bids_ids = [bid["data"]["id"] for bid in active_bids]
    success_bids_ids = []
    while True:
        tender_data = client.get(f"tenders/{tender_id}").json()["data"]
        if set(success_bids_ids) == set(active_bids_ids):
            break
        for bid in active_bids:
            bid_id = bid["data"]["id"]
            if bid_id in success_bids_ids:
                continue
            response = client.get(
                f"tenders/{tender_id}/bids/{bid_id}",
                acc_token=bid["access"]["token"],
                auth_token=args.token,
            )
            data = response.json()["data"]
            if "lotValues" in data:
                lots_with_auction = {lot["id"] for lot in tender_data.get("lots", []) if "auctionPeriod" in lot}
                active_lot_values = [
                    value
                    for value in data["lotValues"]
                    if value.get("status", "active") in ("pending", "active")
                    and value["relatedLot"] in lots_with_auction
                ]
                if all("participationUrl" in value for value in active_lot_values):
                    response_handler(
                        response,
                        success_handler=partial(auction_multilot_participation_url_success_handler),
                    )
                    success_bids_ids.append(bid_id)
            elif "participationUrl" in data:
                response_handler(response, success_handler=auction_participation_url_success_handler)
                success_bids_ids.append(bid_id)
        sleep(SECONDS_BUFFER)


def wait_edr_documents(context, path, items):
    """Wait until every item (award or qualification) has the EDR identification document."""
    logging.info(f"Waiting for {EDR_FILENAME} in {path} documents...\n")
    for item in items:
        while EDR_FILENAME not in [doc["title"] for doc in item.get("documents", [])]:
            sleep(SECONDS_BUFFER)
            item = context.client.get(f"tenders/{tender_id(context)}/{path}/{item['id']}").json()["data"]


# --- actions


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
    wait_edr_documents(context, "qualifications", refresh_qualifications(context))


@action("tender_awards_wait_edr")
def tender_awards_wait_edr(context, step):
    """Wait for the EDR identification documents of the awards; runs only with --wait edr-qualification."""
    context.load(step)
    if WAIT_EDR_QUAL not in (context.args.wait or []):
        skip(f"Skipping EDR wait: pass --wait {WAIT_EDR_QUAL} to enable")
        return
    wait_edr_documents(context, "awards", refresh_awards(context))
