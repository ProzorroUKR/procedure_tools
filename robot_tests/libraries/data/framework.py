"""
Framework payloads.

A framework is the agreement a later procedure buys under, so it carries no
items of its own by default - only what it is about, who runs it and how long
qualification stays open.
"""

from __future__ import annotations

from typing import Any

from data.common import (
    DEFAULT_ADDITIONAL_CLASSIFICATION,
    classification_data,
    contact_point_data,
    organization_data,
)
from data.utils import build, fake, from_now_iso

# Config of a dynamic purchasing system, as the bundled flows create it.
FRAMEWORK_CONFIG: dict[str, Any] = {
    "clarificationUntilDuration": 3,
    "hasItems": False,
    "qualificationComplainDuration": 0,
    "restrictedDerivatives": False,
}

# Two years, which is how long a dynamic purchasing system runs.
QUALIFICATION_DAYS = 366 * 2


def framework_procuring_entity_data(**kwargs: Any) -> dict[str, Any]:
    """
    The organization that runs the framework.

    Unlike a tender, a framework wants both ways of reaching it: the contact
    point has to carry an email as well as a web page.
    """
    organization = organization_data(kind="special", with_email=True)
    organization["contactPoint"] = contact_point_data(with_email=True, url=fake.url())
    return build(organization, **kwargs)


def framework_config_data(**kwargs: Any) -> dict[str, Any]:
    """The config block of a framework, with the named options changed."""
    return build(FRAMEWORK_CONFIG, **kwargs)


def framework_data(
    framework_type: str = "dynamicPurchasingSystem",
    procuring_entity: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
    acceleration: float | None = None,
    qualification_days: float = QUALIFICATION_DAYS,
    **kwargs: Any,
) -> dict[str, Any]:
    """A framework ready to be created."""
    details = f"quick, accelerator={int(acceleration)}" if acceleration else ""
    data: dict[str, Any] = {
        "additionalClassifications": [dict(DEFAULT_ADDITIONAL_CLASSIFICATION)],
        "classification": classification_data(),
        "description": fake.sentence(nb_words=8),
        "frameworkDetails": details,
        "frameworkType": framework_type,
        "procuringEntity": procuring_entity or framework_procuring_entity_data(),
        "qualificationPeriod": {"endDate": from_now_iso(acceleration=acceleration, days=qualification_days)},
        "title": fake.sentence(nb_words=6),
    }
    return {
        "config": config if config is not None else dict(FRAMEWORK_CONFIG),
        "data": build(data, **kwargs),
    }


def framework_patch_data(status: str, **kwargs: Any) -> dict[str, Any]:
    """A patch that moves the framework to ``status``."""
    return {"data": build({"status": status}, **kwargs)}
