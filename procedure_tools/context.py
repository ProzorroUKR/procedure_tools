import datetime
import json
import logging
from functools import partial

from jinja2 import Template

from procedure_tools.fake import fake, fake_en
from procedure_tools.steps import find_resource_path
from procedure_tools.utils import helpers
from procedure_tools.utils.handlers import error


class Context(dict):
    """
    State shared between actions.

    The dictionary part is what actions read and update: created objects
    (``tender``, ``bids``, ``contracts``, ...), their access tokens
    (``tender_token``, ``bids_tokens``, ...) and run settings (``acceleration``,
    ``submission``, ``constants``). The same dictionary is the template context
    of the data files, so ``{{ tender.id }}`` or ``{{ contracts[0].dateModified }}``
    resolve to whatever the previous actions stored.
    """

    def __init__(self, args, client, ds_client, data_path, steps):
        super().__init__()
        self.args = args
        self.client = client
        self.ds_client = ds_client
        self.data_path = data_path
        self.steps = steps
        self.step = None
        self.skip_steps = 0

    # --- templates

    def template_context(self):
        now_kwargs = {
            "acceleration": self.get("acceleration", 1),
            "client_timedelta": self.get("client_timedelta"),
        }
        return {
            **self,
            "fake": fake,
            "fake_en": fake_en,
            "from_date": partial(helpers.from_date, **now_kwargs),
            "from_date_iso": partial(helpers.from_date_iso, **now_kwargs),
            "from_now": partial(helpers.from_now, **now_kwargs),
            "from_now_iso": partial(helpers.from_now_iso, **now_kwargs),
            "datetime": datetime,
        }

    def render(self, content):
        return Template(content).render(self.template_context())

    def load(self, step=None):
        """Render the step data file as a template and parse it as JSON (empty file means ``{}``)."""
        step = step or self.step
        logging.info(f"Processing data file: {step.filename}\n")
        with open(step.path, encoding="utf-8") as file:
            content = file.read()
        rendered = self.render(content)
        if not rendered.strip():
            return {}
        try:
            return json.loads(rendered)
        except json.JSONDecodeError as e:
            error(f"{step.filename}: invalid JSON after rendering: {e}")

    def resource(self, title):
        """Path of a resource file (document to upload) referenced by an action file."""
        path = find_resource_path(self.data_path, title)
        if not path:
            step = self.step.filename if self.step else "context"
            error(f"{step}: resource file {title!r} not found in {self.data_path}")
        return path

    # --- lists

    def set_item(self, key, index, value):
        """Store ``value`` at ``index`` of the ``key`` list, growing the list with ``None`` when needed."""
        items = self.setdefault(key, [])
        while len(items) <= index:
            items.append(None)
        items[index] = value
        return value

    def item(self, key, index, hint=None):
        """Item at ``index`` of the ``key`` list; error when missing."""
        items = self.get(key) or []
        if index >= len(items) or items[index] is None:
            step = self.step.filename if self.step else "context"
            message = f"{step}: {key}[{index}] is not in context"
            if hint:
                message += f", {hint}"
            error(message)
        return items[index]

    def require(self, key, hint=None):
        """Value of ``key``; error when missing."""
        if self.get(key) is None:
            step = self.step.filename if self.step else "context"
            message = f"{step}: {key!r} is not in context"
            if hint:
                message += f", {hint}"
            error(message)
        return self[key]
