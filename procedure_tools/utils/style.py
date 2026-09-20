import os
import threading

_log_context = threading.local()


def set_log_prefix(prefix: str | None) -> None:
    _log_context.prefix = prefix


def get_log_prefix() -> str | None:
    return getattr(_log_context, "prefix", None)


try:
    from colorama import Fore, Style

    FORE_INFO: str = Fore.CYAN
    FORE_SUCCESS: str = Fore.GREEN
    FORE_WARNING: str = Fore.YELLOW
    FORE_ERROR: str = Fore.RED
    FORE_DEBUG: str = Fore.BLUE
    FORE_RESET: str = Style.RESET_ALL
    STYLE_DIM: str = Style.DIM
except ImportError:
    FORE_INFO = ""
    FORE_SUCCESS = ""
    FORE_WARNING = ""
    FORE_ERROR = ""
    FORE_DEBUG = ""
    FORE_RESET = ""
    STYLE_DIM = ""


def fore(msg: str, fr: str) -> str:
    if os.getenv("NO_COLOR"):
        return msg
    return fr + msg + FORE_RESET


def fore_info(msg: str) -> str:
    return fore(msg, FORE_INFO)


def fore_success(msg: str) -> str:
    return fore(msg, FORE_SUCCESS)


def fore_warning(msg: str) -> str:
    return fore(msg, FORE_WARNING)


def fore_error(msg: str) -> str:
    return fore(msg, FORE_ERROR)


def fore_debug(msg: str) -> str:
    return fore(msg, FORE_DEBUG)


def fore_method(method: str | None) -> str:
    normalized_method = str(method or "").upper()
    color = {
        "GET": FORE_SUCCESS,
        "POST": FORE_INFO,
        "PUT": FORE_WARNING,
        "PATCH": FORE_WARNING,
        "DELETE": FORE_ERROR,
        "HEAD": FORE_DEBUG,
        "OPTIONS": FORE_DEBUG,
        "TRACE": FORE_DEBUG,
    }.get(normalized_method, FORE_INFO)
    return fore(normalized_method, color)


def level_fore(levelname: str) -> str:
    colors = {
        "DEBUG": FORE_DEBUG,
        "INFO": FORE_SUCCESS,
        "WARNING": FORE_WARNING,
        "ERROR": FORE_ERROR,
        "CRITICAL": FORE_ERROR,
    }
    return colors.get(levelname, FORE_INFO) or ""


def fore_log_level(msg: str, levelname: str) -> str:
    return fore(msg, level_fore(levelname) or FORE_INFO)


def fore_status_code(code: int) -> str:
    msg = str(code)
    if 100 <= code < 200:
        return fore_info(msg)
    if 200 <= code < 300:
        return fore_success(msg)
    if 300 <= code < 400:
        return fore_warning(msg)
    if 400 <= code < 500:
        return fore_error(msg)
    if 500 <= code:
        return fore_error(msg)
    return msg
