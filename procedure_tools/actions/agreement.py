import logging

from procedure_tools.actions.common import (
    attach_document,
    ensure_agreements,
    ensure_bids,
    get_until,
    has_data,
    refresh_agreements,
    sleep,
    tender_id,
    tender_token,
)
from procedure_tools.actions.registry import action
from procedure_tools.utils.data import get_data
from procedure_tools.utils.handlers import (
    default_success_handler,
    error,
    item_patch_success_handler,
)


def framework_agreement_id(context):
    """Agreement id of the framework in context, waiting until the framework has one."""
    framework_id = context["framework"]["id"]
    logging.info("Waiting for the framework agreement...\n")
    while True:
        response = context.client.get(f"frameworks/{framework_id}")
        context["framework"] = get_data(response)
        agreement_id = context["framework"].get("agreementID")
        if agreement_id:
            return agreement_id
        sleep(1)


def agreement(context, index):
    ensure_agreements(context)
    return context.item("agreements", index)


@action("agreement_get")
def agreement_get(context, step):
    """Load the agreement (GET agreements/{id}) of the framework, or the last agreement of the tender, into agreement."""
    data = context.load(step)
    agreement_id = data.get("data", {}).get("id")
    if not agreement_id and context.get("framework"):
        agreement_id = framework_agreement_id(context)
    if not agreement_id and context.get("tender"):
        response = context.client.get(f"tenders/{tender_id(context)}")
        context["tender"] = get_data(response)
        agreements = context["tender"].get("agreements") or []
        if agreements:
            agreement_id = agreements[-1]["id"]
    if not agreement_id:
        error(f"{step.filename}: no agreement to load, create a framework or a tender with agreements first")
    response = get_until(
        context,
        f"agreements/{agreement_id}",
        has_data,
        info="Check agreement...",
        auth_token=context.args.token,
        error_handler=default_success_handler,
    )
    context["agreement"] = get_data(response)


@action("tender_agreements_get")
def tender_agreements_get(context, step):
    """Refresh the tender agreements in context (GET tenders/{id}/agreements)."""
    context.load(step)
    refresh_agreements(context)


@action("tender_agreement_patch")
def tender_agreement_patch(context, step):
    """Patch a tender agreement (PATCH tenders/{id}/agreements/{id}); parts: [agreement index]."""
    logging.info("Patching agreement...\n")
    index = step.index(0)
    data = context.load(step)
    context.client.patch(
        f"tenders/{tender_id(context)}/agreements/{agreement(context, index)['id']}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    refresh_agreements(context)


@action("tender_agreement_document_attach")
def tender_agreement_document_attach(context, step):
    """Attach a document to a tender agreement (POST tenders/{id}/agreements/{id}/documents); parts: [agreement index]."""
    logging.info("Uploading agreement document...\n")
    index = step.index(0)
    attach_document(
        context,
        step,
        f"tenders/{tender_id(context)}/agreements/{agreement(context, index)['id']}/documents",
        acc_token=tender_token(context),
    )
    refresh_agreements(context)


@action("tender_agreement_contract_patch")
def tender_agreement_contract_patch(context, step):
    """Patch the agreement contract of a bid (PATCH tenders/{id}/agreements/{id}/contracts/{id}); parts: [agreement index, bid index]."""
    logging.info("Patching agreement contract...\n")
    agreement_index = step.index(0)
    bid_index = step.index(1)
    agreement_data = agreement(context, agreement_index)
    bid_id = ensure_bids(context)[bid_index]["id"]
    path = f"tenders/{tender_id(context)}/agreements/{agreement_data['id']}/contracts"
    response = get_until(context, path, info="Checking agreement contracts...")
    contracts = [item for item in response.json()["data"] if item.get("bidID") == bid_id]
    if not contracts:
        error(f"{step.filename}: agreement {agreement_index} has no contract for bid {bid_index}")
    data = context.load(step)
    context.client.patch(
        f"{path}/{contracts[0]['id']}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    refresh_agreements(context)
