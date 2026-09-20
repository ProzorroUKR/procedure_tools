import argparse
import logging
import threading
from collections.abc import Collection
from typing import Any

import requests

from procedure_tools.actions import ACTIONS
from procedure_tools.client import CDBClient, DSClient
from procedure_tools.context import Context
from procedure_tools.steps import Step, StepError, discover_steps
from procedure_tools.utils.file import get_data_path
from procedure_tools.utils.handlers import EX_DATAERR, EX_OK, ProcedureExit, RequestFailed, error
from procedure_tools.utils.runtime import get_controller

logger = logging.getLogger(__name__)


_pause_lock = threading.Lock()


def load_steps(data_path: str) -> list[Step] | None:
    try:
        return discover_steps(data_path, ACTIONS)
    except StepError as e:
        error(str(e))
        return None


def build_clients(args: argparse.Namespace, session: requests.Session | None = None) -> tuple[CDBClient, DSClient]:
    client = CDBClient(
        args.host,
        args.token,
        args.path,
        session=session,
        debug_request=args.debug_request,
        debug_json_level=args.debug_json_level,
        debug=args.debug,
    )
    ds_client = DSClient(
        args.ds_host,
        args.ds_username,
        args.ds_password,
        session=session,
        debug_request=args.debug_request,
        debug_json_level=args.debug_json_level,
        debug=args.debug,
    )
    return client, ds_client


def build_context(
    args: argparse.Namespace,
    data_path: str | None = None,
    steps: list[Step] | None = None,
    session: requests.Session | None = None,
) -> Context:
    """
    Connect to the API and build the context the actions share.

    ``data_path`` and ``steps`` are what the data folder run fills in; a caller
    that drives the actions itself (see ``run_action``) leaves them out.
    """
    client, ds_client = build_clients(args, session=session)
    context = Context(args, client, ds_client, data_path, steps or [])
    context["acceleration"] = args.acceleration
    context["submission"] = args.submission
    context["client_timedelta"] = client.client_timedelta
    context["constants"] = client.get("constants", auth_token=args.token).json()
    return context


def run_action(
    context: Context,
    action: str,
    parts: Collection[str] | None = None,
    data: dict[str, Any] | list[Any] | None = None,
) -> Step:
    """
    Run a single action with the data passed in instead of a data file.

    This is the entry point for callers that build the payloads themselves, the
    Robot Framework keywords in ``robot_tests`` for example.
    """
    if action not in ACTIONS:
        error(f"Unknown action {action!r}")
    step = Step.inline(action, parts, data)
    context.step = step
    logger.info(f"Running {step.stem}\n")
    ACTIONS[action](context, step)
    return step


def process_tools(args: argparse.Namespace, session: requests.Session | None = None) -> Context:
    """
    Run the data folder: discover the steps from the file names and execute
    them one by one. There is no procedure specific logic here, the data files
    define the flow.
    """
    data_path = get_data_path(args.data)
    if data_path is None:
        raise ProcedureExit(EX_DATAERR, f"Data path not found: {args.data}")
    steps = load_steps(data_path) or []
    if not steps:
        error(f"No action files found in {data_path}")
    logger.info(f"Discovered {len(steps)} steps in {data_path}\n")

    context = build_context(args, data_path=data_path, steps=steps, session=session)

    for position, step in enumerate(steps, start=1):
        run_step(context, step, position)
    return context


def run_step(context: Context, step: Step, position: int) -> None:
    controller = get_controller()
    if controller:
        controller.check_pause()
        controller.set_activity(None, step.filename)

    if context.skip_steps > 0:
        context.skip_steps -= 1
        logger.info(f"Step {position}/{len(context.steps)}: {step.filename} (skipped)\n")
        return

    logger.info(f"Step {position}/{len(context.steps)}: {step.filename}\n")
    context.step = step
    if context.allow_fail_next:
        context.allow_fail_next = False
        context.client.allow_fail = True
    try:
        ACTIONS[step.action](context, step)
    except RequestFailed as e:
        logger.info(f"Step {step.filename} failed as allowed: {e}\n")
    finally:
        if context.client.allow_fail:
            logger.info(f"Step {step.filename} made no request, allow_fail had no effect\n")
            context.client.allow_fail = False

    args = context.args
    if step.matches(args.stop):
        logger.info(f"Stopping after {step.filename}\n")
        raise SystemExit(EX_OK)
    if args.pause and any(step.matches(filename) for filename in args.pause):
        with _pause_lock:
            if controller:
                controller.wait_for_enter()
            else:
                input("Press Enter key to continue...")
    if controller:
        controller.check_pause()
