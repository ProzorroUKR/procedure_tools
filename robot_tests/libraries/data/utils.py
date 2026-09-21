"""
Building blocks shared by the data modules.

Every builder follows the same shape: it fills in sensible defaults and takes
``**overrides`` that are merged on top, so a test tweaks one field without
restating the rest. Override keys may be dotted paths, which makes them usable
straight from a Robot Framework keyword call::

    ${tender}=    Дані Закупівлі    value.amount=200000    lots.0.title=Лот A
"""

from __future__ import annotations

import ast
import copy
from datetime import timedelta
from typing import Any
from uuid import uuid4

from procedure_tools.fake import fake, fake_en
from procedure_tools.utils import helpers

__all__ = [
    "apply_overrides",
    "build",
    "deep_merge",
    "fake",
    "fake_en",
    "from_date_iso",
    "from_now_iso",
    "new_id",
]


def new_id() -> str:
    """Identifier in the form the CDB uses for objects a client generates."""
    return uuid4().hex


def from_now_iso(acceleration: float | None = None, **kwargs: float) -> str:
    """ISO date ``kwargs`` from now, shortened by ``acceleration`` like the API does."""
    return helpers.from_now_iso(acceleration=acceleration or 1, **kwargs)


def from_date_iso(date: str, acceleration: float | None = None, **kwargs: float) -> str:
    """ISO date ``kwargs`` from ``date``, shortened by ``acceleration``."""
    return helpers.from_date_iso(date, acceleration=acceleration or 1, **kwargs)


def days(count: float, acceleration: float | None = None) -> timedelta:
    return timedelta(days=count) / (acceleration or 1)


def deep_merge(base: Any, patch: Any) -> Any:
    """
    ``patch`` merged into a copy of ``base``.

    Dictionaries merge key by key; anything else replaces what was there, so a
    list of items is swapped as a whole rather than merged element-wise.
    """
    if not isinstance(base, dict) or not isinstance(patch, dict):
        return copy.deepcopy(patch)
    merged = copy.deepcopy(base)
    for key, value in patch.items():
        merged[key] = deep_merge(merged.get(key), value) if isinstance(value, dict) else copy.deepcopy(value)
    return merged


def parse_value(value: Any) -> Any:
    """
    Robot passes plain ``key=value`` arguments as strings; read the ones that
    are JSON-ish (numbers, booleans, lists) back into Python values. A string
    that is not a literal stays a string, and a value that already came from a
    ``${variable}`` is left alone.
    """
    if not isinstance(value, str):
        return value
    text = value.strip()
    if text in ("None", "null"):
        return None
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return value


def _set_path(target: Any, path: list[str], value: Any) -> None:
    key: Any = path[0]
    if isinstance(target, list):
        key = int(key)
        while len(target) <= key:
            target.append({})
    if len(path) == 1:
        if isinstance(target, list):
            target[key] = value
        else:
            target[key] = value
        return
    if isinstance(target, list):
        child = target[key]
    else:
        child = target.get(key)
    if not isinstance(child, (dict, list)):
        child = [] if path[1].isdigit() else {}
        target[key] = child
    _set_path(child, path[1:], value)


def apply_overrides(data: dict[str, Any], overrides: dict[str, Any] | None) -> dict[str, Any]:
    """
    Apply ``overrides`` to a copy of ``data``.

    A key may be a plain field name or a dotted path into nested dictionaries
    and lists (``value.amount``, ``items.0.quantity``). A value of ``None``
    removes the field, which is how a test drops a default it does not want.
    """
    result = copy.deepcopy(data)
    for key, raw in (overrides or {}).items():
        value = parse_value(raw)
        path = key.split(".")
        if value is None and len(path) == 1:
            result.pop(path[0], None)
            continue
        if len(path) == 1 and isinstance(value, dict) and isinstance(result.get(path[0]), dict):
            result[path[0]] = deep_merge(result[path[0]], value)
            continue
        _set_path(result, path, value)
    return result


def build(defaults: dict[str, Any], overrides: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    """Defaults with the explicit ``overrides`` dictionary and ``kwargs`` paths applied."""
    result = deep_merge(defaults, overrides or {})
    return apply_overrides(result, kwargs)
