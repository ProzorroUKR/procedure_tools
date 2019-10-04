import os
import io

from contextlib import contextmanager

from procedure_tools.utils.handlers import EX_OK


@contextmanager
def open_file(
    path, mode='r', encoding='UTF-8',
    raise_filename=None,
    raise_exception=None,
    raise_exception_args=None,
    **kwargs
):
    _, file_name = os.path.split(path)
    print("Processing data file: {}\n".format(file_name))
    try:
        file = io.open(path, mode, encoding=encoding, **kwargs)
        yield file
        file.close()
    except Exception:
        raise
    if raise_exception and file_name == raise_filename:
        if raise_exception_args:
            raise raise_exception(*raise_exception_args)
        else:
            raise raise_exception


@contextmanager
def open_file_or_exit(path, mode='r', encoding='UTF-8', exit_filename=None, **kwargs):
    with open_file(
        path, mode, encoding,
        raise_filename=exit_filename,
        raise_exception=SystemExit,
        raise_exception_args=(EX_OK,),
        **kwargs
    ) as file:
        yield file


@contextmanager
def ignore(*exceptions):
    try:
        yield
    except exceptions:
        print('Skipping...')
        print('')
