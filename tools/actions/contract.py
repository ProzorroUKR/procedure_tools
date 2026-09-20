"""
Contract actions.

Parts: ``[contract index, (change index,) (role)]``. The optional role
(``buyer`` or ``supplier``) selects the econtract access token obtained with
``contract_access_post``; without a role the legacy token obtained with
``contract_credentials_patch`` is used.

    2430_contract_patch_0.json                       legacy contract 0
    2430_contract_patch_0_buyer.json                 econtract contract 0 as buyer
    2440_contract_change_patch_0_1_supplier.json     change 1 of contract 0 as supplier
"""

import logging

from tools.actions.common import (
    attach_document,
    contract,
    contract_role,
    contract_token,
    ensure_awards,
    ensure_bids,
    refresh_contract,
    refresh_contracts,
    tender_token,
)
from tools.actions.registry import action
from tools.utils.data import get_token
from tools.utils.handlers import (
    contract_access_success_handler,
    contract_credentials_success_handler,
    contract_post_success_handler,
    default_success_handler,
    error,
    item_create_success_handler,
    item_patch_success_handler,
    signatory_post_success_handler,
)


def contract_ref(context, step):
    """(index, contract, token) for steps with parts [contract index, (role)]."""
    index = step.index(0)
    role = contract_role(step, 1)
    return index, contract(context, index), contract_token(context, index, role)


def change_ref(context, step):
    """(index, contract, change, token) for steps with parts [contract index, change index, (role)]."""
    index = step.index(0)
    change_index = step.index(1)
    role = contract_role(step, 2)
    contract_data = contract(context, index)
    changes = contract_data.get("changes") or []
    if change_index >= len(changes):
        error(f"{step.filename}: contract {index} has no change {change_index}")
    return index, contract_data, changes[change_index], contract_token(context, index, role)


def supplier_token(context, index, role):
    """Token of the supplier of contract ``index``: econtract role token or the token of the winning bid."""
    if role:
        return contract_token(context, index, role)
    award_id = contract(context, index).get("awardID")
    for award in ensure_awards(context):
        if award["id"] == award_id:
            for bid_index, bid in enumerate(ensure_bids(context)):
                if bid["id"] == award.get("bid_id"):
                    return context.item("bids_tokens", bid_index, hint=f"bid {bid_index} was not created in this run")
    error(f"{context.step.filename}: no bid token found for the supplier of contract {index}")


@action("tender_contracts_get")
def tender_contracts_get(context, step):
    """Load the tender contracts into contracts (GET tenders/{id}/contracts, then GET contracts/{id} for each)."""
    context.load(step)
    refresh_contracts(context)


@action("contract_credentials_patch")
def contract_credentials_patch(context, step):
    """Get the legacy contract token (PATCH contracts/{id}/credentials); parts: [contract index]; sets contracts_tokens[i]."""
    logging.info("Getting credentials for contract...\n")
    index = step.index(0)
    context.load(step)
    response = context.client.patch(
        f"contracts/{contract(context, index)['id']}/credentials",
        json={},
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=contract_credentials_success_handler,
    )
    context.set_item("contracts_tokens", index, get_token(response))
    refresh_contract(context, index)


@action("contract_access_post")
def contract_access_post(context, step):
    """Get an econtract token for a role (POST contracts/{id}/access); parts: [contract index, buyer|supplier]; sets contracts_<role>_tokens[i]."""
    index = step.index(0)
    role = contract_role(step, 1)
    if not role:
        error(f"{step.filename}: contract_access_post needs a role part: buyer or supplier")
    contract_data = contract(context, index)
    data = context.load(step)
    if not data:
        if role == "buyer":
            identifier = contract_data["buyer"]["identifier"]
        else:
            identifier = contract_data["suppliers"][0]["identifier"]
        data = {"data": {"identifier": identifier}}
    logging.info(f"Getting access for contract {contract_data['id']} for {role}...\n")
    response = context.client.post(
        f"contracts/{contract_data['id']}/access",
        json=data,
        acc_token=tender_token(context),
        auth_token=context.args.token,
        success_handler=contract_access_success_handler(role=role, contract_id=contract_data["id"]),
    )
    context.set_item(f"contracts_{role}_tokens", index, get_token(response))


