import logging

from procedure.utils.handlers import item_patch_success_handler
from tools.actions.common import (
    attach_document,
    qualification,
    refresh_qualifications,
    tender_id,
    tender_token,
)
from tools.actions.registry import action


@action("tender_qualification_patch")
def tender_qualification_patch(context, step):
    """Patch a tender qualification (PATCH tenders/{id}/qualifications/{id}); parts: [qualification index]."""
    logging.info("Patching qualification...\n")
    index = step.index(0)
    data = context.load(step)
    context.client.patch(
        f"tenders/{tender_id(context)}/qualifications/{qualification(context, index)['id']}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    refresh_qualifications(context)


@action("tender_qualification_document_attach")
def tender_qualification_document_attach(context, step):
    """Attach a document to a tender qualification (POST tenders/{id}/qualifications/{id}/documents); parts: [qualification index]."""
    logging.info("Uploading qualification document...\n")
    index = step.index(0)
    attach_document(
        context,
        step,
        f"tenders/{tender_id(context)}/qualifications/{qualification(context, index)['id']}/documents",
        acc_token=tender_token(context),
    )
    refresh_qualifications(context)


@action("tender_qualifications_get")
def tender_qualifications_get(context, step):
    """Refresh the tender qualifications in context (GET tenders/{id}/qualifications)."""
    context.load(step)
    refresh_qualifications(context)
