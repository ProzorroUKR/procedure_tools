import json
import logging
import math
import os
from datetime import timedelta
from functools import partial
from mimetypes import MimeTypes
from time import sleep

from procedure_tools.client import CDBClient, DSClient
from procedure_tools.utils.contextmanagers import open_file, read_file
from procedure_tools.utils.data import SECONDS_BUFFER, get_contracts_bids_ids, get_ids
from procedure_tools.utils.date import fix_datetime, get_utcnow, parse_date
from procedure_tools.utils.file import (
    generate_data_file_name,
    get_data_all_files,
    get_data_file_path,
    get_data_path,
    parse_data_file_parts,
)
from procedure_tools.utils.handlers import (
    agreement_get_success_handler,
    allow_null_success_handler,
    auction_multilot_participation_url_success_handler,
    auction_participation_url_success_handler,
    bid_create_success_handler,
    contract_credentials_success_handler,
    default_success_handler,
    document_attach_success_handler,
    error,
    framework_create_success_handler,
    framework_get_success_handler,
    framework_patch_success_handler,
    item_create_success_handler,
    item_patch_success_handler,
    plan_create_success_handler,
    plan_patch_success_handler,
    response_handler,
    submission_create_success_handler,
    tender_check_status_invalid_handler,
    tender_check_status_success_handler,
    tender_create_success_handler,
    tender_patch_success_handler,
    tender_post_complaint_success_handler,
    tender_post_criteria_success_handler,
    tender_post_plan_success_handler,
)

EDR_FILENAME = "edr_identification.yaml"


def get_bids(
    client: CDBClient,
    args,
    context,
    tender_id,
):
    logging.info("Check bids...\n")
    while True:
        response = client.get(f"tenders/{tender_id}/bids", auth_token=args.token)
        if not response.json()["data"]:
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def upload_bids_proposal(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    bids_ids,
    bids_tokens,
    prefix="",
):
    for bid_index, bid_id in enumerate(bids_ids):
        upload_bid_proposal(
            client,
            ds_client,
            args,
            context,
            tender_id,
            bid_id,
            bids_tokens[bid_index],
            f"bid_proposal_{bid_index}_attach",
            prefix=prefix,
        )


