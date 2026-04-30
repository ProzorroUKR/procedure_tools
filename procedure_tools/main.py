import argparse
import logging
import sys

import requests

from procedure_tools.client import API_PATH_PREFIX_DEFAULT
from procedure_tools.procedure import WAIT_EDR_PRE_QUAL, WAIT_EDR_QUAL, init_procedure
from procedure_tools.utils import adapters
from procedure_tools.utils.data import (
    ACCELERATION_DEFAULT,
    SUBMISSION_QUICK_NO_AUCTION,
    SUBMISSIONS,
)
from procedure_tools.utils.file import DATA_DIR_DEFAULT, get_default_data_dirs
from procedure_tools.utils.handlers import EX_OK
from procedure_tools.utils.style import fore_log_level
from procedure_tools.version import __version__

WAIT_EVENTS = (WAIT_EDR_QUAL, WAIT_EDR_PRE_QUAL)

LOG_DATEFMT = "%H:%M:%S"

LOG_FORMAT_DEFAULT = "%(asctime)s %(message)s"
LOG_FORMAT_DEBUG = "%(asctime)s %(levelname)s %(name)s %(message)s"


class OutputFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dfmt = datefmt if datefmt is not None else self.datefmt
        plain = super().formatTime(record, dfmt)
        return fore_log_level(f"[{plain}]", record.level)


class OutputFilter(logging.Filter):
    def filter(self, record):
        record.level = record.levelname  # back up uncolored levelname
        record.levelname = fore_log_level(record.levelname, record.level)
        record.name = fore_log_level(record.name or "", record.level)
        return True


OUTPUT_FILTER = OutputFilter()
OUTPUT_FORMATTER = OutputFormatter(LOG_FORMAT_DEFAULT, datefmt=LOG_DATEFMT)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
for handler in logging.root.handlers:
    handler.addFilter(OUTPUT_FILTER)
    handler.setFormatter(OUTPUT_FORMATTER)


def apply_debug_log_format(debug: bool):
    fmt = LOG_FORMAT_DEBUG if debug else LOG_FORMAT_DEFAULT
    formatter = OutputFormatter(fmt, datefmt=LOG_DATEFMT)
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)


class ArgumentParserFormatter(argparse.RawTextHelpFormatter):
    def _format_action(self, action):
        return "\n\n" + super()._format_action(action)


def _format_choices(choices):
    return " - " + "\n - ".join(choices)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=ArgumentParserFormatter,
    )
    parser.add_argument("host", help="CDB API Host")
    parser.add_argument("token", help="CDB API Token")
    parser.add_argument("ds_host", help="DS API Host")
    parser.add_argument("ds_username", help="DS API Username")
    parser.add_argument("ds_password", help="DS API Password")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-a",
        "--acceleration",
        help="acceleration multiplier",
        metavar=str(ACCELERATION_DEFAULT),
        type=int,
    )
    parser.add_argument(
        "-p",
        "--path",
        help="api path",
        metavar=str(API_PATH_PREFIX_DEFAULT),
        default=API_PATH_PREFIX_DEFAULT,
    )
    parser.add_argument(
        "-d",
        "--data",
        help=f"data files, custom path or one of:\n{_format_choices(sorted(get_default_data_dirs()))}",
        metavar=str(DATA_DIR_DEFAULT),
        default=DATA_DIR_DEFAULT,
    )
    parser.add_argument(
        "-m",
        "--submission",
        help=f"value for submissionMethodDetails, one of:\n{_format_choices(SUBMISSIONS)}",
        metavar=str(SUBMISSION_QUICK_NO_AUCTION),
    )
    parser.add_argument(
        "-s",
        "--stop",
        help="data file name to stop after",
        metavar="tender_create.json",
    )
    parser.add_argument(
        "--pause",
        help="data file name(s) to pause after (comma-separated)",
        metavar="tender_create.json",
    )
    parser.add_argument(
        "-w",
        "--wait",
        help=f"wait for event, one or many of (divided by comma):\n{_format_choices(WAIT_EVENTS)}",
        metavar=WAIT_EDR_QUAL,
        default="",
    )
    parser.add_argument(
        "-e",
        "--seed",
        type=int,
        help="faker seed",
    )
    parser.add_argument(
        "--reviewer-token",
        help="reviewer token",
    )
    parser.add_argument(
        "--bot-token",
        help="bot token",
    )
    parser.add_argument(
        "--debug",
        help="Debug log level",
        action="store_true",
    )
    parser.add_argument(
        "--debug-req",
        "--debug-request",
        dest="debug_request",
        help="Log HTTP request/response bodies",
        action="store_true",
    )
    parser.add_argument(
        "--debug-json-level",
        dest="debug_json_level",
        type=int,
        help="Fold debug request/response JSON to specified nesting level (>=0)",
    )

    try:
        args = parser.parse_args()
        if args.debug_json_level is not None and args.debug_json_level < 0:
            parser.error("--debug-json-level must be >= 0")
        apply_debug_log_format(args.debug)
        session = requests.Session()
        adapters.mount(session)
        init_procedure(args, session=session)
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt as e:
        sys.exit(str(e))
    else:
        sys.exit(EX_OK)


if __name__ == "__main__":
    main()
