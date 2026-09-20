from __future__ import annotations

import argparse
import datetime
import json
import logging
from functools import partial
from typing import TYPE_CHECKING, Any, cast

from jinja2 import Template

from procedure_tools.fake import fake, fake_en
from procedure_tools.steps import find_resource_path
from procedure_tools.utils import helpers
from procedure_tools.utils.handlers import error

if TYPE_CHECKING:
    from procedure_tools.client import CDBClient, DSClient
    from procedure_tools.steps import Step

logger = logging.getLogger(__name__)


class Context(dict[str, Any]):
    """
    State shared between actions.

    The dictionary part is what actions read and update: created objects
    (``tender``, ``bids``, ``contracts``, ...), their access tokens
    (``tender_token``, ``bids_tokens``, ...) and run settings (``acceleration``,
    ``submission``, ``constants``). The same dictionary is the template context
    of the data files, so ``{{ tender.id }}`` or ``{{ contracts[0].dateModified }}``
    resolve to whatever the previous actions stored.
    """

    def __init__(
        self,
        args: argparse.Namespace,
        client: CDBClient,
        ds_client: DSClient,
        data_path: str | None,
        steps: list[Step],
    ) -> None:
        super().__init__()
        self.args = args
        self.client = client
        self.ds_client = ds_client
        self.data_path = data_path
        self.steps = steps
        self.step: Step | None = None
        self.skip_steps = 0
        self.allow_fail_next = False
        self.resources: dict[str, str] = {}
        """Resource files registered by title, looked up before ``data_path``."""

    # --- templates

    def template_context(self) -> dict[str, Any]:
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

    def render(self, content: str) -> str:
        template: Template = Template(content)
        return template.render(self.template_context())

    def render_data(self, data: Any) -> Any:
        """
        Copy ``data``, rendering the strings in it that hold a template.

        A caller that builds its payload in Python usually needs no templates,
        so only strings with ``{{`` or ``{%`` in them go through Jinja; the
        rest are left exactly as they are.
        """
        if isinstance(data, dict):
            return {key: self.render_data(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self.render_data(item) for item in data]
        if isinstance(data, str):
            return self.render(data) if ("{{" in data or "{%" in data) else data
        return data

    def load(self, step: Step | None = None) -> dict[str, Any]:
        """
        Data of the step: the inline data it carries, or its data file rendered
        as a template and parsed as JSON (an empty file means ``{}``).
        """
        step = step or self.step
        if step is None:
            raise ValueError("no step to load: pass a step or set context.step first")
        if step.data is not None:
            logger.info(f"Processing inline data: {step.stem}\n")
            return cast(dict[str, Any], self.render_data(step.data))
        if not step.path:
            raise ValueError(f"{step.filename}: the step has neither data nor a data file")
        logger.info(f"Processing data file: {step.filename}\n")
        with open(step.path, encoding="utf-8") as file:
            content = file.read()
        rendered = self.render(content)
        if not rendered.strip():
            return {}
        try:
            data: dict[str, Any] = json.loads(rendered)
        except json.JSONDecodeError as e:
            error(f"{step.filename}: invalid JSON after rendering: {e}")
            raise
        return data

    def resource(self, title: str) -> str:
        """Path of a resource file (document to upload) referenced by an action file."""
        if title in self.resources:
            return self.resources[title]
        path = find_resource_path(self.data_path, title) if self.data_path else None
        if path is None:
            step = self.step.filename if self.step else "context"
            error(f"{step}: resource file {title!r} not found in {self.data_path}")
            raise FileNotFoundError(title)
        return path

    # --- lists

    def set_item(self, key: str, index: int, value: Any) -> Any:
        """Store ``value`` at ``index`` of the ``key`` list, growing the list with ``None`` when needed."""
        items = self.setdefault(key, [])
        while len(items) <= index:
            items.append(None)
        items[index] = value
        return value

    def item(self, key: str, index: int, hint: str | None = None) -> Any:
        """Item at ``index`` of the ``key`` list; error when missing."""
        items = self.get(key) or []
        if index >= len(items) or items[index] is None:
            step = self.step.filename if self.step else "context"
            message = f"{step}: {key}[{index}] is not in context"
            if hint:
                message += f", {hint}"
            error(message)
        return items[index]

    def require(self, key: str, hint: str | None = None) -> Any:
        """Value of ``key``; error when missing."""
        if self.get(key) is None:
            step = self.step.filename if self.step else "context"
            message = f"{step}: {key!r} is not in context"
            if hint:
                message += f", {hint}"
            error(message)
        return self[key]
