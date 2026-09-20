import logging
from typing import Any

from procedure_tools.actions.common import (
    attach_document,
    bid,
    bid_token,
    ensure_bids,
    tender_id,
    upload_ds,
)
from procedure_tools.actions.registry import action
from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import get_data, get_token
from procedure_tools.utils.handlers import (
    bid_create_success_handler,
    item_patch_success_handler,
)

logger = logging.getLogger(__name__)


BID_DOCUMENT_CONTAINERS = (
    "documents",
    "eligibilityDocuments",
    "financialDocuments",
    "qualificationDocuments",
)


def refresh_bid(context: Context, index: int) -> dict[str, Any]:
    response = context.client.get(
        f"tenders/{tender_id(context)}/bids/{bid(context, index)['id']}",
        acc_token=bid_token(context, index),
        auth_token=context.args.token,
    )
    item: dict[str, Any] = context.set_item("bids", index, get_data(response))
    return item


@action("tender_bid_create")
def tender_bid_create(context: Context, step: Step) -> None:
    """Create a bid (POST tenders/{id}/bids), uploading the documents listed in it; parts: [bid index]; sets bids[i], bids_tokens[i]."""
    logger.info("Creating bid...\n")
    index = step.index(0)
    data = context.load(step)
    for container in BID_DOCUMENT_CONTAINERS:
        documents = []
        for document in data["data"].get(container, []):
            ds_response = upload_ds(context, document.pop("file", None) or document["title"], title=document["title"])
            document_data = ds_response.json()["data"]
            document_data.update(document)
            documents.append(document_data)
        if documents:
            data["data"][container] = documents
    response = context.client.post(
        f"tenders/{tender_id(context)}/bids",
        json=data,
        auth_token=context.args.token,
        success_handler=bid_create_success_handler,
    )
    context.set_item("bids", index, get_data(response))
    context.set_item("bids_tokens", index, get_token(response))


@action("tender_bid_patch")
def tender_bid_patch(context: Context, step: Step) -> None:
    """Patch a bid (PATCH tenders/{id}/bids/{id}); parts: [bid index]."""
    logger.info("Patching bid...\n")
    index = step.index(0)
    data = context.load(step)
    response = context.client.patch(
        f"tenders/{tender_id(context)}/bids/{bid(context, index)['id']}",
        json=data,
        acc_token=bid_token(context, index),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    context.set_item("bids", index, get_data(response))


@action("tender_bid_document_attach")
def tender_bid_document_attach(context: Context, step: Step) -> None:
    """Attach a document to a bid (POST tenders/{id}/bids/{id}/documents); parts: [bid index, free label]."""
    logger.info("Uploading bid document...\n")
    index = step.index(0)
    attach_document(
        context,
        step,
        f"tenders/{tender_id(context)}/bids/{bid(context, index)['id']}/documents",
        acc_token=bid_token(context, index),
    )
    refresh_bid(context, index)


@action("tender_bid_res_post")
def tender_bid_res_post(context: Context, step: Step) -> None:
    """Post bid requirement responses (POST tenders/{id}/bids/{id}/requirement_responses); parts: [bid index]."""
    logger.info("Posting bid requirement responses...\n")
    index = step.index(0)
    data = context.load(step)
    bid_documents = bid(context, index).get("documents") or []
    for bid_res in data["data"]:
        for evidence in bid_res.get("evidences", []):
            if evidence["type"] == "document" and bid_documents:
                related_document = evidence["relatedDocument"]
                related_document["id"] = bid_documents[0]["id"]
                related_document["title"] = bid_documents[0]["title"]
    context.client.post(
        f"tenders/{tender_id(context)}/bids/{bid(context, index)['id']}/requirement_responses",
        json=data,
        acc_token=bid_token(context, index),
        auth_token=context.args.token,
    )
    refresh_bid(context, index)


@action("tender_bids_get")
def tender_bids_get(context: Context, step: Step) -> None:
    """Load the tender bids into context (GET tenders/{id}/bids) when they were not created in this run."""
    context.load(step)
    context.pop("bids", None)
    ensure_bids(context)
