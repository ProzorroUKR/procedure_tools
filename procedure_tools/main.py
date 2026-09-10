import argparse
import copy
import logging
import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from procedure_tools.client import API_PATH_PREFIX_DEFAULT
from procedure_tools.fake import fake, fake_en
from procedure_tools.procedure import WAIT_EDR_PRE_QUAL, WAIT_EDR_QUAL, process_procedure
from procedure_tools.utils import adapters
from procedure_tools.utils.data import (
    ACCELERATION_DEFAULT,
    SUBMISSION_QUICK_NO_AUCTION,
    SUBMISSIONS,
)
from procedure_tools.utils.file import DATA_DIR_DEFAULT, get_data_path, get_default_data_dirs, get_numberless_filename
from procedure_tools.utils.handlers import EX_DATAERR, EX_OK
from procedure_tools.utils.style import (
    fore_error,
    fore_info,
    fore_log_level,
    fore_success,
    fore_warning,
    get_log_prefix,
    set_log_prefix,
)
from procedure_tools.version import __version__

WAIT_EVENTS = (WAIT_EDR_QUAL, WAIT_EDR_PRE_QUAL)

LOG_DATEFMT = "%H:%M:%S"

LOG_FORMAT_DEFAULT = "%(asctime)s %(prefix)s%(message)s"
LOG_FORMAT_DEBUG = "%(asctime)s %(levelname)s %(name)s %(prefix)s%(message)s"


class OutputFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dfmt = datefmt if datefmt is not None else self.datefmt
        plain = super().formatTime(record, dfmt)
        return fore_log_level(f"[{plain}]", record.level)

    def format(self, record):
        if not hasattr(record, "prefix"):
            record.prefix = ""
        return super().format(record)


class OutputFilter(logging.Filter):
    def filter(self, record):
        record.level = record.levelname  # back up uncolored levelname
        record.levelname = fore_log_level(record.levelname, record.level)
        record.name = fore_log_level(record.name or "", record.level)
        prefix = get_log_prefix()
        record.prefix = f"{fore_info('[' + prefix + ']')} " if prefix else ""
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


def format_choices(choices):
    return " - " + "\n - ".join(choices)


def set_faker_seed(args):
    faker_seed = args.seed or random.randint(0, 1000000)
    logging.info(f"Using seed {faker_seed}\n")
    fake.seed_instance(faker_seed)
    fake_en.seed_instance(faker_seed)


def exit_code(value):
    if value is None:
        return EX_OK
    if isinstance(value, int):
        return value
    return 1


def log_summary(results):
    width = max(len(str(data_dir)) for data_dir, _, _ in results)
    lines = ["Summary"]
    errors = []
    for data_dir, code, error in results:
        if code is None:
            status = fore_warning("aborted")
        elif code == EX_OK:
            status = fore_success("success")
        else:
            status = fore_error("failed")
            if error:
                errors.append((data_dir, error))
        lines.append(f" - {data_dir:<{width}}\t{status}")
    logging.info("\n".join(lines) + "\n")
    if errors:
        error_lines = ["Errors"]
        for data_dir, error in errors:
            error_text = str(error).strip().splitlines() or [str(error).strip()]
            error_lines.append(f" - {data_dir}")
            for error_line in error_text:
                error_lines.append(f"   {fore_error(error_line)}")
        logging.info("\n".join(error_lines) + "\n")
    for handler in logging.root.handlers:
        handler.flush()


def run_result_error(exc):
    message = getattr(exc, "message", None)
    if message:
        return str(message).strip()
    text = str(exc).strip()
    name = type(exc).__name__
    if name in ("ProcedureExit", "SystemExit"):
        return text or name
    if not text:
        return name
    return f"{name}: {text}"


def run_data_dir(args, session=None):
    close_session = False
    if session is None:
        session = requests.Session()
        adapters.mount(session)
        close_session = True
    try:
        data_path = get_data_path(args.data)
        if data_path is None:
            logging.error("Data path not found.\n")
            return EX_DATAERR, "Data path not found"
        process_procedure(args, session=session)
        logging.info("Completed.\n")
        return EX_OK, None
    except SystemExit as e:
        code = exit_code(e.code)
        if code == EX_OK:
            logging.info("Completed.\n")
            return code, None
        return code, run_result_error(e)
    except Exception as e:
        logging.exception("Failed")
        return 1, run_result_error(e)
    finally:
        if close_session:
            session.close()


