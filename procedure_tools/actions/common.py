"""
Helpers shared by the actions: waiting on the API, refreshing objects into the
context and uploading documents.
"""

import logging
from collections.abc import Callable
from mimetypes import MimeTypes
from time import sleep as time_sleep
from typing import Any

from requests import Response

from procedure_tools.context import Context
from procedure_tools.steps import Step
from procedure_tools.utils.data import (
    SECONDS_BUFFER,
    get_access,
    get_config,
    get_data,
    get_token,
)
from procedure_tools.utils.handlers import (
    default_success_handler,
    document_attach_success_handler,
    error,
)
from procedure_tools.utils.runtime import get_controller
from procedure_tools.utils.style import fore_warning

logger = logging.getLogger(__name__)


CONTRACT_ROLES = ("buyer", "supplier")


def sleep(seconds: float) -> None:
    controller = get_controller()
    if controller:
        controller.pause_aware_sleep(seconds)
    else:
        time_sleep(seconds)


def skip(message: str) -> None:
    logger.info(f"{fore_warning(message)}\n")


# --- polling


def has_items(response: Response) -> bool:
    return bool(response.json().get("data"))


def has_data(response: Response) -> bool:
    return "data" in response.json()


def get_until(
    context: Context,
    path: str,
    ready: Callable[[Response], bool] = has_items,
    info: str | None = None,
    **kwargs: Any,
) -> Response:
    """GET ``path`` until ``ready(response)`` is true."""
    if info:
        logger.info(f"{info}\n")
    while True:
        response = context.client.get(path, **kwargs)
        if ready(response):
            return response
        sleep(SECONDS_BUFFER)


# --- tender


def tender_id(context: Context) -> str:
    value: str = context.require("tender", "run tender_create first")["id"]
    return value


def tender_token(context: Context) -> str:
    value: str = context.require("tender_token", "run tender_create first")
    return value


def set_tender(context: Context, response: Response) -> dict[str, Any]:
    tender: dict[str, Any] = get_data(response)
    context["tender"] = tender
    access = get_access(response)
    if access.get("token"):
        context["tender_token"] = get_token(response)
    config = get_config(response)
    if config:
        context["tender_config"] = config
    return tender


def refresh_tender(context: Context) -> Response:
    response = context.client.get(f"tenders/{tender_id(context)}")
    context["tender"] = get_data(response)
    return response


# --- lists