def patch_bids(
    client: CDBClient,
    args,
    context,
    tender_id,
    bids_ids,
    bids_tokens,
    prefix="",
):
    logging.info("Patching bids...\n")
    for bid_index, bid_id in enumerate(bids_ids):
        data_file = f"{prefix}bid_patch_{bid_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            bid_patch_data = json.loads(content)
            client.patch(
                f"tenders/{tender_id}/bids/{bid_id}",
                json=bid_patch_data,
                acc_token=bids_tokens[bid_index],
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def post_bid_res(
    client: CDBClient,
    args,
    context,
    tender_id,
    bids_ids,
    bids_tokens,
    bids_documents,
    prefix="",
):
    logging.info("Post bids requirement responses...\n")
    for bid_index, bid_id in enumerate(bids_ids):
        data_file = f"{prefix}bid_res_post_{bid_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            bid_res_data = json.loads(content)
            for bid_res in bid_res_data["data"]:
                if "evidences" in bid_res:
                    for evidence in bid_res["evidences"]:
                        if evidence["type"] == "document":
                            if bids_documents[bid_index]:
                                bid_document = bids_documents[bid_index][0]
                                related_document = evidence["relatedDocument"]
                                related_document["id"] = bid_document["id"]
                                related_document["title"] = bid_document["title"]

            client.post(
                f"tenders/{tender_id}/bids/{bid_id}/requirement_responses",
                json=bid_res_data,
                acc_token=bids_tokens[bid_index],
                auth_token=args.token,
            )


def patch_agreements_contracts(
    client: CDBClient,
    args,
    context,
    tender_id,
    agreements_ids,
    tender_token,
):
    response = get_bids(client, args, context, tender_id)
    bids_ids = get_ids(response)
    for agreement_index, agreement_id in enumerate(agreements_ids):
        response = get_agreement_contract(client, args, context, tender_id, agreement_id)
        agreement_contracts_ids = get_ids(response)
        agreement_contracts_bids_ids = get_contracts_bids_ids(response)

        patch_agreement_contract(
            client,
            args,
            context,
            tender_id,
            agreement_id,
            agreement_index,
            agreement_contracts_ids,
            bids_ids,
            agreement_contracts_bids_ids,
            tender_token,
        )


def patch_agreement_contract(
    client: CDBClient,
    args,
    context,
    tender_id,
    agreement_id,
    agreement_index,
    agreement_contracts_ids,
    bids_ids,
    agreement_contracts_bids_ids,
    tender_token,
):
    logging.info("Patching agreement contracts...\n")
    for agreement_contract_index, agreement_contract_id in enumerate(agreement_contracts_ids):
        bid_id = agreement_contracts_bids_ids[agreement_contract_index]
        index = bids_ids.index(bid_id)
        data_file = f"agreement_contracts_patch_{agreement_index}_{index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            agreement_contract_patch_data = json.loads(content)
            client.patch(
                f"tenders/{tender_id}/agreements/{agreement_id}/contracts/{agreement_contract_id}",
                json=agreement_contract_patch_data,
                acc_token=tender_token,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def patch_agreements(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    agreements_ids,
    tender_token,
    prefix="",
):
    logging.info("Patching agreements...\n")
    for agreement_index, agreement_id in enumerate(agreements_ids):
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith(prefix + "agreement_document"):
                ds_response = upload_document_ds(ds_client, args, context, data_file)
                if ds_response:
                    client.post(
                        f"tenders/{tender_id}/agreements/{agreement_id}/documents",
                        json={"data": ds_response.json()["data"]},
                        acc_token=tender_token,
                        auth_token=args.token,
                    )
        data_file = f"agreement_patch_{agreement_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            agreement_patch_data = json.loads(content)
            client.patch(
                f"tenders/{tender_id}/agreements/{agreement_id}",
                json=agreement_patch_data,
                acc_token=tender_token,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def get_agreement_contract(
    client: CDBClient,
    args,
    context,
    tender_id,
    agreement_id,
):
    logging.info("Checking agreement contracts...")
    while True:
        response = client.get(f"tenders/{tender_id}/agreements/{agreement_id}/contracts")
        if not response.json()["data"]:
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def get_tender(client: CDBClient, args, context, tender_id):
    return client.get(f"tenders/{tender_id}")


def get_agreements(client: CDBClient, args, context, tender_id):
    logging.info("Check agreements...\n")
    while True:
        response = client.get(f"tenders/{tender_id}/agreements")
        if not response.json()["data"]:
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def get_agreement(
    client: CDBClient,
    args,
    context,
    agreement_id,
):
    logging.info("Check agreement...\n")
    while True:
        response = client.get(
            f"agreements/{agreement_id}",
            auth_token=args.token,
            error_handler=default_success_handler,
        )
        if "data" not in response.json().keys():
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def get_contract(
    client: CDBClient,
    args,
    context,
    contract_id,
):
    logging.info("Check contract...\n")
    while True:
        response = client.get(
            f"contracts/{contract_id}",
            auth_token=args.token,
            error_handler=default_success_handler,
        )
        if "data" not in response.json().keys():
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def patch_contracts_buyer_signer_info(
    client: CDBClient,
    args,
    context,
    contracts_ids,
    contracts_tokens,
    prefix="",
):
    logging.info("Patching contracts buyers signer info...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        contract_token = contracts_tokens[contract_index]
        data_file = f"{prefix}contract_buyer_signer_info_patch_{contract_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            contract_patch_data = json.loads(content)
            client.put(
                f"contracts/{contract_id}/buyer/signer_info",
                json=contract_patch_data,
                acc_token=contract_token,
                auth_token=args.token,
                success_handler=default_success_handler,
            )


def patch_contracts_suppliers_signer_info(
    client: CDBClient,
    args,
    context,
    contracts_ids,
    contracts_tokens,
    prefix="",
):
    logging.info("Patching contracts suppliers signer info...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        contract_token = contracts_tokens[contract_index]
        data_file = f"{prefix}contract_suppliers_signer_info_patch_{contract_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            contract_patch_data = json.loads(content)
            client.put(
                f"contracts/{contract_id}/suppliers/signer_info",
                json=contract_patch_data,
                acc_token=contract_token,
                auth_token=args.token,
                success_handler=default_success_handler,
            )


def patch_contracts(
    client: CDBClient,
    args,
    context,
    contracts_ids,
    contracts_tokens,
    prefix="",
):
    logging.info("Patching contracts...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        contract_token = contracts_tokens[contract_index]
        data_file = f"{prefix}contract_patch_{contract_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args, silent_io_error=True) as content:
            contract_patch_data = json.loads(content)
            client.patch(
                f"contracts/{contract_id}",
                json=contract_patch_data,
                acc_token=contract_token,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def change_contracts(
    client: CDBClient,
    args,
    context,
    contracts_ids,
    contracts_tokens,
    action_index=0,
    prefix="",
):
    """
    Patch contracts by action index.

    Note: Contract change filename has the following format:
        contract_change_{action_index}_{contract_index}_{contract_change_action_index}.json
        contract_change_0_0_0.json
    """
    logging.info("Patching contracts...\n")

    contract_change_data_files = []
    action_name = "contract_change"
    filename_base = f"{prefix}{action_name}_{action_index}"
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(filename_base):
            contract_change_data_files.append(data_file)
    responses = []
    for data_file in contract_change_data_files:
        action_name, action_parts, action_extra, extension_parts = parse_data_file_parts(data_file, action_name, 3)

        contract_index = int(action_parts[1])

        if extension_parts[-1] == "json":
            if action_extra == "contract_patch":
                contract_id = contracts_ids[contract_index]
                contract_token = contracts_tokens[contract_index]
                path = get_data_file_path(get_data_path(args.data), data_file)
                with read_file(path, context=context, args=args) as content:
                    contract_patch_data = json.loads(content)
                    response = client.patch(
                        f"contracts/{contract_id}",
                        json=contract_patch_data,
                        acc_token=contract_token,
                        auth_token=args.token,
                        success_handler=item_patch_success_handler,
                    )
                responses.append(response)
                context["contracts"][contract_index] = response.json()["data"]
            elif action_extra == "change_post":
                contract_id = contracts_ids[contract_index]
                contract_token = contracts_tokens[contract_index]
                path = get_data_file_path(get_data_path(args.data), data_file)
                with read_file(path, context=context, args=args) as content:
                    contract_change_post_data = json.loads(content)
                    response = client.post(
                        f"contracts/{contract_id}/changes",
                        json=contract_change_post_data,
                        acc_token=contract_token,
                        auth_token=args.token,
                        success_handler=item_create_success_handler,
                    )
                responses.append(response)
                context["contracts"][contract_index] = get_contract(client, args, context, contract_id).json()["data"]
            elif action_extra.startswith("change_patch"):
                change_index = int(action_extra.split("_")[-1])
                change_id = context["contracts"][contract_index]["changes"][change_index]["id"]
                contract_id = contracts_ids[contract_index]
                contract_token = contracts_tokens[contract_index]
                path = get_data_file_path(get_data_path(args.data), data_file)
                with read_file(path, context=context, args=args) as content:
                    contract_change_patch_data = json.loads(content)
                    response = client.patch(
                        f"contracts/{contract_id}/changes/{change_id}",
                        json=contract_change_patch_data,
                        acc_token=contract_token,
                        auth_token=args.token,
                        success_handler=item_patch_success_handler,
                    )
                responses.append(response)
                context["contracts"][contract_index] = get_contract(client, args, context, contract_id).json()["data"]
    return responses


def get_contracts(client: CDBClient, args, context, contracts_ids):
    contracts = []
    for contracts_id in contracts_ids:
        response = get_contract(client, args, context, contracts_id)
        contracts.append(response.json()["data"])
    return contracts


def patch_tender_qual(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
):
    logging.info("Approving awards by switching to next status...\n")
    data_file = "tender_patch_qual.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{tender_id}",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_tender_waiting(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
):
    logging.info("Finishing first stage by switching to next status...\n")
    data_file = "tender_patch_waiting.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{tender_id}",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def upload_award_documents(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    award_id,
    tender_token,
    data_file_prefix,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        data_file_prefix=data_file_prefix,
        attach_callback=partial(
            client.post,
            f"tenders/{tender_id}/awards/{award_id}/documents",
            acc_token=tender_token,
        ),
        prefix=prefix,
    )


def patch_award(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    awards_ids,
    tender_token,
    action_index=0,
    prefix="",
):
    """
    Patch awards by action index.

    Note: Award filename has the following format:
        award_patch_{action_index}_{award_index}_{award_action_index}.json
        award_patch_0_0_0.json
    """
    logging.info("Patching awards...\n")
    award_patch_data_files = []
    action_name = "award_patch"
    filename_base = f"{prefix}{action_name}_{action_index}"
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(filename_base):
            award_patch_data_files.append(data_file)
    responses = []
    for data_file in award_patch_data_files:
        action_name, action_parts, action_extra, extension_parts = parse_data_file_parts(data_file, action_name, 3)

        # Award index is the second last part of the filename
        award_index = int(action_parts[1])

        # Get award id by index
        award_id = awards_ids[award_index]

        if action_extra == "document_attach":
            data_file_prefix = generate_data_file_name(action_name, action_parts, action_extra, extension_parts)
            upload_award_documents(
                client,
                ds_client,
                args,
                context,
                tender_id,
                award_id,
                tender_token,
                data_file_prefix=data_file_prefix,
                prefix=prefix,
            )
        elif extension_parts[-1] == "json":
            path = get_data_file_path(get_data_path(args.data), data_file)
            with read_file(path, context=context, args=args) as content:
                award_patch_data = json.loads(content)
                response = client.patch(
                    f"tenders/{tender_id}/awards/{award_id}",
                    json=award_patch_data,
                    acc_token=tender_token,
                    auth_token=args.token,
                    success_handler=allow_null_success_handler(
                        item_patch_success_handler,
                    ),
                )
                responses.append(response)
    return responses


def get_awards(
    client: CDBClient,
    args,
    context,
    tender_id,
):
    logging.info("Checking awards...\n")
    while True:
        response = client.get(f"tenders/{tender_id}/awards")
        if not response.json()["data"]:
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def get_tender_contracts(
    client: CDBClient,
    args,
    context,
    tender_id,
):
    logging.info("Checking contracts...\n")
    while True:
        response = client.get(f"tenders/{tender_id}/contracts")
        if not response.json()["data"]:
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def patch_tender_pre(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    logging.info("Approving qualifications by switching to next status...\n")
    data_file = f"{prefix}tender_patch_pre.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{tender_id}",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_qualifications(
    client: CDBClient,
    args,
    context,
    tender_id,
    qualifications_ids,
    tender_token,
    prefix="",
):
    logging.info("Patching qualifications...\n")
    for qualification_index, qualification_id in enumerate(qualifications_ids):
        data_file = f"{prefix}qualification_patch_{qualification_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            qualification_patch_data = json.loads(content)
            client.patch(
                f"tenders/{tender_id}/qualifications/{qualification_id}",
                json=qualification_patch_data,
                acc_token=tender_token,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def get_qualifications(client: CDBClient, args, context, tender_id):
    logging.info("Checking qualifications...\n")
    while True:
        response = client.get(f"tenders/{tender_id}/qualifications")
        if not response.json()["data"]:
            sleep(SECONDS_BUFFER)
        else:
            break
    return response


def create_awards(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    logging.info("Creating awards...\n")
    award_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(f"{prefix}award_create"):
            award_data_files.append(data_file)
    for award_data_file in award_data_files:
        path = get_data_file_path(get_data_path(args.data), award_data_file)
        with read_file(path, context=context, args=args) as content:
            award_create_data = json.loads(content)
            client.post(
                f"tenders/{tender_id}/awards",
                json=award_create_data,
                acc_token=tender_token,
                auth_token=args.token,
                success_handler=item_create_success_handler,
            )


def create_bids(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    prefix="",
):
    logging.info("Creating bids...\n")
    bid_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(f"{prefix}bid_create"):
            bid_data_files.append(data_file)
    responses = []
    for bid_data_file in bid_data_files:
        path = get_data_file_path(get_data_path(args.data), bid_data_file)
        with read_file(path, context=context, args=args) as content:
            bid_create_data = json.loads(content)
            for bid_document_container in (
                "documents",
                "eligibilityDocuments",
                "financialDocuments",
                "qualificationDocuments",
            ):
                bid_documents = []
                for bid_document_data in bid_create_data["data"].get(bid_document_container, []):
                    upload_file = bid_document_data["title"]
                    ds_response = upload_document_ds(ds_client, args, context, upload_file)
                    if ds_response:
                        document_data = ds_response.json()["data"]
                        document_data.update(bid_document_data)
                        bid_documents.append(document_data)
                if bid_documents:
                    bid_create_data["data"][bid_document_container] = bid_documents
            response = client.post(
                f"tenders/{tender_id}/bids",
                json=bid_create_data,
                auth_token=args.token,
                success_handler=bid_create_success_handler,
            )
            responses.append(response)
    return responses


def upload_document_ds(
    ds_client: DSClient,
    args,
    context,
    filename,
):
    path = get_data_file_path(get_data_path(args.data), filename)
    with open_file(path, mode="rb") as f:
        mime = MimeTypes()
        mime_type = mime.guess_type(path)
        ds_response = ds_client.post_document_upload({"file": (filename, f, mime_type[0])})
        return ds_response


def create_plans(
    client: CDBClient,
    args,
    context,
    prefix="",
):
    logging.info("Creating plans...\n")
    plan_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(f"{prefix}plan_create"):
            plan_data_files.append(data_file)
    responses = []
    for plan_data_file in plan_data_files:
        path = get_data_file_path(get_data_path(args.data), plan_data_file)
        with read_file(path, context=context, args=args) as content:
            plan_create_data = json.loads(content)
            response = client.post(
                "plans",
                json=plan_create_data,
                auth_token=args.token,
                success_handler=plan_create_success_handler,
            )
            responses.append(response)
    return responses


def create_plan(
    client: CDBClient,
    args,
    context,
    prefix="",
):
    logging.info("Creating plan...\n")
    data_file = f"{prefix}plan_create.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args, silent_io_error=True) as content:
        plan_create_data = json.loads(content)
        response = client.post(
            "plans",
            json=plan_create_data,
            auth_token=args.token,
            success_handler=plan_create_success_handler,
        )
        return response


def patch_plan(
    client: CDBClient,
    args,
    context,
    plan_id,
    plan_token,
    prefix="",
):
    logging.info("Patching plan...\n")
    data_file = f"{prefix}plan_patch.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args, silent_io_error=True) as content:
        plan_patch_data = json.loads(content)
        response = client.patch(
            f"plans/{plan_id}",
            json=plan_patch_data,
            acc_token=plan_token,
            auth_token=args.token,
            success_handler=plan_patch_success_handler,
        )
        return response


def create_framework(
    client: CDBClient,
    args,
    context,
    prefix="",
):
    logging.info("Creating framework...\n")
    data_file = f"{prefix}framework_create.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args, silent_io_error=True) as content:
        framework_create_data = json.loads(content)
        response = client.post(
            "frameworks",
            json=framework_create_data,
            auth_token=args.token,
            success_handler=framework_create_success_handler,
        )
        return response


def patch_framework_active(
    client: CDBClient,
    args,
    context,
    framework_id,
    framework_token,
    prefix="",
):
    logging.info("Activating framework by switching to next status...\n")
    data_file = f"{prefix}framework_patch_active.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        framework_patch_data = json.loads(content)
        return client.patch(
            f"frameworks/{framework_id}",
            json=framework_patch_data,
            acc_token=framework_token,
            auth_token=args.token,
            success_handler=framework_patch_success_handler,
        )


def create_sublissions(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    framework_id,
    prefix="",
):
    logging.info("Creating submissions...\n")
    submission_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(f"{prefix}submission_create"):
            submission_data_files.append(data_file)
    responses = []
    for submission_data_file in submission_data_files:
        path = get_data_file_path(get_data_path(args.data), submission_data_file)
        with read_file(path, context=context, args=args) as content:
            submission_create_data = json.loads(content)
            response = client.post(
                f"submissions",
                json=submission_create_data,
                auth_token=args.token,
                success_handler=submission_create_success_handler,
            )
            responses.append(response)
    return responses


def patch_submissions(
    client: CDBClient,
    args,
    context,
    submissions_ids,
    submissions_tokens,
    prefix="",
):
    logging.info("Patching submissions...\n")
    responses = []
    for submission_index, submission_id in enumerate(submissions_ids):
        data_file = f"{prefix}submission_patch_{submission_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            submission_patch_data = json.loads(content)
            response = client.patch(
                f"submissions/{submission_id}",
                json=submission_patch_data,
                acc_token=submissions_tokens[submission_index],
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )
            responses.append(response)
    return responses


def patch_framework_qualifications(
    client: CDBClient,
    args,
    context,
    qualifications_ids,
    framework_token,
    prefix="",
):
    logging.info("Patching qualifications...\n")
    responses = []
    for qualification_index, qualification_id in enumerate(qualifications_ids):
        data_file = f"{prefix}qualification_patch_{qualification_index}.json"
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, args=args) as content:
            qualification_patch_data = json.loads(content)
            response = client.patch(
                f"qualifications/{qualification_id}",
                json=qualification_patch_data,
                acc_token=framework_token,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )
            responses.append(response)
    return responses


def upload_qualification_evaluation_report(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    qualification_id,
    framework_token,
    data_file_prefix,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        data_file_prefix=data_file_prefix,
        attach_callback=partial(
            client.post,
            f"qualifications/{qualification_id}/documents",
            acc_token=framework_token,
        ),
        prefix=prefix,
    )


def upload_qualifications_evaluation_reports(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    qualifications_ids,
    framework_token,
    prefix="",
):
    for qualification_index, qualification_id in enumerate(qualifications_ids):
        upload_qualification_evaluation_report(
            client,
            ds_client,
            args,
            context,
            qualification_id,
            framework_token,
            f"qualification_evaluation_report_{qualification_index}_attach",
            prefix=prefix,
        )


def get_framework(
    client: CDBClient,
    args,
    context,
    framework_id,
):
    return client.get(
        f"frameworks/{framework_id}",
        success_handler=framework_get_success_handler,
    )


def create_tender(
    client: CDBClient,
    args,
    context,
    plan_id=None,
    prefix="",
):
    logging.info("Creating tender...\n")
    data_file = f"{prefix}tender_create.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_create_data = json.loads(content)
        if plan_id:
            response = client.post(
                f"plans/{plan_id}/tenders",
                json=tender_create_data,
                auth_token=args.token,
                success_handler=tender_create_success_handler,
            )
        else:
            response = client.post(
                "tenders",
                json=tender_create_data,
                auth_token=args.token,
                success_handler=tender_create_success_handler,
            )
        return response


def upload_documents(
    ds_client: DSClient,
    args,
    context,
    data_file_prefix,
    attach_callback,
    ignore_error=False,
    prefix="",
):
    responses = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(f"{prefix}{data_file_prefix}"):
            path = get_data_file_path(get_data_path(args.data), data_file)
            with read_file(path, context=context, args=args) as content:
                tender_document_data = json.loads(content)
                document_file = tender_document_data["data"]["title"]
                upload_file = f"{prefix}{document_file}"
                ds_response = upload_document_ds(ds_client, args, context, upload_file)
                if ds_response:
                    document_data = ds_response.json()["data"]
                    # apply data from data_file on top to add additional fields like documentType
                    document_data.update(tender_document_data["data"])
                    response = attach_callback(
                        json={"data": document_data},
                        auth_token=args.token,
                        success_handler=document_attach_success_handler,
                    )
                    if not ignore_error or ignore_error and 200 <= response.status_code < 300:
                        responses.append(response)
    return responses


def upload_tender_documents(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        data_file_prefix="tender_document_attach",
        attach_callback=partial(
            client.post,
            f"tenders/{tender_id}/documents",
            acc_token=tender_token,
        ),
        prefix=prefix,
    )


def upload_contract_proforma(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        data_file_prefix="contract_proforma_attach",
        attach_callback=partial(
            client.post,
            f"tenders/{tender_id}/documents",
            acc_token=tender_token,
        ),
        prefix=prefix,
    )


def upload_tender_notice(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        data_file_prefix="tender_notice_attach",
        attach_callback=partial(
            client.post,
            f"tenders/{tender_id}/documents",
            acc_token=tender_token,
        ),
        prefix=prefix,
    )


def upload_bid_proposal(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    bid_id,
    bid_token,
    data_file_prefix,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        data_file_prefix=data_file_prefix,
        attach_callback=partial(
            client.post,
            f"tenders/{tender_id}/bids/{bid_id}/documents",
            acc_token=bid_token,
        ),
        prefix=prefix,
    )


def upload_evaluation_report(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        "evaluation_report_attach",
        attach_callback=partial(
            client.post,
            f"tenders/{tender_id}/documents",
            acc_token=tender_token,
        ),
        prefix=prefix,
    )


def re_upload_evaluation_report(
    client: CDBClient,
    ds_client: DSClient,
    args,
    context,
    tender_id,
    document_id,
    tender_token,
    prefix="",
):
    return upload_documents(
        ds_client,
        args,
        context,
        "evaluation_report_attach",
        attach_callback=partial(
            client.put,
            f"tenders/{tender_id}/documents/{document_id}",
            acc_token=tender_token,
        ),
        prefix=prefix,
    )


def wait(
    date_str,
    client_timedelta=timedelta(),
    date_info_str=None,
):
    now = fix_datetime(get_utcnow(), client_timedelta)
    date_timedelta = parse_date(date_str) - now
    delta_seconds = date_timedelta.total_seconds()
    date_seconds = math.ceil(delta_seconds) if delta_seconds > 0 else 0
    info_str = f" for {date_info_str}" if date_info_str else ""
    logging.info(f"Waiting {date_seconds} seconds{info_str} - {date_str}...\n")
    sleep(date_seconds)


def wait_status(
    client: CDBClient,
    args,
    context,
    tender_id,
    delay,
    status,
    fail_status=None,
    fallback=None,
):
    logging.info(f"Waiting for {status}...\n")
    status = [status] if not isinstance(status, list) else status
    fail_status = [fail_status] if fail_status and not isinstance(fail_status, list) else fail_status
    while True:
        response = client.get(f"tenders/{tender_id}")
        current_status = response.json()["data"]["status"]
        if current_status not in status:
            if fail_status and current_status in fail_status:
                response_handler(
                    response,
                    success_handler=tender_check_status_invalid_handler,
                )
                error("Terminated.")
            if fallback:
                fallback()
            sleep(delay)
        else:
            response_handler(
                response,
                success_handler=tender_check_status_success_handler,
            )
            break
    return response


def patch_stage2_credentials(
    client: CDBClient,
    args,
    context,
    stage2_tender_id,
    tender_token,
):
    logging.info("Getting credentials for second stage...\n")
    data_file = "stage2_tender_credentials.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{stage2_tender_id}/credentials",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_create_success_handler,
        )


def patch_contract_credentials(
    client: CDBClient,
    args,
    context,
    contract_id,
    tender_token,
):
    logging.info("Getting credentials for contract...\n")
    return client.patch(
        f"contracts/{contract_id}/credentials",
        json={},
        acc_token=tender_token,
        auth_token=args.token,
        success_handler=contract_credentials_success_handler,
    )


def patch_tender_tendering(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    logging.info("Activating tender by switching to next status...\n")
    data_file = f"{prefix}tender_patch_tendering.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{tender_id}",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_tender_pending(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    logging.info("Activating tender by switching to next status...\n")
    data_file = f"{prefix}tender_patch_pending.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{tender_id}",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def post_criteria(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    logging.info("Create tender criteria...\n")
    data_file = f"{prefix}criteria_create.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args, silent_io_error=True) as content:
        criteria_data = json.loads(content)
        return client.post(
            f"tenders/{tender_id}/criteria",
            json=criteria_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_post_criteria_success_handler,
        )


def patch_tender(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    prefix="",
):
    logging.info("Patching tender...\n")
    data_file = f"{prefix}tender_patch.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, args=args) as content:
        tender_patch_data = json.loads(content)
        return client.patch(
            f"tenders/{tender_id}",
            json=tender_patch_data,
            acc_token=tender_token,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def wait_edr_pre_qual(
    client: CDBClient,
    args,
    context,
    tender_id,
):
    logging.info(f"Waiting for {EDR_FILENAME} in qualifications documents...\n")
    response = get_qualifications(client, args, context, tender_id)
    for qualification in response.json()["data"]:
        while EDR_FILENAME not in [doc["title"] for doc in qualification.get("documents", [])]:
            sleep(SECONDS_BUFFER)
            qualification = client.get(f"tenders/{tender_id}/qualifications/{qualification['id']}").json()["data"]


def wait_edr_qual(
    client: CDBClient,
    args,
    context,
    tender_id,
):
    logging.info(f"Waiting for {EDR_FILENAME} in awards documents...\n")
    response = get_awards(client, args, context, tender_id)
    for award in response.json()["data"]:
        while EDR_FILENAME not in [doc["title"] for doc in award.get("documents", [])]:
            sleep(SECONDS_BUFFER)
            award = client.get(f"tenders/{tender_id}/awards/{award['id']}").json()["data"]


def wait_auction_participation_urls(
    client: CDBClient,
    args,
    tender_id,
    bids,
):
    logging.info("Waiting for the auction participation urls...\n")
    active_bids = [bid for bid in bids if bid["data"].get("status") != "unsuccessful"]
    active_bids_ids = [bid["data"]["id"] for bid in active_bids]
    success_bids_ids = []
    success_lots_ids = {}
    while True:
        response = client.get(f"tenders/{tender_id}")
        tender_data = response.json()["data"]
        if set(success_bids_ids) == set(active_bids_ids):
            break
        for bid in active_bids:
            bid_id = bid["data"]["id"]
            bid_token = bid["access"]["token"]
            if bid_id in success_bids_ids:
                continue
            if bid_id not in success_lots_ids:
                success_lots_ids[bid_id] = []
            response = client.get(
                f"tenders/{tender_id}/bids/{bid_id}",
                acc_token=bid_token,
                auth_token=args.token,
            )
            data = response.json()["data"]
            participation_url_exists = lambda x: "participationUrl" in x
            if "lotValues" in response.json()["data"]:
                lot_values = data["lotValues"]
                active_lot_values = [
                    value
                    for value in lot_values
                    if all(
                        [
                            value.get("status", "active") in ("pending", "active"),
                            "auctionPeriod"
                            in [lot for lot in tender_data["lots"] if lot["id"] == value["relatedLot"]][0].keys(),
                        ]
                    )
                ]
                for lot_value in active_lot_values:
                    related_lot = lot_value["relatedLot"]
                    if related_lot in success_lots_ids[bid_id]:
                        continue
                    if participation_url_exists(lot_value):
                        success_lots_ids[bid_id].append(related_lot)
                        response_handler(
                            response,
                            success_handler=partial(
                                auction_multilot_participation_url_success_handler,
                                related_lot=related_lot,
                            ),
                        )
                if all(map(participation_url_exists, active_lot_values)):
                    success_bids_ids.append(bid_id)
            else:
                if participation_url_exists(data):
                    response_handler(
                        response,
                        success_handler=auction_participation_url_success_handler,
                    )
                    success_bids_ids.append(bid_id)
        sleep(SECONDS_BUFFER)


def post_tender_plan(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    plan_id,
    prefix="",
):
    logging.info("Connecting plan to tender...\n")
    tender_patch_data = {"data": {"id": plan_id}}
    return client.post(
        f"tenders/{tender_id}/plans",
        json=tender_patch_data,
        acc_token=tender_token,
        auth_token=args.token,
        success_handler=tender_post_plan_success_handler,
    )


def create_complaints(
    client: CDBClient,
    args,
    context,
    tender_id,
    acc_token,  # bid_token or tender_token
    obj_type=None,
    obj_index=None,
    obj_id=None,
    file_subpath="",
    prefix="",
):
    if not args.bot_token or not args.reviewer_token:
        logging.info("Skipping complaints creating: bot and reviewer tokens are required\n")
        return

    if obj_type == "award":
        logging.info(f"Creating award {obj_id} complaints...\n")
        filename_base = f"award_complaint_create_{obj_index}"
    elif obj_type == "qualification":
        logging.info(f"Creating qualification {obj_id} complaints...\n")
        filename_base = f"qualification_complaint_create_{obj_index}"
    else:
        logging.info("Creating complaints...\n")
        filename_base = "complaint_create"

    complaints_data_files = []
    data_path = get_data_path(os.path.join(args.data, f"{prefix}{file_subpath}"))
    for data_file in get_data_all_files(data_path):
        if data_file.startswith(filename_base):
            complaints_data_files.append(data_file)
    responses = []
    for complaints_data_file in complaints_data_files:
        path = get_data_file_path(data_path, complaints_data_file)
        with read_file(path, context=context, args=args) as content:
            complaints_create_data = json.loads(content)
            if obj_type == "award":
                response = client.post(
                    f"tenders/{tender_id}/awards/{obj_id}/complaints",
                    json=complaints_create_data,
                    acc_token=acc_token,
                    auth_token=args.token,
                    success_handler=tender_post_complaint_success_handler,
                )
            elif obj_type == "qualification":
                response = client.post(
                    f"tenders/{tender_id}/qualifications/{obj_id}/complaints",
                    json=complaints_create_data,
                    acc_token=acc_token,
                    auth_token=args.token,
                    success_handler=tender_post_complaint_success_handler,
                )
            else:
                response = client.post(
                    f"tenders/{tender_id}/complaints",
                    json=complaints_create_data,
                    acc_token=acc_token,
                    auth_token=args.token,
                    success_handler=tender_post_complaint_success_handler,
                )
            responses.append(response)
    return responses


def patch_complaints(
    client: CDBClient,
    args,
    context,
    tender_id,
    tender_token,
    complaints_ids,
    complaints_tokens,
    obj_type=None,
    obj_index=None,
    obj_id=None,
    file_subpath="",
    prefix="",
):
    def get_auth_token(role: str) -> str:
        tokens = {
            "bot": args.bot_token,
            "reviewer": args.reviewer_token,
            "tenderer": args.token,
            "complainer": args.token,
        }
        if role not in tokens:
            error(f"Unknown role: {role}")
        return tokens[role]

    def get_access_token(role: str, complaint_id: str) -> str:
        if role == "bot" or role == "reviewer":
            return None
        if role == "tenderer":
            return tender_token
        if role == "complainer":
            try:
                complaint_index = complaints_ids.index(complaint_id)
                return complaints_tokens[complaint_index]
            except ValueError:
                error(f"No token found for complaint ID: {complaint_id}")
                return None
        error(f"Unknown role: {role}")
        return None

    if not args.bot_token or not args.reviewer_token:
        logging.info("Skipping complaints patching: bot and reviewer tokens are required\n")
        return

    if obj_type == "award":
        logging.info(f"Patching award {obj_id} complaints...\n")
        filename_base = f"award_complaint_patch_{obj_index}"
    elif obj_type == "qualification":
        logging.info(f"Patching qualification {obj_id} complaints...\n")
        filename_base = f"qualification_complaint_patch_{obj_index}"
    else:
        logging.info("Patching complaints...\n")
        filename_base = "complaint_patch"

    for complaint_index, complaint_id in enumerate(complaints_ids):
        complaints_data_files = []
        data_path = get_data_path(os.path.join(args.data, f"{prefix}{file_subpath}"))
        for data_file in get_data_all_files(data_path):
            if data_file.startswith(f"{filename_base}_{complaint_index}_"):
                complaints_data_files.append(data_file)
        actions_count = len(complaints_data_files)
        for action_index in range(actions_count):
            complaints_action_data_files = []
            for data_file in get_data_all_files(data_path):
                if data_file.startswith(f"{filename_base}_{complaint_index}_{action_index}_"):
                    complaints_action_data_files.append(data_file)
            for data_file in complaints_action_data_files:
                path = get_data_file_path(data_path, data_file)
                with read_file(path, context=context, args=args, silent_io_error=True) as content:
                    complaint_patch_data = json.loads(content)
                    role = data_file.split(".")[-2].split("_")[-1]
                    role_auth_token = get_auth_token(role)
                    if not role_auth_token:
                        error(f"No auth token for role: {role}")
                        continue
                    role_access_token = get_access_token(role, complaint_id)
                    if obj_type == "award":
                        client.patch(
                            f"tenders/{tender_id}/awards/{obj_id}/complaints/{complaint_id}",
                            json=complaint_patch_data,
                            acc_token=role_access_token,
                            auth_token=role_auth_token,
                            success_handler=item_patch_success_handler,
                        )
                    elif obj_type == "qualification":
                        client.patch(
                            f"tenders/{tender_id}/qualifications/{obj_id}/complaints/{complaint_id}",
                            json=complaint_patch_data,
                            acc_token=role_access_token,
                            auth_token=role_auth_token,
                            success_handler=item_patch_success_handler,
                        )
                    else:
                        client.patch(
                            f"tenders/{tender_id}/complaints/{complaint_id}",
                            json=complaint_patch_data,
                            acc_token=role_access_token,
                            auth_token=role_auth_token,
                            success_handler=item_patch_success_handler,
                        )
