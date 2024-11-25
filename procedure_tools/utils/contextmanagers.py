import datetime
import io
import logging
import os
from contextlib import contextmanager
from functools import partial

from jinja2 import Template

from procedure_tools.fake import fake, fake_en
from procedure_tools.utils import helpers
from procedure_tools.utils.file import get_actual_file_path
from procedure_tools.utils.handlers import EX_OK
from procedure_tools.utils.style import fore_error


@contextmanager
def open_file(path, mode="r", encoding="UTF-8", exit_filename=None, silent_error=False, **kwargs):
    _, file_name = os.path.split(path)
    actual_path = get_actual_file_path(path)
    logging.info(f"Processing data file: {file_name}\n")
    try:
        encoding = encoding if "b" not in mode else None
        file = io.open(actual_path, mode, encoding=encoding, **kwargs)
        yield file
        file.close()
    except IOError as e:
        if not silent_error:
            msg = fore_error(str(e))
            msg += "\n"
            logging.info(msg)
        logging.info("Skipping...\n")
        yield
    except Exception:
        yield
    if file_name == exit_filename:
        raise SystemExit(EX_OK)


@contextmanager
def read_file(path, context=None, exit_filename=None, silent_error=False, **kwargs):
    context = context or {}
    with open_file(
        path,
        mode="r",
        encoding="UTF-8",
        exit_filename=exit_filename,
        silent_error=silent_error,
        **kwargs,
    ) as file:
        if not file:
            yield
        content = file.read()
        acceleration = context.get("acceleration", 1)
        client_timedelta = context.get("client_timedelta")
        context_fake = {
            "fake": fake,
            "fake_en": fake_en,
        }
        context_now = {
            "from_now": partial(
                helpers.from_now,
                acceleration=acceleration,
                client_timedelta=client_timedelta,
            ),
            "from_now_iso": partial(
                helpers.from_now_iso,
                acceleration=acceleration,
                client_timedelta=client_timedelta,
            ),
        }
        context_modules = {
            "datetime": datetime,
        }
        context.update(
            **context_fake,
            **context_now,
            **context_modules,
        )
        yield Template(content).render(context)
