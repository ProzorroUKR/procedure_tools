"""
Technical actions that change the run itself instead of calling the API.
"""

import logging
import threading

from procedure_tools.actions.registry import action
from procedure_tools.utils.handlers import EX_OK, error
from procedure_tools.utils.runtime import get_controller

logger = logging.getLogger(__name__)


_pause_lock = threading.Lock()

TRUE_VALUES = ("true", "1", "yes", "on")


def is_true(value):
    if isinstance(value, str):
        return value.strip().lower() in TRUE_VALUES
    return bool(value)


@action("stop_if")
def stop_if(context, step):
    """Stop the run successfully when a condition holds: {"condition": "{{ constants.SIGNATURE_VERIFICATION_ENABLED }}", "message": "..."}."""
    data = context.load(step)
    if not is_true(data.get("condition")):
        return
    message = data.get("message") or f"{step.filename}: condition is true"
    logger.info(f"{message}, cannot continue...\n")
    raise SystemExit(EX_OK)


@action("skip_if")
def skip_if(context, step):
    """Skip the next steps when a condition holds: {"condition": "{{ tender.status != 'active.pre-qualification' }}", "steps": 2}."""
    data = context.load(step)
    steps = int(data.get("steps", 1))
    if not is_true(data.get("condition")):
        return
    message = data.get("message") or f"{step.filename}: condition is true"
    logger.info(f"{message}, skipping the next {steps} step(s)\n")
    context.skip_steps = steps


@action("context_set")
def context_set(context, step):
    """Merge the data file into the context: {"my_value": "{{ tender.id }}"}."""
    data = context.load(step)
    if not isinstance(data, dict):
        error(f"{step.filename}: context_set expects a JSON object")
    context.update(data)
    logger.info(f"Context updated: {', '.join(sorted(data))}\n")


@action("context_rename")
def context_rename(context, step):
    """Rename context keys, e.g. before a new stage: {"tender": "stage1_tender", "tender_token": "stage1_tender_token"}."""
    data = context.load(step)
    for old_key, new_key in data.items():
        if old_key in context:
            context[new_key] = context.pop(old_key)
    logger.info(f"Context keys renamed: {', '.join(f'{old} -> {new}' for old, new in data.items())}\n")


@action("context_delete")
def context_delete(context, step):
    """Delete context keys: {"keys": ["awards", "contracts"]}."""
    data = context.load(step)
    keys = data.get("keys") or []
    for key in keys:
        context.pop(key, None)
    logger.info(f"Context keys deleted: {', '.join(keys)}\n")


@action("pause")
def pause(context, step):
    """Pause until Enter is pressed: {"message": "<optional prompt>"}."""
    data = context.load(step)
    prompt = data.get("message") or "Press Enter key to continue..."
    controller = get_controller()
    with _pause_lock:
        if controller:
            controller.wait_for_enter(prompt)
        else:
            input(prompt)
