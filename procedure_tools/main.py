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
from procedure_tools.procedure import (
    WAIT_EDR_PRE_QUAL,
    WAIT_EDR_QUAL,
    process_procedure,
)
from procedure_tools.utils import adapters
from procedure_tools.utils.data import (
    ACCELERATION_DEFAULT,
    SUBMISSION_QUICK_NO_AUCTION,
    SUBMISSIONS,
)
from procedure_tools.utils.env import (
    ENV_SELECT_VAR,
    EXTEND_ARGS,
    REQUIRED_ARGS,
    EnvFileNotFound,
    EnvValueError,
    first_set,
    load_run_env,
)
from procedure_tools.utils.file import (
    DATA_DIR_DEFAULT,
    get_data_path,
    get_default_data_dirs,
    get_numberless_filename,
)
from procedure_tools.utils.handlers import EX_DATAERR, EX_OK
from procedure_tools.utils.runtime import RunController, log_results_summary, set_controller
from procedure_tools.utils.style import (
    fore_info,
    fore_log_level,
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


def run_data_dir(args, session=None, controller=None):
    close_session = False
    if session is None:
        session = requests.Session()
        adapters.mount(session)
        close_session = True
    data_dir = args.data
    if controller:
        controller.mark_started(data_dir)
    try:
        data_path = get_data_path(args.data)
        if data_path is None:
            logging.error("Data path not found.\n")
            result = EX_DATAERR, "Data path not found"
        else:
            process_procedure(args, session=session)
            logging.info("Completed.\n")
            result = EX_OK, None
    except SystemExit as e:
        code = exit_code(e.code)
        if code == EX_OK:
            logging.info("Completed.\n")
            result = code, None
        else:
            result = code, run_result_error(e)
    except Exception as e:
        logging.exception("Failed")
        result = 1, run_result_error(e)
    finally:
        if close_session:
            session.close()
    if controller:
        controller.mark_finished(data_dir, *result)
    return result


def run_data_dir_parallel(args, data_dir, controller=None):
    folder_args = copy.copy(args)
    folder_args.data = data_dir
    set_log_prefix(data_dir)
    try:
        set_faker_seed(folder_args)
        return run_data_dir(folder_args, controller=controller)
    except Exception as e:
        logging.exception("Failed")
        result = 1, run_result_error(e)
        if controller:
            controller.mark_finished(data_dir, *result)
        return result
    finally:
        set_log_prefix(None)


def run(args, session=None):
    if args.stop:
        args.stop = get_numberless_filename(args.stop)

    if args.pause:
        args.pause = [get_numberless_filename(filename) for filename in args.pause]
    args.wait = args.wait or []

    data_dirs = args.data if isinstance(args.data, list) else [args.data]
    controller = RunController(data_dirs)
    set_controller(controller)
    controller.start()
    interrupted = False
    try:
        if args.parallel is not None and len(data_dirs) > 1:
            codes = {}
            max_workers = args.parallel or len(data_dirs)
            max_workers = max(1, min(max_workers, len(data_dirs)))
            executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="procedure")
            try:
                futures = {
                    executor.submit(run_data_dir_parallel, args, data_dir, controller): data_dir
                    for data_dir in data_dirs
                }
                for future in as_completed(futures):
                    data_dir = futures[future]
                    try:
                        codes[data_dir] = future.result()
                    except KeyboardInterrupt:
                        raise
                    except BaseException as e:
                        result = (1, run_result_error(e))
                        codes[data_dir] = result
                        controller.mark_finished(data_dir, *result)
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
                            result = (1, run_result_error(e))
                            codes[data_dir] = result
                            controller.mark_finished(data_dir, *result)
                    else:
                        codes[data_dir] = (None, None)
                        controller.mark_finished(data_dir, None, None)
            else:
                executor.shutdown(wait=True)
            results = [(data_dir, *(codes.get(data_dir) or (None, None))) for data_dir in data_dirs]
        else:
            set_faker_seed(args)
            results = []
            for data_dir in data_dirs:
                args.data = data_dir
                set_log_prefix(data_dir if len(data_dirs) > 1 else None)
                if len(data_dirs) > 1:
                    logging.info(f"Starting {data_dir}\n")
                try:
                    controller.check_pause()
                    code, error = run_data_dir(args, session=session, controller=controller)
                    results.append((data_dir, code, error))
                except KeyboardInterrupt:
                    controller.mark_finished(data_dir, None, None)
                    results.append((data_dir, None, None))
                    for remaining in data_dirs[len(results) :]:
                        controller.mark_finished(remaining, None, None)
                        results.append((remaining, None, None))
                    interrupted = True
                    break
            set_log_prefix(None)

        if interrupted:
            print("\n")
        log_results_summary(results)
        if interrupted:
            raise KeyboardInterrupt
        failed = [code for _, code, _ in results if code != EX_OK]
        if failed:
            raise SystemExit(failed[0])
    finally:
        controller.stop()
        set_controller(None)


def _env_help():
    return (
        "env file or environment name for this run "
        f"(default: {ENV_SELECT_VAR} or .env if present; CLI arguments override the file).\n"
        "Looks up .env.<name>, <name>.env, or envs/<name>"
    )


