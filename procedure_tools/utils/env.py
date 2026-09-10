import os
import re

DEFAULT_ENV_FILE = ".env"
ENV_SELECT_VAR = "PROCEDURE_ENV"
EXAMPLE_SUFFIXES = (".example", ".sample", ".template")

# Maps argparse dest names to env variable names (first match wins).
ARG_ENV_KEYS = {
    "host": ("API_HOST", "HOST"),
    "token": ("API_TOKEN", "TOKEN"),
    "ds_host": ("DS_HOST",),
    "ds_username": ("DS_USERNAME", "DS_USER"),
    "ds_password": ("DS_PASSWORD", "DS_PASS"),
    "acceleration": ("ACCELERATION",),
    "path": ("API_PATH",),
    "data": ("DATA",),
    "parallel": ("PARALLEL",),
    "submission": ("SUBMISSION",),
    "stop": ("STOP",),
    "pause": ("PAUSE",),
    "wait": ("WAIT",),
    "seed": ("SEED",),
    "reviewer_token": ("REVIEWER_TOKEN",),
    "bot_token": ("BOT_TOKEN",),
    "debug": ("DEBUG",),
    "debug_request": ("DEBUG_REQUEST", "DEBUG_REQ"),
    "debug_json_level": ("DEBUG_JSON_LEVEL",),
}

LIST_ARGS = frozenset({"data", "pause", "wait"})
INT_ARGS = frozenset({"acceleration", "seed", "debug_json_level", "parallel"})
BOOL_ARGS = frozenset({"debug", "debug_request"})
# Fill after parse so argparse extend actions do not append to env defaults.
EXTEND_ARGS = LIST_ARGS

TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
FALSE_VALUES = frozenset({"0", "false", "no", "off"})

REQUIRED_ARGS = (
    ("host", "host / --host / API_HOST"),
    ("token", "token / --token / API_TOKEN"),
    ("ds_host", "ds_host / --ds-host / DS_HOST"),
    ("ds_username", "ds_username / --ds-username / DS_USERNAME"),
    ("ds_password", "ds_password / --ds-password / DS_PASSWORD"),
)


class EnvFileNotFound(FileNotFoundError):
    def __init__(self, spec, tried, available):
        self.spec = spec
        self.tried = tried
        self.available = available
        tried_text = ", ".join(tried) if tried else "(none)"
        available_text = ", ".join(available) if available else "(none)"
        super().__init__(f"env file not found for {spec!r}. Tried: {tried_text}. Available: {available_text}")


class EnvValueError(ValueError):
    pass


def get_repo_root():
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.dirname(utils_dir)
    return os.path.dirname(package_dir)


def get_search_dirs(search_dirs=None):
    if search_dirs is not None:
        return [os.path.abspath(path) for path in search_dirs]
    dirs = [os.getcwd()]
    repo_root = get_repo_root()
    if os.path.abspath(repo_root) not in [os.path.abspath(path) for path in dirs]:
        dirs.append(repo_root)
    return dirs


def parse_env_content(text):
    result = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        result[key] = _unquote_env_value(value.strip())
    return result


def _unquote_env_value(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def load_env_file(path):
    with open(path, encoding="utf-8") as env_file:
        return parse_env_content(env_file.read())


def _is_example_env(filename):
    return filename.endswith(EXAMPLE_SUFFIXES)


def _env_name_from_filename(filename):
    if _is_example_env(filename):
        return None
    if filename == DEFAULT_ENV_FILE:
        return DEFAULT_ENV_FILE
    if filename.startswith(".env."):
        return filename[len(".env.") :]
    if filename.endswith(".env"):
        return filename[: -len(".env")]
    return filename


def list_available_envs(search_dirs=None):
    names = []
    seen = set()
    for directory in get_search_dirs(search_dirs):
        for rel_dir in ("", "envs"):
            path = os.path.join(directory, rel_dir) if rel_dir else directory
            if not os.path.isdir(path):
                continue
            try:
                filenames = os.listdir(path)
            except OSError:
                continue
            for filename in filenames:
                file_path = os.path.join(path, filename)
                if not os.path.isfile(file_path):
                    continue
                name = _env_name_from_filename(filename)
                if not name or name in seen:
                    continue
                if not (
                    filename == DEFAULT_ENV_FILE
                    or filename.startswith(".env.")
                    or filename.endswith(".env")
                    or rel_dir == "envs"
                ):
                    continue
                seen.add(name)
                names.append(name)
    names.sort(key=lambda item: (item != DEFAULT_ENV_FILE, item))
    return names


def _candidate_paths(spec, search_dirs):
    if os.path.isabs(spec):
        return [spec]
    candidates = []
    for directory in search_dirs:
        candidates.extend(
            [
                os.path.join(directory, spec),
                os.path.join(directory, f".env.{spec}"),
                os.path.join(directory, f"{spec}.env"),
                os.path.join(directory, "envs", spec),
                os.path.join(directory, "envs", f".env.{spec}"),
                os.path.join(directory, "envs", f"{spec}.env"),
            ]
        )
    return candidates


def resolve_env_path(spec=None, search_dirs=None):
    dirs = get_search_dirs(search_dirs)
    if spec in (None, ""):
        for directory in dirs:
            path = os.path.join(directory, DEFAULT_ENV_FILE)
            if os.path.isfile(path):
                return os.path.abspath(path)
        return None

    if os.path.isfile(spec):
        return os.path.abspath(spec)

    tried = []
    for path in _candidate_paths(spec, dirs):
        abs_path = os.path.abspath(path)
        if abs_path not in tried:
            tried.append(abs_path)
        if os.path.isfile(path):
            return abs_path
    raise EnvFileNotFound(spec, tried, list_available_envs(search_dirs))


def _first_raw_value(keys, file_vars, environ):
    for key in keys:
        if key in file_vars and file_vars[key] != "":
            return file_vars[key]
    for key in keys:
        value = environ.get(key)
        if value:
            return value
    return None


def _parse_bool(dest, value):
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise EnvValueError(f"invalid boolean value for {dest}: {value!r}")


def _parse_int(dest, value):
    stripped = value.strip()
    if dest == "parallel" and stripped.lower() == "all":
        return 0
    try:
        return int(stripped)
    except (TypeError, ValueError):
        raise EnvValueError(f"invalid integer value for {dest}: {value!r}")


def _parse_list(value):
    parts = [part.strip() for part in re.split(r"[,\s]+", value.strip()) if part.strip()]
    return parts or None


def convert_env_value(dest, value):
    if dest in BOOL_ARGS:
        return _parse_bool(dest, value)
    if dest in INT_ARGS:
        return _parse_int(dest, value)
    if dest in LIST_ARGS:
        return _parse_list(value)
    return value


def build_env_values(file_vars, environ=None):
    environ = os.environ if environ is None else environ
    values = {}
    for dest, keys in ARG_ENV_KEYS.items():
        raw = _first_raw_value(keys, file_vars, environ)
        if raw is None:
            continue
        converted = convert_env_value(dest, raw)
        if converted is None:
            continue
        values[dest] = converted
    return values


def load_run_env(spec=None, environ=None, search_dirs=None):
    environ = os.environ if environ is None else environ
    if spec in (None, ""):
        spec = environ.get(ENV_SELECT_VAR) or None
    path = resolve_env_path(spec, search_dirs=search_dirs)
    file_vars = load_env_file(path) if path else {}
    return path, build_env_values(file_vars, environ)


def first_set(*values):
    for value in values:
        if value is not None and value != "":
            return value
    return None