@action("contract_patch")
def contract_patch(context, step):
    """Patch a contract (PATCH contracts/{id}); parts: [contract index, (role)]."""
    logging.info("Patching contract...\n")
    index, contract_data, token = contract_ref(context, step)
    data = context.load(step)
    context.client.patch(
        f"contracts/{contract_data['id']}",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    refresh_contract(context, index)


@action("contract_post")
def contract_post(context, step):
    """Create a contract (POST contracts) with the token of contract [index]; parts: [contract index, (role)]."""
    logging.info("Creating contract...\n")
    index, _, token = contract_ref(context, step)
    data = context.load(step)
    context.client.post(
        "contracts",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=contract_post_success_handler,
    )
    refresh_contract(context, index)


@action("contract_document_attach")
def contract_document_attach(context, step):
    """Attach a document to a contract (POST contracts/{id}/documents); parts: [contract index, (role)]."""
    logging.info("Uploading contract document...\n")
    index, contract_data, token = contract_ref(context, step)
    attach_document(context, step, f"contracts/{contract_data['id']}/documents", acc_token=token)
    refresh_contract(context, index)


@action("contract_buyer_signer_info_put")
def contract_buyer_signer_info_put(context, step):
    """Set the buyer signer info (PUT contracts/{id}/buyer/signer_info); parts: [contract index, (role)]."""
    logging.info("Setting contract buyer signer info...\n")
    index, contract_data, token = contract_ref(context, step)
    data = context.load(step)
    context.client.put(
        f"contracts/{contract_data['id']}/buyer/signer_info",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=default_success_handler,
    )
    refresh_contract(context, index)


@action("contract_suppliers_signer_info_put")
def contract_suppliers_signer_info_put(context, step):
    """Set the suppliers signer info (PUT contracts/{id}/suppliers/signer_info) with the winning bid token; parts: [contract index, (role)]."""
    logging.info("Setting contract suppliers signer info...\n")
    index = step.index(0)
    role = contract_role(step, 1)
    contract_data = contract(context, index)
    token = supplier_token(context, index, role)
    data = context.load(step)
    context.client.put(
        f"contracts/{contract_data['id']}/suppliers/signer_info",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=default_success_handler,
    )
    refresh_contract(context, index)


@action("contract_signatories_post")
def contract_signatories_post(context, step):
    """Sign a contract (POST contracts/{id}/signatories); parts: [contract index, (role)]."""
    logging.info("Signing contract...\n")
    index, contract_data, token = contract_ref(context, step)
    data = context.load(step)
    context.client.post(
        f"contracts/{contract_data['id']}/signatories",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=signatory_post_success_handler,
    )
    refresh_contract(context, index)


@action("contract_cancellation_post")
def contract_cancellation_post(context, step):
    """Cancel a contract (POST contracts/{id}/cancellations); parts: [contract index, (role)]."""
    logging.info("Cancelling contract...\n")
    index, contract_data, token = contract_ref(context, step)
    data = context.load(step)
    context.client.post(
        f"contracts/{contract_data['id']}/cancellations",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=item_create_success_handler,
    )
    refresh_contract(context, index)


@action("contract_change_post")
def contract_change_post(context, step):
    """Create a contract change (POST contracts/{id}/changes); parts: [contract index, (role)]."""
    logging.info("Creating contract change...\n")
    index, contract_data, token = contract_ref(context, step)
    data = context.load(step)
    context.client.post(
        f"contracts/{contract_data['id']}/changes",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=item_create_success_handler,
    )
    refresh_contract(context, index)


@action("contract_change_patch")
def contract_change_patch(context, step):
    """Patch a contract change (PATCH contracts/{id}/changes/{id}); parts: [contract index, change index, (role)]."""
    logging.info("Patching contract change...\n")
    index, contract_data, change, token = change_ref(context, step)
    data = context.load(step)
    context.client.patch(
        f"contracts/{contract_data['id']}/changes/{change['id']}",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=item_patch_success_handler,
    )
    refresh_contract(context, index)


@action("contract_change_document_attach")
def contract_change_document_attach(context, step):
    """Attach a document to a contract change (POST contracts/{id}/changes/{id}/documents); parts: [contract index, change index, (role)]."""
    logging.info("Uploading contract change document...\n")
    index, contract_data, change, token = change_ref(context, step)
    attach_document(
        context,
        step,
        f"contracts/{contract_data['id']}/changes/{change['id']}/documents",
        acc_token=token,
    )
    refresh_contract(context, index)


@action("contract_change_signatories_post")
def contract_change_signatories_post(context, step):
    """Sign a contract change (POST contracts/{id}/changes/{id}/signatories); parts: [contract index, change index, (role)]."""
    logging.info("Signing contract change...\n")
    index, contract_data, change, token = change_ref(context, step)
    data = context.load(step)
    context.client.post(
        f"contracts/{contract_data['id']}/changes/{change['id']}/signatories",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=signatory_post_success_handler,
    )
    refresh_contract(context, index)


@action("contract_change_cancellation_post")
def contract_change_cancellation_post(context, step):
    """Cancel a contract change (POST contracts/{id}/changes/{id}/cancellations); parts: [contract index, change index, (role)]."""
    logging.info("Cancelling contract change...\n")
    index, contract_data, change, token = change_ref(context, step)
    data = context.load(step)
    context.client.post(
        f"contracts/{contract_data['id']}/changes/{change['id']}/cancellations",
        json=data,
        acc_token=token,
        auth_token=context.args.token,
        success_handler=item_create_success_handler,
    )
    refresh_contract(context, index)
