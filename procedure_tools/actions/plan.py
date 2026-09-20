import logging
from typing import Any

from procedure_tools.actions.registry import action
from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import get_data, get_token
from procedure_tools.utils.handlers import (
    plan_create_success_handler,
    plan_patch_success_handler,
)

logger = logging.getLogger(__name__)


def plan_ref(context: Context, step: Step) -> tuple[int, dict[str, Any], str]:
    """(index, plan, token) of the plan the step refers to: part #1 or the last created plan."""
    plans = context.get("plans") or []
    index = step.index(0, default=len(plans) - 1)
    plan = context.item("plans", index, hint="run plan_create first")
    token = context.item("plans_tokens", index, hint="run plan_create first")
    return index, plan, token


def store_plan(context: Context, index: int, plan: dict[str, Any]) -> None:
    context.set_item("plans", index, plan)
    if index == len(context["plans"]) - 1:
        context["plan"] = plan


@action("plan_create")
def plan_create(context: Context, step: Step) -> None:
    """Create a plan (POST plans); sets plan, plan_token and appends to plans, plans_tokens."""
    logger.info("Creating plan...\n")
    data = context.load(step)
    response = context.client.post(
        "plans",
        json=data,
        auth_token=context.args.token,
        success_handler=plan_create_success_handler,
    )
    plans = context.setdefault("plans", [])
    index = len(plans)
    context.set_item("plans_tokens", index, get_token(response))
    store_plan(context, index, get_data(response))
    context["plan_token"] = get_token(response)


@action("plan_patch")
def plan_patch(context: Context, step: Step) -> None:
    """Patch a plan (PATCH plans/{id}); parts: [plan index] (default: the last created plan)."""
    logger.info("Patching plan...\n")
    index, plan, token = plan_ref(context, step)
    data = context.load(step)
    response = context.client.patch(
        f"plans/{plan['id']}",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=plan_patch_success_handler,
    )
    store_plan(context, index, get_data(response))
