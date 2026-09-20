"""
Tender criteria and the bid answers to them.

A criterion is built from the catalogue shape in ``criteria_templates`` with
fresh requirement ids, so nothing has to be kept in sync by hand. The bid
answers are then derived from the criteria the API returned, which is what
makes them match: the ids come from the tender itself, not from a fixture.

    ${criteria}=     Criteria Data              lots=${lots}
    ${posted}=       Post Tender Criteria       ${criteria}
    ${responses}=    Requirement Responses Data ${posted}
"""

from __future__ import annotations

import copy
from typing import Any

from data.criteria_templates import TEMPLATES
from data.utils import apply_overrides, new_id

# Criteria the procuring entity answers, never the bidder.
PROCURING_ENTITY_SOURCE = "procuringEntity"

# Criteria bound to a lot: one copy of each is needed per lot of the tender.
LOT_RELATED = tuple(key for key, template in TEMPLATES.items() if template.get("relatesTo") == "lot")

EXCLUSION = tuple(key for key in TEMPLATES if key.startswith("CRITERION.EXCLUSION."))
SELECTION = tuple(key for key in TEMPLATES if key.startswith("CRITERION.SELECTION."))
OTHER = tuple(key for key in TEMPLATES if key.startswith("CRITERION.OTHER."))


def classification_ids() -> list[str]:
    """Every classification id that can be built."""
    return list(TEMPLATES)


def criterion(classification_id: str, related_item: str | None = None, **kwargs: Any) -> dict[str, Any]:
    """
    One criterion, with a fresh id on every requirement.

    ``related_item`` binds a lot related criterion to a lot; without it such a
    criterion falls back to relating to the tender as a whole.
    """
    if classification_id not in TEMPLATES:
        raise ValueError(f"unknown criterion {classification_id!r}, see criteria.classification_ids()")
    data = copy.deepcopy(TEMPLATES[classification_id])
    data["classification"]["id"] = classification_id
    for group in data["requirementGroups"]:
        for requirement in group["requirements"]:
            requirement["id"] = new_id()
    if data.get("relatesTo") == "lot":
        if related_item:
            data["relatedItem"] = related_item
        else:
            data["relatesTo"] = "tender"
    return apply_overrides(data, kwargs)


def criteria_for(classification_ids_: list[str], lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """
    Build the named criteria, repeating the lot related ones for every lot.

    ``lots`` are the lots of the tender; each may be a lot dictionary or a
    plain lot id.
    """
    lot_ids = [lot["id"] if isinstance(lot, dict) else lot for lot in (lots or [])]
    result: list[dict[str, Any]] = []
    for classification_id in classification_ids_:
        if classification_id in LOT_RELATED and lot_ids:
            result.extend(criterion(classification_id, related_item=lot_id) for lot_id in lot_ids)
        else:
            result.append(criterion(classification_id))
    return result


def exclusion_criteria(lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Grounds for refusing a bidder: convictions, unpaid taxes, bankruptcy."""
    return criteria_for(list(EXCLUSION), lots)


def selection_criteria(lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Qualification criteria: equipment, staff, experience, financial standing."""
    return criteria_for(list(SELECTION), lots)


def other_criteria(lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Bid language, guarantees and validity period; the guarantees are per lot."""
    return criteria_for(list(OTHER), lots)


def criteria_data(
    lots: list[dict[str, Any]] | None = None,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
) -> dict[str, Any]:
    """
    The criteria payload of a tender.

    By default every criterion of the catalogue is built. ``include`` narrows
    that to the named classification ids, ``exclude`` drops some of them.
    """
    selected = list(include) if include else list(TEMPLATES)
    if exclude:
        selected = [key for key in selected if key not in set(exclude)]
    return {"data": criteria_for(selected, lots)}


# --- bid answers


def requirement_value(requirement: dict[str, Any]) -> dict[str, Any]:
    """
    An answer that satisfies ``requirement``.

    Booleans answer what is expected of them, a choice answers with the
    allowed values, and a number answers with the highest value it may take,
    falling back to the lowest when there is no ceiling.
    """
    data_type = requirement.get("dataType")
    if data_type == "boolean":
        return {"value": requirement.get("expectedValue", True)}
    if data_type == "string":
        values = requirement.get("expectedValues") or [""]
        count = max(int(requirement.get("expectedMinItems", 1) or 1), 1)
        return {"values": values[:count]}
    if requirement.get("maxValue") is not None:
        return {"value": requirement["maxValue"]}
    if requirement.get("minValue") is not None:
        return {"value": requirement["minValue"]}
    return {"value": 0}


def requirement_evidences(requirement: dict[str, Any], document_title: str) -> list[dict[str, Any]]:
    """Answer evidences for the documents a requirement accepts as proof."""
    return [
        {
            "type": "document",
            "title": evidence.get("title") or "Підтвердний документ",
            "relatedDocument": {"title": document_title},
        }
        for evidence in requirement.get("eligibleEvidences") or []
        if evidence.get("type") == "document"
    ]


def requirement_responses_data(
    criteria: list[dict[str, Any]] | dict[str, Any],
    document_title: str | None = None,
) -> dict[str, Any]:
    """
    Answers to the criteria of the tender, as the bidder sends them.

    ``criteria`` is what the API returned when the criteria were posted, so
    every answer carries a requirement id that exists in the tender. Only the
    first requirement group of each criterion is answered - that is what
    picking one group means - and criteria the procuring entity answers are
    left out. Pass ``document_title`` to also send evidences pointing at a
    document of the bid.
    """
    if isinstance(criteria, dict):
        criteria = criteria.get("data", [])
    responses: list[dict[str, Any]] = []
    for item in criteria:
        if item.get("source") == PROCURING_ENTITY_SOURCE:
            continue
        groups = item.get("requirementGroups") or []
        if not groups:
            continue
        for requirement in groups[0].get("requirements") or []:
            response: dict[str, Any] = {"requirement": {"id": requirement["id"]}}
            response.update(requirement_value(requirement))
            if document_title:
                evidences = requirement_evidences(requirement, document_title)
                if evidences:
                    response["evidences"] = evidences
            responses.append(response)
    return {"data": responses}
