"""
Helpers shared by the actions: waiting on the API, refreshing objects into the
context and uploading documents.
"""

import logging
from mimetypes import MimeTypes
from time import sleep as time_sleep

from procedure.utils.data import (
    SECONDS_BUFFER,
    get_access,
    get_config,
    get_data,
    get_token,
)
from procedure.utils.handlers import (
    default_success_handler,
    document_attach_success_handler,
    error,
)
from procedure.utils.runtime import get_controller
from procedure.utils.style import fore_warning

CONTRACT_ROLES = ("buyer", "supplier")


def sleep(seconds):
    controller = get_controller()
    if controller:
        controller.pause_aware_sleep(seconds)
    else:
        time_sleep(seconds)


def skip(message):
    logging.info(f"{fore_warning(message)}\n")


# --- polling


def has_items(response):
    return bool(response.json().get("data"))


def has_data(response):
    return "data" in response.json()


def get_until(context, path, ready=has_items, info=None, **kwargs):
    """GET ``path`` until ``ready(response)`` is true."""
    if info:
        logging.info(f"{info}\n")
    while True:
        response = context.client.get(path, **kwargs)
        if ready(response):
            return response
        sleep(SECONDS_BUFFER)


# --- tender


def tender_id(context):
    return context.require("tender", "run tender_create first")["id"]


def tender_token(context):
    return context.require("tender_token", "run tender_create first")


def set_tender(context, response):
    context["tender"] = get_data(response)
    access = get_access(response)
    if access.get("token"):
        context["tender_token"] = get_token(response)
    config = get_config(response)
    if config:
        context["tender_config"] = config
    return context["tender"]


def refresh_tender(context):
    response = context.client.get(f"tenders/{tender_id(context)}")
    context["tender"] = get_data(response)
    return response


# --- lists


def refresh_list(context, key, path, info=None, wait=True, **kwargs):
    """Refresh a tender sub-collection (awards, qualifications, ...) into ``context[key]``."""
    if wait:
        response = get_until(context, path, has_items, info=info, **kwargs)
    else:
        response = context.client.get(path, **kwargs)
    context[key] = response.json()["data"]
    return context[key]


def refresh_awards(context):
    return refresh_list(context, "awards", f"tenders/{tender_id(context)}/awards", "Checking awards...")


def refresh_qualifications(context):
    return refresh_list(
        context,
        "qualifications",
        f"tenders/{tender_id(context)}/qualifications",
        "Checking qualifications...",
    )


def refresh_agreements(context):
    return refresh_list(context, "agreements", f"tenders/{tender_id(context)}/agreements", "Checking agreements...")


def ensure(context, key, refresh):
    if context.get(key):
        return context[key]
    return refresh(context)


def ensure_awards(context):
    return ensure(context, "awards", refresh_awards)


def ensure_qualifications(context):
    return ensure(context, "qualifications", refresh_qualifications)


def ensure_agreements(context):
    return ensure(context, "agreements", refresh_agreements)


def ensure_bids(context):
    """Bids list; fetched without tokens when no bids were created in this run."""
    if context.get("bids"):
        return context["bids"]
    logging.info("Checking bids...\n")
    response = get_until(context, f"tenders/{tender_id(context)}/bids", auth_token=context.args.token)
    context["bids"] = response.json()["data"]
    return context["bids"]


def award(context, index):
    ensure_awards(context)
    return context.item("awards", index)


def qualification(context, index):
    ensure_qualifications(context)
    return context.item("qualifications", index)


def bid(context, index):
    return context.item("bids", index, hint=f"run tender_bid_create_{index} first")


def bid_token(context, index):
    return context.item("bids_tokens", index, hint=f"run tender_bid_create_{index} first")


# --- contracts


def get_contract(context, contract_id):
    return get_until(
        context,
        f"contracts/{contract_id}",
        has_data,
        info="Check contract...",
        auth_token=context.args.token,
        error_handler=default_success_handler,
    )


def refresh_contracts(context):
    response = get_until(context, f"tenders/{tender_id(context)}/contracts", info="Checking contracts...")
    contracts_ids = [item["id"] for item in response.json()["data"]]
    context["contracts"] = [get_data(get_contract(context, contract_id)) for contract_id in contracts_ids]
    return context["contracts"]


def ensure_contracts(context):
    return ensure(context, "contracts", refresh_contracts)


def contract(context, index):
    ensure_contracts(context)
    return context.item("contracts", index)


def refresh_contract(context, index):
    contract_id = contract(context, index)["id"]
    context["contracts"][index] = get_data(get_contract(context, contract_id))
    return context["contracts"][index]


def contract_role(step, position):
    """Optional ``buyer``/``supplier`` part at ``position`` (econtract flows)."""
    role = step.part(position)
    if role is None:
        return None
    if role not in CONTRACT_ROLES:
        error(f"{step.filename}: expected contract role {CONTRACT_ROLES}, got {role!r}")
    return role


def contract_token(context, index, role=None):
    if role:
        key = f"contracts_{role}_tokens"
        hint = f"run contract_access_post_{index}_{role} first"
    else:
        key = "contracts_tokens"
        hint = f"run contract_credentials_patch_{index} first"
    return context.item(key, index, hint=hint)


# --- documents


def upload_ds(context, resource, title=None):
    """Upload the resource file to the document service under ``title`` (default: the resource name)."""
    path = context.resource(resource)
    mime_type = MimeTypes().guess_type(path)[0]
    with open(path, "rb") as file:
        return context.ds_client.post_document_upload({"file": (title or resource, file, mime_type)})


def attach_document(context, step, path, acc_token, method="post", data=None):
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
    response = request(
        path,
        json={"data": document_data},
        acc_token=acc_token,
        auth_token=context.args.token,
        success_handler=document_attach_success_handler,
    )
    return response
