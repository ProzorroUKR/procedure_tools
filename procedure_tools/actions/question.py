"""
Tender questions (enquiries).

    2030_tender_question_create_0.json    question 0, asked by the broker during the enquiry period
    2031_tender_question_patch_0.json     answered by the tender owner (``{"data": {"answer": "..."}}``)

Questions are stored in ``questions``; a data file can point a question at a lot
or an item with ``questionOf`` and ``relatedItem``, e.g. ``{{ tender.lots[0].id }}``.
"""

import logging
from typing import Any

from procedure_tools.actions.common import skip, tender_id, tender_token
from procedure_tools.actions.registry import action
from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import get_data
from procedure_tools.utils.handlers import question_success_handler

logger = logging.getLogger(__name__)


def questions_disabled(context: Context) -> bool:
    """True when --disable-questions / DISABLE_QUESTIONS is set."""
    return bool(getattr(context.args, "disable_questions", False))


def question(context: Context, index: int) -> dict[str, Any]:
    item: dict[str, Any] = context.item("questions", index, hint=f"run tender_question_create_{index} first")
    return item


@action("tender_question_create")
def tender_question_create(context: Context, step: Step) -> None:
    """Ask a tender question (POST tenders/{id}/questions); parts: [question index]; sets questions[i]."""
    index = step.index(0)
    if questions_disabled(context):
        skip(f"Skipping question {index}: questions are disabled")
        return
    logger.info(f"Creating question {index}...\n")
    data = context.load(step)
    response = context.client.post(
        f"tenders/{tender_id(context)}/questions",
        json=data,
        auth_token=context.args.token,
        success_handler=question_success_handler,
    )
    context.set_item("questions", index, get_data(response))


@action("tender_question_patch")
def tender_question_patch(context: Context, step: Step) -> None:
    """Answer a tender question (PATCH tenders/{id}/questions/{id}) as the tender owner; parts: [question index]."""
    index = step.index(0)
    if questions_disabled(context):
        skip(f"Skipping question {index} answer: questions are disabled")
        return
    logger.info(f"Answering question {index}...\n")
    data = context.load(step)
    response = context.client.patch(
        f"tenders/{tender_id(context)}/questions/{question(context, index)['id']}",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=question_success_handler,
    )
    context.set_item("questions", index, get_data(response))
