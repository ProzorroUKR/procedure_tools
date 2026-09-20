import os
from pathlib import Path

DATA_DIR_DEFAULT = "aboveThreshold"
DATA_SUB_DIR_DEFAULT = "data"


def get_project_dir() -> str:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(this_dir)


def get_default_data_path(data_dir: str) -> str:
    return os.path.join(get_project_dir(), DATA_SUB_DIR_DEFAULT, data_dir)


def get_default_data_dirs() -> list[str]:
    data_path = os.path.join(get_project_dir(), DATA_SUB_DIR_DEFAULT)
    return [
        item
        for item in os.listdir(data_path)
        if os.path.isdir(os.path.join(data_path, item)) and not item.startswith(("_", "."))
    ]


def get_data_path(path: str) -> str | None:
    """
    Resolve a data folder: an existing directory, a path relative to the current
    directory or the name of one of the bundled data folders.
    """
    if Path(path).is_dir():
        return path
    relative_path = os.path.join(os.getcwd(), path)
    if Path(relative_path).is_dir():
        return relative_path
    default_data_path = get_default_data_path(path)
    if Path(default_data_path).is_dir():
        return default_data_path
    return None
