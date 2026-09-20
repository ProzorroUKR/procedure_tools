"""
Action keywords.

Each keyword is a thin wrapper around one ``procedure_tools`` action: it hands
the action the payload the test built and returns what the action put into the
shared context. No data files are involved - the payload comes from the
``ProcedureData`` keywords, and the files of a document are written to a
temporary directory when the document is uploaded.

    Start Procedure Session
    ${tender}=    Create Tender    ${tender_data}
    Patch Tender  ${{ {'data': {'status': 'active.tendering'}} }}

The session reads the API host, token and document service credentials from
the same environment variables as the ``procedure-tools`` command
(``API_HOST``, ``API_TOKEN``, ``DS_HOST``, ``DS_USERNAME``, ``DS_PASSWORD``,
``ACCELERATION``, ``SUBMISSION``), so one env file drives both.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
from collections.abc import Callable
from typing import Any

import requests
from robot.api import logger
from robot.api.deco import keyword, library

from procedure_tools.actions import ACTIONS, format_actions
from procedure_tools.context import Context
from procedure_tools.main import parse_args, set_faker_seed
from procedure_tools.runner import build_context, run_action
from procedure_tools.utils import adapters
from procedure_tools.utils.handlers import ProcedureExit

# Key the data builders put the file content of a document under.
CONTENTS_KEY = "contents"

# Context entries that describe the run rather than a procedure, so they
# survive a reset between tests.
RUN_KEYS = ("acceleration", "submission", "client_timedelta", "constants")

# The logger the actions and the API client write to.
PROCEDURE_LOGGER = "procedure_tools"

# Environment switch for the console log; on unless it is turned off.
CONSOLE_LOG_VAR = "ROBOT_CONSOLE_LOG"
FALSE_VALUES = frozenset({"0", "false", "no", "off"})


class ConsoleLogHandler(logging.Handler):
    """
    Sends the procedure_tools log to the terminal.

    Robot captures whatever a library writes to stdout and files it away in
    ``log.html``, so a running suite says nothing beyond a dot per keyword.
    ``robot.api.logger.console`` writes past that capture, which puts every
    request the actions make back in front of whoever is watching the run.

    ``break_line`` is asked, before the first message of a test, whether the
    console is still sitting on the unfinished ``Test name   `` line that
    Robot printed; the log then starts below it instead of next to it.
    """

    def __init__(self, break_line: Callable[[], bool] | None = None) -> None:
        super().__init__()
        self.break_line = break_line

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record).rstrip()
        except Exception:  # pylint: disable=broad-exception-caught  # noqa: BLE001
            self.handleError(record)
            return
        if not message:
            return
        if self.break_line is not None and self.break_line():
            logger.console("")
        logger.console(message)


def console_log_default() -> bool:
    return os.environ.get(CONSOLE_LOG_VAR, "").strip().lower() not in FALSE_VALUES


@library(scope="GLOBAL", version="1.0")
class ProcedureTools:
    """Drives ``procedure_tools`` actions from Robot Framework."""

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self) -> None:
        self.ROBOT_LIBRARY_LISTENER = self  # to know when a test starts, see break_console_line
        self._context: Context | None = None
        self._session: requests.Session | None = None
        self._files_dir: str | None = None
        self._console_handler: logging.Handler | None = None
        self._console_line_open = False

    # --- console

    def start_test(self, data: Any, result: Any) -> None:  # pylint: disable=unused-argument
        """Listener hook: Robot has just written the name of a test, unfinished."""
        self._console_line_open = True

    def break_console_line(self) -> bool:
        """True once per test, for the first log line that follows the test name."""
        if not self._console_line_open:
            return False
        self._console_line_open = False
        return True

    # --- session

    @property
    def context(self) -> Context:
        if self._context is None:
            raise RuntimeError("no procedure session, run 'Start Procedure Session' first")
        return self._context

    @keyword("Start Procedure Session")
    def start_procedure_session(self, console: bool | None = None, **options: Any) -> None:
        """
        Connect to the CDB and the document service.

        Settings come from the environment (``API_HOST``, ``API_TOKEN``,
        ``DS_HOST``, ``DS_USERNAME``, ``DS_PASSWORD``, ``ACCELERATION``,
        ``SUBMISSION``); ``options`` override any of them by argparse name,
        for example ``acceleration=1000``.

        ``console`` mirrors the procedure log to the terminal, so a run shows
        the requests it makes instead of one dot per keyword. It is on unless
        ``ROBOT_CONSOLE_LOG`` says otherwise, and it changes nothing about
        ``log.html``, which keeps the full log either way.
        """
        self._start_console_log(console_log_default() if console is None else bool(console))
        args = parse_args([])
        for name, value in options.items():
            setattr(args, name, value)
        set_faker_seed(args)
        self._session = requests.Session()
        adapters.mount(self._session)
        self._files_dir = tempfile.mkdtemp(prefix="robot_tests_")
        self._context = build_context(args, session=self._session)
        logger.info(f"Connected to {args.host} as broker, acceleration {args.acceleration}")

    @keyword("End Procedure Session")
    def end_procedure_session(self) -> None:
        """Close the HTTP session and remove the generated document files."""
        if self._session is not None:
            self._session.close()
            self._session = None
        if self._files_dir and os.path.isdir(self._files_dir):
            shutil.rmtree(self._files_dir, ignore_errors=True)
        self._files_dir = None
        self._context = None
        self._stop_console_log()

    def _start_console_log(self, enabled: bool) -> None:
        self._stop_console_log()
        if not enabled:
            return
        handler = ConsoleLogHandler(break_line=self.break_console_line)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger(PROCEDURE_LOGGER).addHandler(handler)
        self._console_handler = handler

    def _stop_console_log(self) -> None:
        if self._console_handler is not None:
            logging.getLogger(PROCEDURE_LOGGER).removeHandler(self._console_handler)
            self._console_handler = None

    @keyword("Reset Procedure State")
    def reset_procedure_state(self) -> None:
        """
        Forget the procedure built so far and keep the connection.

        Use it as the test setup: the plan, tender, bids, awards and contracts
        of the previous test go, the API session and the run settings stay.
        """
        context = self.context
        for key in [key for key in context if key not in RUN_KEYS]:
            del context[key]
        context.resources.clear()
        context.step = None
        context.skip_steps = 0
        context.allow_fail_next = False

    @keyword("Get Acceleration")
    def get_acceleration(self) -> int | None:
        """The acceleration multiplier of this run, as the tender dates need it."""
        value: int | None = self.context.args.acceleration
        return value

    @keyword("Get Submission")
    def get_submission(self) -> str | None:
        """The ``submissionMethodDetails`` of this run, if one is configured."""
        value: str | None = self.context.args.submission
        return value

    # --- generic

    @keyword("Run Procedure Action")
    def run_procedure_action(
        self,
        action: str,
        data: dict[str, Any] | list[Any] | None = None,
        *parts: Any,
    ) -> None:
        """
        Run any registered action with the payload passed in.

        The named keywords below cover the common ones; this is the way to
        reach an action that has no wrapper yet. ``parts`` are what a data file
        name would carry after the action name, an object index for example.
        """
        if action not in ACTIONS:
            raise ValueError(f"unknown action {action!r}. Available actions:\n{format_actions()}")
        payload = self._register_files(data)
        try:
            run_action(self.context, action, [str(part) for part in parts], payload)
        except ProcedureExit as e:
            # The actions end the process on a rejected request, which is right
            # for the command line but would abort the whole Robot run. Here it
            # is one failing step, so report it as a failing keyword.
            raise AssertionError(f"{action}: {e.message or e}") from None

    @keyword("Get Context Value")
    def get_context_value(self, key: str, default: Any = None) -> Any:
        """A value the actions put into the shared context (``tender``, ``awards``, ...)."""
        return self.context.get(key, default)

    # --- plan

    @keyword("Create Plan")
    def create_plan(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a plan; the next tender is created from it."""
        self.run_procedure_action("plan_create", data)
        plan: dict[str, Any] = self.context["plan"]
        return plan

    @keyword("Patch Plan")
    def patch_plan(self, data: dict[str, Any], index: int | None = None) -> dict[str, Any]:
        """Patch a plan, by default the last one created."""
        parts = [index] if index is not None else []
        self.run_procedure_action("plan_patch", data, *parts)
        plan: dict[str, Any] = self.context["plan"]
        return plan

    # --- tender

    @keyword("Create Tender")
    def create_tender(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a tender, from the plan in the context when there is one."""
        self.run_procedure_action("tender_create", data)
        return self.get_tender()

    @keyword("Patch Tender")
    def patch_tender(self, data: dict[str, Any]) -> dict[str, Any]:
        """Patch the tender, for example to publish it."""
        self.run_procedure_action("tender_patch", data)
        return self.get_tender()

    @keyword("Refresh Tender")
    def refresh_tender(self) -> dict[str, Any]:
        """Re-read the tender from the API."""
        self.run_procedure_action("tender_get")
        return self.get_tender()

    @keyword("Get Tender")
    def get_tender(self) -> dict[str, Any]:
        """The tender as the context currently holds it."""
        tender: dict[str, Any] = self.context.require("tender", "create a tender first")
        return tender

    @keyword("Get Tender Token")
    def get_tender_token(self) -> str:
        """The access token of the tender."""
        token: str = self.context.require("tender_token", "create a tender first")
        return token

    @keyword("Attach Tender Document")
    def attach_tender_document(self, document: dict[str, Any]) -> dict[str, Any]:
        """Upload a document and attach it to the tender."""
        self.run_procedure_action("tender_document_attach", document)
        documents: list[dict[str, Any]] = self.context.get("tender_documents") or []
        return documents[-1] if documents else {}

    @keyword("Post Tender Criteria")
    def post_tender_criteria(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        """Publish the criteria of the tender and return them with their ids."""
        self.run_procedure_action("tender_criteria_post", data)
        criteria: list[dict[str, Any]] = self.context["criteria"]
        return criteria

    # --- bids

    @keyword("Create Bid")
    def create_bid(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Create a draft bid, uploading the documents it carries."""
        self.run_procedure_action("tender_bid_create", data, index)
        return self.get_bid(index)

    @keyword("Patch Bid")
    def patch_bid(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Patch a bid, for example to submit it."""
        self.run_procedure_action("tender_bid_patch", data, index)
        return self.get_bid(index)

    @keyword("Post Bid Requirement Responses")
    def post_bid_requirement_responses(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Answer the tender criteria for a bid."""
        self.run_procedure_action("tender_bid_res_post", data, index)
        return self.get_bid(index)

    @keyword("Attach Bid Document")
    def attach_bid_document(self, document: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Upload a document and attach it to a bid."""
        self.run_procedure_action("tender_bid_document_attach", document, index)
        return self.get_bid(index)

    @keyword("Get Bid")
    def get_bid(self, index: int = 0) -> dict[str, Any]:
        """A bid created in this run."""
        bid: dict[str, Any] = self.context.item("bids", int(index), hint="create the bid first")
        return bid

    @keyword("Get Bids")
    def get_bids(self) -> list[dict[str, Any]]:
        """Every bid created in this run."""
        bids: list[dict[str, Any]] = self.context.get("bids") or []
        return bids

    # --- waiting

    @keyword("Wait Tender Status")
    def wait_tender_status(
        self,
        status: str | list[str],
        fail_status: str | list[str] | None = None,
        delay: float = 1,
    ) -> dict[str, Any]:
        """Poll the tender until it reaches ``status``, failing on ``fail_status``."""
        data: dict[str, Any] = {"status": status, "delay": delay}
        if fail_status:
            data["fail_status"] = fail_status
        self.run_procedure_action("tender_wait_status", data)
        return self.get_tender()

    @keyword("Wait Tender Next Check")
    def wait_tender_next_check(self) -> dict[str, Any]:
        """Wait for the next chronograph check of the tender."""
        self.run_procedure_action("tender_wait_next_check")
        return self.get_tender()

    @keyword("Wait Tender Auction")
    def wait_tender_auction(self) -> None:
        """Wait for the auction participation urls of the active bids."""
        self.run_procedure_action("tender_wait_auction")

    @keyword("Wait Awards Complaint Period")
    def wait_awards_complaint_period(self) -> None:
        """Wait for the complaint period of every award to end."""
        self.run_procedure_action("tender_awards_wait_complaint_period")

    @keyword("Wait Awards Edr Documents")
    def wait_awards_edr_documents(self) -> None:
        """Wait for the EDR documents of the awards (only with ``WAIT=edr-qualification``)."""
        self.run_procedure_action("tender_awards_wait_edr")

    @keyword("Wait Date")
    def wait_date(self, date: str, description: str | None = None) -> None:
        """Wait until an ISO date has passed."""
        self.run_procedure_action("wait_date", {"date": date, "description": description})

    @keyword("Wait Seconds")
    def wait_seconds(self, seconds: float) -> None:
        """Sleep, taking a paused run into account."""
        self.run_procedure_action("wait_seconds", {"seconds": seconds})

    # --- awards

    @keyword("Create Award")
    def create_award(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create an award; limited procedures pick the supplier this way."""
        self.run_procedure_action("tender_award_create", data)
        return self.get_award(0)

    @keyword("Patch Award")
    def patch_award(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Patch an award: qualify it, activate it or make it unsuccessful."""
        self.run_procedure_action("tender_award_patch", data, index)
        return self.get_award(index)

    @keyword("Attach Award Document")
    def attach_award_document(self, document: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Upload a document and attach it to an award."""
        self.run_procedure_action("tender_award_document_attach", document, index)
        return self.get_award(index)

    @keyword("Get Awards")
    def get_awards(self) -> list[dict[str, Any]]:
        """The awards of the tender, fetched when they are not in the context yet."""
        self.run_procedure_action("tender_awards_get")
        awards: list[dict[str, Any]] = self.context.get("awards") or []
        return awards

    @keyword("Get Award")
    def get_award(self, index: int = 0) -> dict[str, Any]:
        """One award of the tender, fetching the awards when they are not loaded yet."""
        if not self.context.get("awards"):
            self.get_awards()
        award: dict[str, Any] = self.context.item("awards", int(index))
        return award

    # --- contracts

    @keyword("Get Contracts")
    def get_contracts(self) -> list[dict[str, Any]]:
        """The contracts of the tender, read from the contracting API."""
        self.run_procedure_action("tender_contracts_get")
        contracts: list[dict[str, Any]] = self.context.get("contracts") or []
        return contracts

    @keyword("Get Contract")
    def get_contract(self, index: int = 0) -> dict[str, Any]:
        """One contract of the tender, fetching the contracts when they are not loaded yet."""
        if not self.context.get("contracts"):
            self.get_contracts()
        contract: dict[str, Any] = self.context.item("contracts", int(index))
        return contract

    @keyword("Take Contract Credentials")
    def take_contract_credentials(self, index: int = 0) -> dict[str, Any]:
        """Get the access token of a contract, which every later change needs."""
        self.run_procedure_action("contract_credentials_patch", {}, index)
        return self.get_contract(index)

    @keyword("Put Contract Buyer Signer Info")
    def put_contract_buyer_signer_info(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Set the signer info of the buyer."""
        self.run_procedure_action("contract_buyer_signer_info_put", data, index)
        return self.get_contract(index)

    @keyword("Put Contract Suppliers Signer Info")
    def put_contract_suppliers_signer_info(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Set the signer info of the supplier, signed with the winning bid token."""
        self.run_procedure_action("contract_suppliers_signer_info_put", data, index)
        return self.get_contract(index)

    @keyword("Patch Contract")
    def patch_contract(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Patch a contract: sign it, change its value or terminate it."""
        self.run_procedure_action("contract_patch", data, index)
        return self.get_contract(index)

    @keyword("Post Contract Change")
    def post_contract_change(self, data: dict[str, Any], index: int = 0) -> dict[str, Any]:
        """Create an amendment to an active contract."""
        self.run_procedure_action("contract_change_post", data, index)
        return self.get_contract(index)

    @keyword("Patch Contract Change")
    def patch_contract_change(
        self,
        data: dict[str, Any],
        index: int = 0,
        change_index: int = 0,
    ) -> dict[str, Any]:
        """Patch an amendment, for example to activate it."""
        self.run_procedure_action("contract_change_patch", data, index, change_index)
        return self.get_contract(index)

    # --- files

    def _register_files(self, data: Any) -> Any:
        """
        Write the document files a payload carries and make the actions find them.

        ``ProcedureData`` puts the content of a document under ``contents``,
        keyed by file name. Here it becomes a real file in the temporary
        directory of the session, registered under the same name the payload
        refers to, and the key is dropped before the payload is sent.
        """
        if not isinstance(data, dict) or CONTENTS_KEY not in data:
            return data
        payload = {key: value for key, value in data.items() if key != CONTENTS_KEY}
        directory = self._files_dir or tempfile.mkdtemp(prefix="robot_tests_")
        self._files_dir = directory
        for title, content in (data.get(CONTENTS_KEY) or {}).items():
            path = os.path.join(directory, title)
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            self.context.resources[title] = path
        return payload
