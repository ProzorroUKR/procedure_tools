"""
Documents.

A document payload names a file and says what kind of document it is; the file
itself is generated content, written to a temporary directory by the keyword
that uploads it. Nothing is read from a fixture folder.
"""

from __future__ import annotations

from typing import Any

from data.utils import build, fake

# Enough of a PKCS#7 envelope to look like a signature to anything that only
# checks the file, not the certificate chain behind it.
SIGNATURE_CONTENT = "-----BEGIN PKCS7-----\nMIIBc=\n-----END PKCS7-----\n"


def document_data(
    title: str = "document.txt",
    document_type: str | None = None,
    content: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    A document to attach, with the content that will be uploaded for it.

    The content travels next to the payload under ``contents``, keyed by file
    name; the keyword that uploads it writes the file and drops the key before
    the payload reaches the API.
    """
    data: dict[str, Any] = {"title": title}
    if document_type:
        data["documentType"] = document_type
    return {
        "data": build(data, **kwargs),
        "contents": {title: content if content is not None else f"{fake.sentence(nb_words=20)}\n"},
    }


def merge_contents(payload: dict[str, Any], documents: list[dict[str, Any]]) -> None:
    """Collect the files of ``documents`` into the ``contents`` of ``payload``."""
    contents = payload.setdefault("contents", {})
    for document in documents:
        contents.update(document.get("contents") or {})


def signature_document_data(title: str = "sign.p7s", **kwargs: Any) -> dict[str, Any]:
    """A notice signature, the document a procuring entity signs its decisions with."""
    return document_data(title=title, document_type="notice", content=SIGNATURE_CONTENT, **kwargs)


def contract_proforma_document_data(title: str = "contract_proforma.txt", **kwargs: Any) -> dict[str, Any]:
    """The draft contract published with the tender."""
    return document_data(title=title, document_type="contractProforma", **kwargs)


def proposal_document_data(title: str = "bid_proposal.p7s", **kwargs: Any) -> dict[str, Any]:
    """
    The signed proposal a bid has to carry before it can be submitted.

    The API asks for a pkcs7 signature here and reads the format off the file
    name, so the title has to keep its ``.p7s`` ending.
    """
    return document_data(title=title, document_type="proposal", content=SIGNATURE_CONTENT, **kwargs)
