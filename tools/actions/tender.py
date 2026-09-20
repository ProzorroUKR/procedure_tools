import logging

from procedure.utils.data import get_data
from procedure.utils.handlers import (
    error,
    tender_create_success_handler,
    tender_patch_success_handler,
    tender_post_criteria_success_handler,
    tender_post_plan_success_handler,
)
from tools.actions.common import (
    attach_document,
    refresh_tender,
    set_tender,
    tender_id,
    tender_token,
)
from tools.actions.registry import action


@action("tender_create")
def tender_create(context, step):
    """Create a tender (POST tenders, or POST plans/{id}/tenders when a plan is in context); sets tender, tender_token, tender_config."""
    logging.info("Creating tender...\n")
    data = context.load(step)
    plan = context.get("plan")
    path = f"plans/{plan['id']}/tenders" if plan else "tenders"
    response = context.client.post(
        path,
        json=data,
        auth_token=context.args.token,
        success_handler=tender_create_success_handler,
    )
    set_tender(context, response)
    context["tender_documents"] = []


@action("tender_patch")
def tender_patch(context, step):
    """Patch the tender (PATCH tenders/{id}), for example to switch its status."""
    logging.info("Patching tender...\n")
    data = context.load(step)
    response = context.client.patch(
        f"tenders/{tender_id(context)}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=tender_patch_success_handler,
    )
    context["tender"] = get_data(response)


@action("tender_get")
def tender_get(context, step):
    """Refresh the tender in context (GET tenders/{id})."""
    context.load(step)
    refresh_tender(context)


@action("tender_document_attach")
def tender_document_attach(context, step):
    """Attach a document to the tender (POST tenders/{id}/documents); parts are a free label; appends to tender_documents."""
    logging.info("Uploading tender document...\n")
    response = attach_document(
        context,
        step,
        f"tenders/{tender_id(context)}/documents",
        acc_token=tender_token(context),
    )
    context.setdefault("tender_documents", []).append(get_data(response))


@action("tender_document_put")
def tender_document_put(context, step):
    """Replace a tender document with a new version (PUT tenders/{id}/documents/{id}); parts: [tender_documents index] or a label, then the last attached document with the same title is replaced."""
    logging.info("Re-uploading tender document...\n")
    data = context.load(step)
    documents = context.get("tender_documents") or []
    part = step.part(0)
    if part is not None and part.isdigit():
        index = int(part)
        context.item("tender_documents", index, hint="run tender_document_attach first")
    else:
        title = data["data"]["title"]
        matches = [i for i, document in enumerate(documents) if document and document.get("title") == title]
        if not matches:
            error(f"{step.filename}: no tender document titled {title!r} was attached in this run")
        index = matches[-1]
    response = attach_document(
        context,
        step,
        f"tenders/{tender_id(context)}/documents/{documents[index]['id']}",
        acc_token=tender_token(context),
        method="put",
        data=data,
    )
    context["tender_documents"][index] = get_data(response)


@action("tender_criteria_post")
def tender_criteria_post(context, step):
    """Create tender criteria (POST tenders/{id}/criteria); sets criteria."""
    logging.info("Creating tender criteria...\n")
    data = context.load(step)
    response = context.client.post(
        f"tenders/{tender_id(context)}/criteria",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=tender_post_criteria_success_handler,
    )
    context["criteria"] = get_data(response)


@action("tender_plan_post")
def tender_plan_post(context, step):
    """Connect a plan to the tender (POST tenders/{id}/plans); the data file holds the plan id, e.g. {{ plans[1].id }}."""
    logging.info("Connecting plan to tender...\n")
    data = context.load(step)
    context.client.post(
        f"tenders/{tender_id(context)}/plans",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=tender_post_plan_success_handler,
    )
    refresh_tender(context)


@action("tender_credentials_patch")
def tender_credentials_patch(context, step):
    """Take over the second stage tender (PATCH tenders/{stage2TenderID}/credentials); the previous tender moves to stage1_tender."""
    logging.info("Getting credentials for second stage...\n")
    stage2_tender_id = context.require("tender").get("stage2TenderID")
    if not stage2_tender_id:
        error(f"{step.filename}: the tender has no stage2TenderID yet")
    data = context.load(step)
    response = context.client.patch(
        f"tenders/{stage2_tender_id}/credentials",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=tender_create_success_handler,
    )
    context["stage1_tender"] = context["tender"]
    context["stage1_tender_token"] = context["tender_token"]
    set_tender(context, response)
    # the credentials response has no config, fetch the full tender
    response = context.client.get(f"tenders/{stage2_tender_id}")
    set_tender(context, response)
    context["tender_documents"] = []
