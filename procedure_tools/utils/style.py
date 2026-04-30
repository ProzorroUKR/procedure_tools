try:
    from colorama import Fore, Style

    FORE_INFO = Fore.CYAN
    FORE_SUCCESS = Fore.GREEN
    FORE_WARNING = Fore.YELLOW
    FORE_ERROR = Fore.RED
    FORE_DEBUG = Fore.BLUE
    FORE_RESET = Style.RESET_ALL
    STYLE_DIM = Style.DIM
except ImportError:
    FORE_INFO = ""
    FORE_SUCCESS = ""
    FORE_WARNING = ""
    FORE_ERROR = ""
    FORE_DEBUG = ""
    FORE_RESET = ""
    STYLE_DIM = ""


def fore(msg, fr):
    return fr + msg + FORE_RESET


def fore_info(msg):
    return fore(msg, FORE_INFO)


def fore_success(msg):
    return fore(msg, FORE_SUCCESS)


def fore_warning(msg):
    return fore(msg, FORE_WARNING)


def fore_error(msg):
    return fore(msg, FORE_ERROR)


def level_fore(levelname):
    """Foreground ANSI code for a logging level (no reset); use to build multi-field lines."""
    colors = {
        "DEBUG": FORE_DEBUG,
        "INFO": FORE_SUCCESS,
        "WARNING": FORE_WARNING,
        "ERROR": FORE_ERROR,
        "CRITICAL": FORE_ERROR,
    }
    return colors.get(levelname, FORE_INFO) or ""


def fore_log_level(msg, levelname):
    """ANSI-colored log level name for terminals (no-op if colorama unavailable)."""
    return fore(msg, level_fore(levelname) or FORE_INFO)


def fore_status_code(code):
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
