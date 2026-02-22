import glob
import os
import re
from pathlib import Path

DATA_DIR_DEFAULT = "aboveThresholdUA"
DATA_SUB_DIR_DEFAULT = "data"

NUMBERED_PREFIX_LENGTH = 4


def get_data_file_path(path, filename):
    return os.path.join(path, filename)


def get_numberless_filename(filename):
    """
    Get the filename without the numbered prefix.

    Example:
        >>> get_numberless_filename('0100_tender_create.json')
        'tender_create.json'

    :param filename:
    :return:
    """
    pattern_str = f"^[0-9]{{{NUMBERED_PREFIX_LENGTH}}}_(.*)"  # ^[0-9]{4}_(.*)
    pattern = re.compile(pattern_str)
    match = pattern.match(filename)
    if match:
        return match.group(1)
    return filename


def get_data_all_files(path):
    actual_filenames = sorted(os.listdir(path))
    numberless_filenames = [get_numberless_filename(filename) for filename in actual_filenames]
    return numberless_filenames


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
    return None


def get_default_data_path(data_dir):
    project_dir = get_project_dir()
    return os.path.join(project_dir, DATA_SUB_DIR_DEFAULT, data_dir)


def get_default_data_dirs():
    project_dir = get_project_dir()
    data_path = os.path.join(project_dir, DATA_SUB_DIR_DEFAULT)
    return [
        item
        for item in os.listdir(data_path)
        if os.path.isdir(os.path.join(data_path, item)) and item != "__pycache__"
    ]


def get_actual_file_path(path):
    """
    Get the actual file path.

    Examples:

    This will search the file in the directory and return the actual path if the file have numbered prefix:
        >>> get_actual_file_path('/path/to/data/aboveThreshold/tender_create.json')
        '/path/to/data/aboveThreshold/0100_tender_create.json'

    Or the original path if the file doesn't have numbered prefix:
        >>> get_actual_file_path('/path/to/data/aboveThreshold/tender_create.json')
        '/path/to/data/aboveThreshold/tender_create.json'

    :param path:
    :return:
    """
    directory, filename = os.path.split(path)
    pattern_filename = "[0-9]" * NUMBERED_PREFIX_LENGTH + "_" + filename  # [0-9][0-9][0-9][0-9]_filename
    pattern_path = os.path.join(directory, pattern_filename)
    glob_paths = glob.glob(pattern_path)
    actual_path = glob_paths[0] if glob_paths else path
    return actual_path


def parse_data_file_parts(data_file, first_part, middle_parts_count):
    """
    Parse the data file parts.

    Example:
        >>> parse_data_file_parts("award_patch_0_0_0_document_attach.json", "award_patch", 3)
        ("award_patch", ["0", "0", "0"], "document_attach", ["json"])
    """
    # Result: ["award_patch_0_0_0_document_attach", "json"]
    data_file_parts = data_file.split(".")

    # Result: ["json"]
    extension_parts = data_file_parts[1:]

    # Result: "award_patch_0_0_0_document_attach"
    data_file_name = data_file_parts[0]

    # Result: "0_0_0_document_attach"
    middle_and_last_part = data_file_name.split(f"{first_part}_")[-1]

    # Result: ["0", "0", "0"]
    middle_parts = middle_and_last_part.split("_")[:middle_parts_count]

    # Result: "0_0_0"
    middle_part = "_".join(middle_parts)

    # Result: "document_attach"
    last_part = data_file_name.split(f"{first_part}_{middle_part}_")[-1]

    # Result: ("award_patch" ,["0", "0", "0"], "document_attach", ["json"])
    return first_part, middle_parts, last_part, extension_parts


def generate_data_file_name(first_part, middle_parts, last_part, extension_parts):
    middle_part = "_".join(middle_parts)
    extension_part = ".".join(extension_parts)
    return f"{first_part}_{middle_part}_{last_part}.{extension_part}"
