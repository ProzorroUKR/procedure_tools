import os
from pathlib import Path

DATA_DIR_DEFAULT = "aboveThresholdUA"
DATA_SUB_DIR_DEFAULT = "data"


def get_data_file_path(filename, path):
    return os.path.join(path, filename)


def get_data_all_files(path):
    return sorted(os.listdir(path))


def get_project_dir():
    this_dir, _ = os.path.split(__file__)
    project_dir, _ = os.path.split(this_dir)
    return project_dir


def get_data_path(path):
    if Path(path).is_dir():
        return path
    relative_path = os.path.join(os.getcwd(), path)
    if Path(relative_path).is_dir():
        return relative_path
    default_data_path = get_default_data_path(path)
    if Path(default_data_path).is_dir():
        return default_data_path


def get_default_data_path(data_dir):
    project_dir = get_project_dir()
    return os.path.join(project_dir, DATA_SUB_DIR_DEFAULT, data_dir)


def get_default_data_dirs():
    project_dir = get_project_dir()
    data_path = os.path.join(project_dir, DATA_SUB_DIR_DEFAULT)
    return os.listdir(data_path)