def refresh_list(
    context: Context,
    key: str,
    path: str,
    info: str | None = None,
    wait: bool = True,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """Refresh a tender sub-collection (awards, qualifications, ...) into ``context[key]``."""
    if wait:
        response = get_until(context, path, has_items, info=info, **kwargs)
    else:
        response = context.client.get(path, **kwargs)
    items: list[dict[str, Any]] = response.json()["data"]
    context[key] = items
    return items


def refresh_awards(context: Context) -> list[dict[str, Any]]:
    return refresh_list(context, "awards", f"tenders/{tender_id(context)}/awards", "Checking awards...")


def refresh_qualifications(context: Context) -> list[dict[str, Any]]:
    return refresh_list(
        context,
        "qualifications",
        f"tenders/{tender_id(context)}/qualifications",
        "Checking qualifications...",
    )


def refresh_agreements(context: Context) -> list[dict[str, Any]]:
    return refresh_list(context, "agreements", f"tenders/{tender_id(context)}/agreements", "Checking agreements...")


def ensure(
    context: Context,
    key: str,
    refresh: Callable[[Context], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] | None = context.get(key)
    if items:
        return items
    return refresh(context)


def ensure_awards(context: Context) -> list[dict[str, Any]]:
    return ensure(context, "awards", refresh_awards)


def ensure_qualifications(context: Context) -> list[dict[str, Any]]:
    return ensure(context, "qualifications", refresh_qualifications)


def ensure_agreements(context: Context) -> list[dict[str, Any]]:
    return ensure(context, "agreements", refresh_agreements)


def ensure_bids(context: Context) -> list[dict[str, Any]]:
    """Bids list; fetched without tokens when no bids were created in this run."""
    bids: list[dict[str, Any]] | None = context.get("bids")
    if bids:
        return bids
    logger.info("Checking bids...\n")
    response = get_until(context, f"tenders/{tender_id(context)}/bids", auth_token=context.args.token)
    bids = response.json()["data"]
    context["bids"] = bids
    return bids


def award(context: Context, index: int) -> dict[str, Any]:
    ensure_awards(context)
    item: dict[str, Any] = context.item("awards", index)
    return item


def qualification(context: Context, index: int) -> dict[str, Any]:
    ensure_qualifications(context)
    item: dict[str, Any] = context.item("qualifications", index)
    return item


def bid(context: Context, index: int) -> dict[str, Any]:
    item: dict[str, Any] = context.item("bids", index, hint=f"run tender_bid_create_{index} first")
    return item


def bid_token(context: Context, index: int) -> str:
    token: str = context.item("bids_tokens", index, hint=f"run tender_bid_create_{index} first")
    return token


# --- contracts


def get_contract(context: Context, contract_id: str) -> Response:
    return get_until(
        context,
        f"contracts/{contract_id}",
        has_data,
        info="Check contract...",
        auth_token=context.args.token,
        error_handler=default_success_handler,
    )


def refresh_contracts(context: Context) -> list[dict[str, Any]]:
    response = get_until(context, f"tenders/{tender_id(context)}/contracts", info="Checking contracts...")
    contracts_ids = [item["id"] for item in response.json()["data"]]
    contracts: list[dict[str, Any]] = [get_data(get_contract(context, contract_id)) for contract_id in contracts_ids]
    context["contracts"] = contracts
    return contracts


def ensure_contracts(context: Context) -> list[dict[str, Any]]:
    return ensure(context, "contracts", refresh_contracts)


def contract(context: Context, index: int) -> dict[str, Any]:
    ensure_contracts(context)
    item: dict[str, Any] = context.item("contracts", index)
    return item


def refresh_contract(context: Context, index: int) -> dict[str, Any]:
    contract_id = contract(context, index)["id"]
    contract_data: dict[str, Any] = get_data(get_contract(context, contract_id))
    context["contracts"][index] = contract_data
    return contract_data


def contract_role(step: Step, position: int) -> str | None:
    """Optional ``buyer``/``supplier`` part at ``position`` (econtract flows)."""
    role: str | None = step.part(position)
    if role is None:
        return None
    if role not in CONTRACT_ROLES:
        error(f"{step.filename}: expected contract role {CONTRACT_ROLES}, got {role!r}")
    return role


def contract_token(context: Context, index: int, role: str | None = None) -> str:
    if role:
        key = f"contracts_{role}_tokens"
        hint = f"run contract_access_post_{index}_{role} first"
    else:
        key = "contracts_tokens"
        hint = f"run contract_credentials_patch_{index} first"
    token: str = context.item(key, index, hint=hint)
    return token


# --- documents


def upload_ds(context: Context, resource: str, title: str | None = None) -> Response:
    """Upload the resource file to the document service under ``title`` (default: the resource name)."""
    path = context.resource(resource)
    mime_type = MimeTypes().guess_type(path)[0]
    with open(path, "rb") as file:
        return context.ds_client.post_document_upload({"file": (title or resource, file, mime_type)})


def attach_document(
    context: Context,
    step: Step,
    path: str,
    acc_token: str | None,
    method: str = "post",
    data: dict[str, Any] | None = None,
) -> Response:
    """
    Upload the document named in the step data file to the document service and
    attach it with ``method`` (``post`` to add, ``put`` to replace) to ``path``.
    """
    data = context.load(step) if data is None else data
    document = data["data"]
    # "file" names the resource on disk when it differs from the document title
    ds_response = upload_ds(context, data.get("file") or document["title"], title=document["title"])
    document_data = ds_response.json()["data"]
    # apply data from the data file on top to add fields like documentType
    document_data.update(document)
    request = getattr(context.client, method)
    response: Response = request(
        path,
        json={"data": document_data},
        acc_token=acc_token,
        auth_token=context.args.token,
        success_handler=document_attach_success_handler,
    )
    return response