def build_parser(env_values=None):
    env_values = env_values or {}
    parser = argparse.ArgumentParser(
        formatter_class=ArgumentParserFormatter,
    )
    parser.add_argument(
        "host",
        nargs="?",
        help="CDB API Host",
    )
    parser.add_argument(
        "token",
        nargs="?",
        help="CDB API Token",
    )
    parser.add_argument(
        "ds_host",
        nargs="?",
        help="DS API Host",
    )
    parser.add_argument(
        "ds_username",
        nargs="?",
        help="DS API Username",
    )
    parser.add_argument(
        "ds_password",
        nargs="?",
        help="DS API Password",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-E",
        "--env",
        help=_env_help(),
        metavar="sandbox",
    )
    parser.add_argument(
        "--host",
        dest="host_option",
        metavar="HOST",
        help="CDB API Host (env API_HOST)",
    )
    parser.add_argument(
        "--token",
        dest="token_option",
        metavar="TOKEN",
        help="CDB API Token (env API_TOKEN)",
    )
    parser.add_argument(
        "--ds-host",
        dest="ds_host_option",
        metavar="DS_HOST",
        help="DS API Host (env DS_HOST)",
    )
    parser.add_argument(
        "--ds-username",
        dest="ds_username_option",
        metavar="DS_USERNAME",
        help="DS API Username (env DS_USERNAME)",
    )
    parser.add_argument(
        "--ds-password",
        dest="ds_password_option",
        metavar="DS_PASSWORD",
        help="DS API Password (env DS_PASSWORD)",
    )
    parser.add_argument(
        "-a",
        "--acceleration",
        help="acceleration multiplier",
        metavar=str(ACCELERATION_DEFAULT),
        type=int,
        default=env_values.get("acceleration"),
    )
    parser.add_argument(
        "-p",
        "--path",
        help="api path",
        metavar=str(API_PATH_PREFIX_DEFAULT),
        default=env_values.get("path", API_PATH_PREFIX_DEFAULT),
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
        default=env_values.get("parallel"),
        type=int,
    )
    parser.add_argument(
        "-m",
        "--submission",
        help=f"value for submissionMethodDetails, one of:\n{format_choices(SUBMISSIONS)}",
        metavar=str(SUBMISSION_QUICK_NO_AUCTION),
        default=env_values.get("submission"),
    )
    parser.add_argument(
        "-s",
        "--stop",
        help="data file name to stop after",
        metavar="tender_create.json",
        default=env_values.get("stop"),
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
        default=env_values.get("seed"),
    )
    parser.add_argument(
        "--reviewer-token",
        help="reviewer token",
        default=env_values.get("reviewer_token"),
    )
    parser.add_argument(
        "--bot-token",
        help="bot token",
        default=env_values.get("bot_token"),
    )
    parser.add_argument(
        "--debug",
        help="Debug log level",
        action="store_true",
        default=bool(env_values.get("debug")),
    )
    parser.add_argument(
        "--debug-req",
        "--debug-request",
        dest="debug_request",
        help="Log HTTP request/response bodies",
        action="store_true",
        default=bool(env_values.get("debug_request")),
    )
    parser.add_argument(
        "--debug-json-level",
        dest="debug_json_level",
        type=int,
        help="Fold debug request/response JSON to specified nesting level (>=0)",
        default=env_values.get("debug_json_level"),
    )
    return parser


def _parse_env_spec(argv):
    env_parser = argparse.ArgumentParser(add_help=False)
    env_parser.add_argument("-E", "--env")
    env_ns, _ = env_parser.parse_known_args(argv)
    return env_ns.env


def apply_env_values(args, env_values):
    args.host = first_set(args.host_option, args.host, env_values.get("host"))
    args.token = first_set(args.token_option, args.token, env_values.get("token"))
    args.ds_host = first_set(args.ds_host_option, args.ds_host, env_values.get("ds_host"))
    args.ds_username = first_set(args.ds_username_option, args.ds_username, env_values.get("ds_username"))
    args.ds_password = first_set(args.ds_password_option, args.ds_password, env_values.get("ds_password"))
    for dest in EXTEND_ARGS:
        if getattr(args, dest) is None and dest in env_values:
            setattr(args, dest, env_values[dest])


def parse_args(argv=None, environ=None, search_dirs=None):
    argv = sys.argv[1:] if argv is None else argv
    if any(arg in ("-h", "--help", "-v", "--version") for arg in argv):
        parser = build_parser()
        parser.parse_args(argv)

    env_spec = _parse_env_spec(argv)
    try:
        env_file, env_values = load_run_env(env_spec, environ=environ, search_dirs=search_dirs)
    except EnvFileNotFound as e:
        parser = build_parser()
        parser.error(str(e))
    except EnvValueError as e:
        parser = build_parser()
        parser.error(str(e))

    parser = build_parser(env_values)
    args = parser.parse_args(argv)
    apply_env_values(args, env_values)
    args.env_file = env_file

    missing = [label for dest, label in REQUIRED_ARGS if not getattr(args, dest)]
    if missing:
        parser.error("the following arguments are required: " + ", ".join(missing))
    if args.debug_json_level is not None and args.debug_json_level < 0:
        parser.error("--debug-json-level must be >= 0")
    if args.parallel is not None and args.parallel < 0:
        parser.error("--parallel must be >= 0")
    return args


def main():
    try:
        args = parse_args()
        apply_debug_log_format(args.debug)
        if args.env_file:
            logging.info(f"Using env file {args.env_file}\n")
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