def run_data_dir_parallel(args, data_dir):
    folder_args = copy.copy(args)
    folder_args.data = data_dir
    set_log_prefix(data_dir)
    try:
        set_faker_seed(folder_args)
        return run_data_dir(folder_args)
    except Exception as e:
        logging.exception("Failed")
        return 1, run_result_error(e)
    finally:
        set_log_prefix(None)


def run(args, session=None):
    if args.stop:
        args.stop = get_numberless_filename(args.stop)

    if args.pause:
        args.pause = [get_numberless_filename(filename) for filename in args.pause]
    args.wait = args.wait or []

    data_dirs = args.data if isinstance(args.data, list) else [args.data]
    interrupted = False
    if args.parallel is not None and len(data_dirs) > 1:
        codes = {}
        max_workers = args.parallel or len(data_dirs)
        max_workers = max(1, min(max_workers, len(data_dirs)))
        executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="procedure")
        try:
            futures = {executor.submit(run_data_dir_parallel, args, data_dir): data_dir for data_dir in data_dirs}
            for future in as_completed(futures):
                data_dir = futures[future]
                try:
                    codes[data_dir] = future.result()
                except KeyboardInterrupt:
                    raise
                except BaseException as e:
                    codes[data_dir] = (1, run_result_error(e))
        except KeyboardInterrupt:
            executor.shutdown(wait=False, cancel_futures=True)
            interrupted = True
            for future, data_dir in futures.items():
                if data_dir in codes:
                    continue
                if future.done() and not future.cancelled():
                    try:
                        codes[data_dir] = future.result()
                    except BaseException as e:
                        codes[data_dir] = (1, run_result_error(e))
                else:
                    codes[data_dir] = (None, None)
        else:
            executor.shutdown(wait=True)
        results = [(data_dir, *(codes.get(data_dir) or (None, None))) for data_dir in data_dirs]
    else:
        set_faker_seed(args)
        results = []
        for data_dir in data_dirs:
            args.data = data_dir
            if len(data_dirs) > 1:
                logging.info(f"Starting {data_dir}\n")
            try:
                code, error = run_data_dir(args, session=session)
                results.append((data_dir, code, error))
            except KeyboardInterrupt:
                results.append((data_dir, None, None))
                results.extend((remaining, None, None) for remaining in data_dirs[len(results) :])
                interrupted = True
                break

    if len(results) > 1 or interrupted:
        log_summary(results)
    if interrupted:
        raise KeyboardInterrupt
    failed = [code for _, code, _ in results if code != EX_OK]
    if failed:
        raise SystemExit(failed[0])


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
        help=f"one or more data folders, custom path or one of (omit to run all; sequential unless --parallel):\n{format_choices(sorted(get_default_data_dirs()))}",
        metavar=str(DATA_DIR_DEFAULT),
        action="extend",
        nargs="+",
    )
    parser.add_argument(
        "--parallel",
        help="run data folders in parallel (optional max concurrent folders; omit N to run all)",
        metavar="N",
        nargs="?",
        const=0,
        default=None,
        type=int,
    )
    parser.add_argument(
        "-m",
        "--submission",
        help=f"value for submissionMethodDetails, one of:\n{format_choices(SUBMISSIONS)}",
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
        help="one or more data file names to pause after",
        metavar="tender_create.json",
        action="extend",
        nargs="+",
    )
    parser.add_argument(
        "-w",
        "--wait",
        help=f"one or more events to wait for:\n{format_choices(WAIT_EVENTS)}",
        metavar=WAIT_EDR_QUAL,
        action="extend",
        nargs="+",
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
        if args.parallel is not None and args.parallel < 0:
            parser.error("--parallel must be >= 0")
        apply_debug_log_format(args.debug)
        if not args.data:
            args.data = sorted(get_default_data_dirs())
        session = None
        if args.parallel is None:
            session = requests.Session()
            adapters.mount(session)
        run(args, session=session)
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        os._exit(130)
    else:
        sys.exit(EX_OK)


if __name__ == "__main__":
    main()
