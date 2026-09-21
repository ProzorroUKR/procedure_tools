"""
Question payloads.

A question is asked by a supplier during the enquiry period and answered by the
tender owner. It may be about the tender as a whole, about one lot or about one
item, which is what ``questionOf`` and ``relatedItem`` say.
"""

from __future__ import annotations

from typing import Any

from data.common import organization_data
from data.utils import build, fake

# What a question can be about.
QUESTION_OF = ("tender", "lot", "item")


def question_author_data(identifier_id: str = "00137256", **kwargs: Any) -> dict[str, Any]:
    """
    The supplier asking the question.

    It is an organization, not a tenderer: there is no bid behind it, so it
    carries no ``scale`` and the API refuses the field.
    """
    author = organization_data(kind=None, identifier_id=identifier_id)
    author["identifier"]["uri"] = fake.url()
    return build(author, **kwargs)


def question_data(
    question_of: str = "tender",
    related_item: str | None = None,
    author: dict[str, Any] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """A question from a supplier, about the tender or about one of its parts."""
    if question_of not in QUESTION_OF:
        raise ValueError(f"a question is about one of {QUESTION_OF}, not {question_of!r}")
    data: dict[str, Any] = {
        "author": author or question_author_data(),
        "title": fake.sentence(nb_words=6),
        "description": fake.paragraph(nb_sentences=2),
        "questionOf": question_of,
    }
    if related_item:
        data["relatedItem"] = related_item
    return {"data": build(data, **kwargs)}


def question_answer_data(answer: str | None = None, **kwargs: Any) -> dict[str, Any]:
    """The tender owner's answer."""
    return {"data": build({"answer": answer or fake.paragraph(nb_sentences=2)}, **kwargs)}
