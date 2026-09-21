"""
Reading the config schemas.

``config_schemas`` holds what each procedure may put in its config. This module
is how a test asks the questions that matter: what does this procedure allow,
what does it take by default, and which keys are a real branch of behaviour
rather than a value the schema pins.
"""

from __future__ import annotations

from typing import Any

from data.config_schemas import SCHEMAS

TENDER = "TenderConfig"
FRAMEWORK = "FrameworkConfig"


def qualified(procedure: str, group: str = TENDER) -> str:
    """``aboveThreshold`` -> ``TenderConfig/aboveThreshold``."""
    return procedure if "/" in procedure else f"{group}/{procedure}"


def procedures(group: str = TENDER) -> list[str]:
    """The procedures of a group that have a config schema."""
    prefix = f"{group}/"
    return [name[len(prefix) :] for name in SCHEMAS if name.startswith(prefix)]


def config_schema(procedure: str, group: str = TENDER) -> dict[str, dict[str, Any]]:
    name = qualified(procedure, group)
    if name not in SCHEMAS:
        raise ValueError(f"no config schema for {name}, see data.config.procedures()")
    return SCHEMAS[name]


def config_defaults(procedure: str, group: str = TENDER) -> dict[str, Any]:
    """The config a procedure has when nothing is said about it."""
    return {key: entry["default"] for key, entry in config_schema(procedure, group).items()}


def config_options(key: str, procedure: str, group: str = TENDER) -> list[Any]:
    """What ``key`` may be set to in this procedure."""
    entry = config_schema(procedure, group).get(key)
    if entry is None:
        raise ValueError(f"{qualified(procedure, group)} has no config key {key!r}")
    return list(entry["options"] or [])


def is_variable(key: str, procedure: str, group: str = TENDER) -> bool:
    """True when the schema lets this procedure choose, rather than pinning a value."""
    entry = config_schema(procedure, group).get(key)
    return bool(entry and entry["options"] is not None and len(entry["options"]) > 1)


def variable_keys(procedure: str, group: str = TENDER) -> list[str]:
    """The config keys this procedure is free to choose."""
    return [key for key in config_schema(procedure, group) if is_variable(key, procedure, group)]


def variable_pairs(group: str | None = None) -> list[tuple[str, str, str]]:
    """
    Every ``(group, procedure, key)`` the schemas leave open.

    This is the whole config test space: a pair that is not here cannot be
    varied at all, and one that is here is a branch of behaviour nothing else
    covers unless a suite says so.
    """
    pairs: list[tuple[str, str, str]] = []
    for name, keys in SCHEMAS.items():
        schema_group, _, procedure = name.partition("/")
        if group and schema_group != group:
            continue
        for key, entry in keys.items():
            if entry["options"] is not None and len(entry["options"]) > 1:
                pairs.append((schema_group, procedure, key))
    return pairs


def procedures_varying(key: str, group: str = TENDER) -> list[str]:
    """The procedures that may choose ``key``; the rest have it pinned."""
    return [procedure for procedure in procedures(group) if is_variable(key, procedure, group)]
