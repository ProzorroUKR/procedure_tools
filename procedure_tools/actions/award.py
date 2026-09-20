import logging

from procedure_tools.actions.common import (
    attach_document,
    award,
    refresh_awards,
    tender_id,
    tender_token,
)
from procedure_tools.actions.registry import action
from procedure_tools.utils.handlers import (
    allow_null_success_handler,
    item_create_success_handler,
    item_patch_success_handler,
)

logger = logging.getLogger(__name__)


@action("tender_award_create")
def tender_award_create(context, step):
    """Create an award (POST tenders/{id}/awards) in limited procedures; parts are a free label."""
    logger.info("Creating award...\n")
    data = context.load(step)
    context.client.post(
        f"tenders/{tender_id(context)}/awards",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=item_create_success_handler,
    )
    refresh_awards(context)


@action("tender_award_patch")
def tender_award_patch(context, step):
    """Patch an award (PATCH tenders/{id}/awards/{id}); parts: [award index]; refreshes awards."""
    logger.info("Patching award...\n")
    index = step.index(0)
    data = context.load(step)
    context.client.patch(
        f"tenders/{tender_id(context)}/awards/{award(context, index)['id']}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=allow_null_success_handler(item_patch_success_handler),
    )
    refresh_awards(context)


@action("tender_award_document_attach")
def tender_award_document_attach(context, step):
    """Attach a document to an award (POST tenders/{id}/awards/{id}/documents); parts: [award index, free label]."""
    logger.info("Uploading award document...\n")
    index = step.index(0)
    attach_document(
        context,
        step,
        f"tenders/{tender_id(context)}/awards/{award(context, index)['id']}/documents",
        acc_token=tender_token(context),
    )
    refresh_awards(context)


@action("tender_awards_get")
def tender_awards_get(context, step):
    """Refresh the tender awards in context (GET tenders/{id}/awards)."""
    context.load(step)
    refresh_awards(context)
