"""
Feature payloads.

A feature is a non-price quality the bids are compared on: the tender declares
what may be offered and what each option is worth, and every bid answers with
the option it offers. The answers are the ``parameters`` of a bid, and a bid
that leaves one out is refused.
"""

from __future__ import annotations

from typing import Any

from data.utils import build, new_id

# What a feature can be about.
FEATURE_OF = ("tenderer", "lot", "item")


def feature_data(
    feature_of: str = "lot",
    related_item: str | None = None,
    title: str = "Розмір товару",
    values: list[float] | None = None,
    code: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    One feature, with the options a bid may choose between.

    The values are what each option adds to the score, so they are fractions
    and the best one is the largest.
    """
    if feature_of not in FEATURE_OF:
        raise ValueError(f"a feature is about one of {FEATURE_OF}, not {feature_of!r}")
    options = values if values is not None else [0.15, 0.1, 0.05]
    titles = ("Великий", "Середній", "Малий")
    data: dict[str, Any] = {
        "code": code or new_id(),
        "title": title,
        "description": title,
        "featureOf": feature_of,
        "enum": [{"title": titles[index % len(titles)], "value": value} for index, value in enumerate(options)],
    }
    if related_item:
        data["relatedItem"] = related_item
    return build(data, **kwargs)


def features_data(lot_id: str, item_id: str) -> list[dict[str, Any]]:
    """The pair of features the bundled above threshold flow declares."""
    return [
        feature_data(feature_of="lot", related_item=lot_id, title="Розмір товару"),
        feature_data(
            feature_of="item",
            related_item=item_id,
            title="Термін поставки",
            values=[0.05, 0.01, 0],
        ),
    ]


def parameters_data(features: list[dict[str, Any]], best: bool = False) -> list[dict[str, Any]]:
    """
    A bid's answer to every feature of the tender.

    Without ``best`` each feature is answered with its least valuable option,
    which is what a bid that competes on price alone would offer.
    """
    answers = []
    for feature in features:
        values = [option["value"] for option in feature["enum"]]
        answers.append({"code": feature["code"], "value": max(values) if best else min(values)})
    return answers
