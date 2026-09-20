"""
Action registry.

An action is a function ``action(context, step)`` registered under the name
that data files use: ``0010_<name>[_parts].json``. The step carries the parts,
the context carries everything the previous actions produced.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol, cast

if TYPE_CHECKING:
    from procedure_tools.context import Context
    from procedure_tools.steps import Step


class Action(Protocol):
    """A registered action: the action function plus its registry metadata."""

    action_name: str
    action_description: str

    def __call__(self, context: Context, step: Step) -> None: ...


ActionFunc = Callable[["Context", "Step"], None]

ACTIONS: dict[str, Action] = {}


def action(name: str, description: str | None = None) -> Callable[[ActionFunc], Action]:
    def decorator(func: ActionFunc) -> Action:
        if name in ACTIONS:
            raise ValueError(f"Action {name!r} is already registered")
        registered = cast(Action, func)
        registered.action_name = name
        registered.action_description = description or _first_line(func.__doc__)
        ACTIONS[name] = registered
        return registered

    return decorator


def _first_line(text: str | None) -> str:
    for line in (text or "").strip().splitlines():
        if line.strip():
            return line.strip()
    return ""


def format_actions() -> str:
    width = max(len(name) for name in ACTIONS) if ACTIONS else 0
    return "\n".join(f" - {name:<{width}}  {ACTIONS[name].action_description}" for name in sorted(ACTIONS))
