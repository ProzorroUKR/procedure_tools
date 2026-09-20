"""
Data files define the flow.

Every ``.json`` file in a data folder is one action step:

    0010_action_name[_part[_part...]].json

- the leading number defines the order (files are processed sorted by name),
- ``action_name`` selects the action function (see ``tools.actions``),
- the remaining underscore separated parts are handed to the action, which
  decides what they mean (object index, role, sub-action, ...).

The number carries no meaning besides ordering, so any action can be placed at
any point of the flow. A label can precede the action name for readability, for
example ``4010_stage2_tender_patch.json`` or ``4020_selection_bid_create_0.json``:
when the stem does not start with a known action, leading ``label_`` tokens are
stripped until it does, and the label is kept as ``Step.prefix``.

The bundled folders share number ranges (0100 plan, 1000 framework, 2000 tender,
2200 bids, 2400 pre-qualification, 2600 awarding, 3000 contracts, 3300
agreements, 3900 finalization, +2000 for a second stage), see the README; the
runner itself only sorts by name.

Files with any other extension are resources (documents to upload) that action
files reference by title. A resource can carry a number prefix too, it is looked
up by its numberless name.
"""

from __future__ import annotations

import os
import re
from collections.abc import Collection
from dataclasses import dataclass
from typing import Any, TypeVar, overload

NUMBER_PREFIX_PATTERN = re.compile(r"^(\d+)_(.+)$")
ACTION_FILE_EXTENSION = ".json"

_MISSING = object()

_T = TypeVar("_T")


class StepError(ValueError):
    pass


def get_numberless_filename(filename: str) -> str:
    """
    >>> get_numberless_filename("0010_tender_create.json")
    'tender_create.json'
    >>> get_numberless_filename("tender_create.json")
    'tender_create.json'
    """
    match = NUMBER_PREFIX_PATTERN.match(filename)
    return match.group(2) if match else filename


def is_action_file(filename: str) -> bool:
    return filename.endswith(ACTION_FILE_EXTENSION) and not filename.startswith(".")


@dataclass
class Step:
    number: str
    action: str
    parts: list[str]
    filename: str
    path: str
    prefix: str = ""

    @property
    def name(self) -> str:
        """Filename without the number prefix."""
        return get_numberless_filename(self.filename)

    @property
    def stem(self) -> str:
        """Prefix, action name and parts joined back together."""
        return self.prefix + "_".join([self.action, *self.parts])

    def part(self, position: int, default: str | None = None) -> str | None:
        if position < len(self.parts):
            return self.parts[position]
        return default

    @overload
    def index(self, position: int) -> int: ...

    @overload
    def index(self, position: int, default: _T) -> int | _T: ...

    def index(self, position: int, default: Any = _MISSING) -> Any:
        """Integer part at ``position``; error when missing (unless ``default`` given) or not a number."""
        value = self.part(position)
        if value is None:
            if default is _MISSING:
                raise StepError(f"{self.filename}: missing index part #{position + 1} for action {self.action!r}")
            return default
        if not value.isdigit():
            raise StepError(f"{self.filename}: part #{position + 1} must be an index, got {value!r}")
        return int(value)

    def matches(self, filename: str | None) -> bool:
        """True when ``filename`` names this step, with or without the number prefix."""
        if not filename:
            return False
        return filename == self.filename or get_numberless_filename(filename) == self.name


def split_action(stem: str, action_names: Collection[str]) -> tuple[str, list[str], str]:
    """
    Split a numberless file stem into the action name and its parts.

    The longest registered action name matching the beginning of the stem wins,
    so ``framework_qualification_patch_0`` resolves to ``framework_qualification_patch``
    even though ``framework`` alone would also match.

    A leading label that is not an action (``stage2_``, ``selection_``) is
    skipped and returned as the prefix.

    >>> split_action("award_patch_0", ["award_patch", "award_document_attach"])
    ('award_patch', ['0'], '')
    >>> split_action("tender_create", ["tender_create"])
    ('tender_create', [], '')
    >>> split_action("stage2_tender_create", ["tender_create"])
    ('tender_create', [], 'stage2_')
    """
    prefix = ""
    rest = stem
    while True:
        candidates = [name for name in action_names if rest == name or rest.startswith(name + "_")]
        if candidates:
            break
        token, separator, rest = rest.partition("_")
        if not separator or not rest:
            raise StepError(f"unknown action {stem!r}")
        prefix += token + separator
    action = max(candidates, key=len)
    rest = rest[len(action) :].lstrip("_")
    parts = rest.split("_") if rest else []
    return action, parts, prefix


def discover_steps(data_path: str, action_names: Collection[str]) -> list[Step]:
    """Build the ordered list of steps from the action files of ``data_path``."""
    steps: list[Step] = []
    for filename in sorted(os.listdir(data_path)):
        path = os.path.join(data_path, filename)
        if not is_action_file(filename) or not os.path.isfile(path):
            continue
        match = NUMBER_PREFIX_PATTERN.match(filename)
        if not match:
            raise StepError(
                f"{filename}: action files must start with a number prefix that defines the order, "
                f"for example 0010_{filename}"
            )
        number, rest = match.groups()
        stem = rest[: -len(ACTION_FILE_EXTENSION)]
        try:
            action, parts, prefix = split_action(stem, action_names)
        except StepError:
            available = "\n".join(f" - {name}" for name in sorted(action_names))
            raise StepError(f"{filename}: unknown action {stem!r}. Available actions:\n{available}") from None
        steps.append(Step(number=number, action=action, parts=parts, filename=filename, path=path, prefix=prefix))
    return steps


def find_resource_path(data_path: str, title: str) -> str | None:
    """Find a resource file by its title, ignoring an optional number prefix on disk."""
    exact_path = os.path.join(data_path, title)
    if os.path.isfile(exact_path):
        return exact_path
    for filename in sorted(os.listdir(data_path)):
        path = os.path.join(data_path, filename)
        if get_numberless_filename(filename) == title and os.path.isfile(path):
            return path
    return None
