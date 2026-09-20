"""
Action registry.

An action is a function ``action(context, step)`` registered under the name
that data files use: ``0010_<name>[_parts].json``. The step carries the parts,
the context carries everything the previous actions produced.
"""

ACTIONS = {}


def action(name, description=None):
    def decorator(func):
        if name in ACTIONS:
            raise ValueError(f"Action {name!r} is already registered")
        func.action_name = name
        func.action_description = description or _first_line(func.__doc__)
        ACTIONS[name] = func
        return func

    return decorator


def _first_line(text):
    for line in (text or "").strip().splitlines():
        if line.strip():
            return line.strip()
    return ""


def format_actions():
    width = max(len(name) for name in ACTIONS) if ACTIONS else 0
    return "\n".join(f" - {name:<{width}}  {ACTIONS[name].action_description}" for name in sorted(ACTIONS))
