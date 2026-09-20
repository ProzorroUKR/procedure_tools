from procedure.main import main as base_main
from tools.runner import process_tools
from tools.utils.file import DATA_DIR_DEFAULT, get_data_path, get_default_data_dirs


def main():
    """
    ``procedure-tools`` command.

    Same CLI, env files, parallel execution and summary as ``procedure``, but the
    data folders are processed by ``tools.runner``: the data files define the flow.
    """
    base_main(
        process=process_tools,
        get_data_dirs=get_default_data_dirs,
        resolve_data_path=get_data_path,
        data_dir_default=DATA_DIR_DEFAULT,
    )


if __name__ == "__main__":
    main()
