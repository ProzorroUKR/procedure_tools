import logging

from tools.actions.common import attach_document, get_until, has_data
from tools.actions.registry import action
from tools.utils.data import get_data, get_token
from tools.utils.handlers import (
    error,
    framework_create_success_handler,
    framework_get_success_handler,
    framework_patch_success_handler,
    item_patch_success_handler,
    submission_create_success_handler,
)


def framework_id(context):
    return context.require("framework", "run framework_create first")["id"]


def framework_token(context):
    return context.require("framework_token", "run framework_create first")


def submission(context, index):
    return context.item("submissions", index, hint=f"run framework_submission_create_{index} first")


def framework_qualification(context, index):
    """Framework qualification created by the activation of submission ``index``."""
    qualifications = context.get("framework_qualifications") or []
    if index < len(qualifications) and qualifications[index]:
        return qualifications[index]
    qualification_id = submission(context, index).get("qualificationID")
    if not qualification_id:
        error(f"{context.step.filename}: submission {index} has no qualificationID yet, activate it first")
    response = get_until(
        context,
        f"qualifications/{qualification_id}",
        has_data,
        info="Check qualification...",
        auth_token=context.args.token,
    )
    return context.set_item("framework_qualifications", index, get_data(response))


@action("framework_create")
def framework_create(context, step):
    """Create a framework (POST frameworks); sets framework, framework_token."""
    logging.info("Creating framework...\n")
    data = context.load(step)
    response = context.client.post(
        "frameworks",
        json=data,
        auth_token=context.args.token,
        success_handler=framework_create_success_handler,
    )
    context["framework"] = get_data(response)
    context["framework_token"] = get_token(response)


@action("framework_patch")
def framework_patch(context, step):
    """Patch the framework (PATCH frameworks/{id}), for example to activate it."""
    logging.info("Patching framework...\n")
    data = context.load(step)
    response = context.client.patch(
        f"frameworks/{framework_id(context)}",
        json=data,
        acc_token=framework_token(context),
        auth_token=context.args.token,
        success_handler=framework_patch_success_handler,
    )
    context["framework"] = get_data(response)


@action("framework_get")
def framework_get(context, step):
    """Refresh the framework in context (GET frameworks/{id})."""
    context.load(step)
    response = context.client.get(
        f"frameworks/{framework_id(context)}",
        success_handler=framework_get_success_handler,
    )
    context["framework"] = get_data(response)


@action("framework_submission_create")
def framework_submission_create(context, step):
    """Create a submission (POST submissions); parts: [submission index]; sets submissions[i], submissions_tokens[i]."""
    logging.info("Creating submission...\n")
    index = step.index(0)
    data = context.load(step)
    response = context.client.post(
        "submissions",
        json=data,
        auth_token=context.args.token,
        success_handler=submission_create_success_handler,
    )
    context.set_item("submissions", index, get_data(response))
    context.set_item("submissions_tokens", index, get_token(response))


@action("framework_submission_patch")
def framework_submission_patch(context, step):
    """Patch a submission (PATCH submissions/{id}); parts: [submission index]."""
    logging.info("Patching submission...\n")
    index = step.index(0)
    data = context.load(step)
    response = context.client.patch(
        f"submissions/{submission(context, index)['id']}",
        json=data,
        acc_token=context.item("submissions_tokens", index),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    context.set_item("submissions", index, get_data(response))


@action("framework_qualification_document_attach")
def framework_qualification_document_attach(context, step):
    """Attach a document to a framework qualification (POST qualifications/{id}/documents); parts: [submission index]."""
    logging.info("Uploading qualification document...\n")
    index = step.index(0)
    qualification = framework_qualification(context, index)
    attach_document(
        context,
        step,
        f"qualifications/{qualification['id']}/documents",
        acc_token=framework_token(context),
    )


@action("framework_qualification_patch")
def framework_qualification_patch(context, step):
    """Patch a framework qualification (PATCH qualifications/{id}); parts: [submission index]."""
    logging.info("Patching qualification...\n")
    index = step.index(0)
    qualification = framework_qualification(context, index)
    data = context.load(step)
    response = context.client.patch(
        f"qualifications/{qualification['id']}",
        json=data,
        acc_token=framework_token(context),
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    context.set_item("framework_qualifications", index, get_data(response))
