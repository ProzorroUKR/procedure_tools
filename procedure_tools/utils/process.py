import json
import logging
import math
import os
from datetime import timedelta
from functools import partial
from mimetypes import MimeTypes
from time import sleep

from procedure_tools.utils.contextmanagers import open_file, read_file
from procedure_tools.utils.data import (
    TENDER_SECONDS_BUFFER,
    get_contracts_bids_ids,
    get_ids,
)
from procedure_tools.utils.date import fix_datetime, get_utcnow, parse_date
from procedure_tools.utils.file import (
    get_data_all_files,
    get_data_file_path,
    get_data_path,
)
from procedure_tools.utils.handlers import (
    allow_error_handler,
    auction_multilot_participation_url_success_handler,
    auction_participation_url_success_handler,
    bid_create_success_handler,
    contract_credentials_success_handler,
    default_success_handler,
    error,
    item_create_success_handler,
    item_patch_success_handler,
    plan_create_success_handler,
    plan_patch_success_handler,
    response_handler,
    tender_check_status_invalid_handler,
    tender_check_status_success_handler,
    tender_create_success_handler,
    tender_patch_success_handler,
    tender_post_complaint_success_handler,
    tender_post_criteria_success_handler,
    tender_post_plan_success_handler,
)

EDR_FILENAME = "edr_identification.yaml"


def get_bids(client, args, context, tender_id):
    logging.info("Check bids...\n")
    while True:
        response = client.get_tender_bids(tender_id, auth_token=args.token)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_bids(client, args, context, tender_id, bids_ids, bids_tokens, prefix=""):
    logging.info("Patching bids...\n")
    for bid_index, bid_id in enumerate(bids_ids):
        data_file = "{}bid_patch_{}.json".format(prefix, bid_index)
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            bid_patch_data = json.loads(content)
            client.patch_tender_bid(
                tender_id,
                bid_id,
                bids_tokens[bid_index],
                bid_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def post_bid_res(
    client,
    args,
    context,
    tender_id,
    bids_ids,
    bids_tokens,
    bids_documents,
    tender_criteria,
    prefix="",
):
    logging.info("Post bids requirement responses...\n")
    for bid_index, bid_id in enumerate(bids_ids):
        data_file = "{}bid_res_post_{}.json".format(prefix, bid_index)
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            bid_res_data = json.loads(content)
            for bid_res in bid_res_data["data"]:
                if "evidences" in bid_res:
                    for evidence in bid_res["evidences"]:
                        if evidence["type"] == "document":
                            bid_document = bids_documents[bid_index][0]
                            related_document = evidence["relatedDocument"]
                            related_document["id"] = bid_document["id"]
                            related_document["title"] = bid_document["title"]
                for tender_criteria_item in tender_criteria:
                    for group in tender_criteria_item["requirementGroups"]:
                        for req in group["requirements"]:
                            if bid_res["requirement"]["title"] == req["title"]:
                                bid_res["requirement"]["id"] = req["id"]

            client.post_tender_bid_res(
                tender_id,
                bid_id,
                bids_tokens[bid_index],
                bid_res_data,
                auth_token=args.token,
            )


def patch_agreements_contracts(
    client, args, context, tender_id, agreements_ids, tender_token
):
    response = get_bids(client, args, context, tender_id)
    bids_ids = get_ids(response)
    for agreement_index, agreement_id in enumerate(agreements_ids):
        response = get_agreement_contract(
            client, args, context, tender_id, agreement_id
        )
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
):
    logging.info("Patching agreement contracts...\n")
    for agreement_contract_index, agreement_contract_id in enumerate(
        agreement_contracts_ids
    ):
        bid_id = agreement_contracts_bids_ids[agreement_contract_index]
        index = bids_ids.index(bid_id)
        data_file_pattern = "agreement_contracts_patch_{}_{}.json"
        data_file = data_file_pattern.format(agreement_index, index)
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            agreement_contract_patch_data = json.loads(content)
            client.patch_tender_agreement_contract(
                tender_id,
                agreement_id,
                agreement_contract_id,
                tender_token,
                agreement_contract_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def patch_agreements(
    client, ds_client, args, context, tender_id, agreements_ids, tender_token, prefix=""
):
    logging.info("Patching agreements...\n")
    for agreement_index, agreement_id in enumerate(agreements_ids):
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith(prefix + "agreement_document"):
                ds_response = upload_document(
                    ds_client,
                    args,
                    context,
                    data_file,
                )
                if ds_response:
                    client.post_tender_agreement_document(
                        tender_id,
                        agreement_id,
                        tender_token,
                        {"data": ds_response.json()["data"]},
                        auth_token=args.token,
                    )
        data_file = "agreement_patch_{}.json".format(agreement_index)
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            agreement_patch_data = json.loads(content)
            client.patch_tender_agreement(
                tender_id,
                agreement_id,
                tender_token,
                agreement_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def get_agreement_contract(client, args, context, tender_id, agreement_id):
    logging.info("Checking agreement contracts...")
    while True:
        response = client.get_tender_agreement_contracts(tender_id, agreement_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def get_tender(client, args, context, tender_id):
    return client.get_tender(tender_id)


def get_agreements(client, args, context, tender_id):
    logging.info("Check agreements...\n")
    while True:
        response = client.get_tender_agreements(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def get_agreement(client, args, context, agreement_id):
    logging.info("Check agreement...\n")
    while True:
        response = client.get_agreement(
            agreement_id,
            auth_token=args.token,
            error_handler=default_success_handler,
        )
        if "data" not in response.json().keys():
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def get_contract(client, args, context, contract_id):
    logging.info("Check contract...\n")
    while True:
        response = client.get_contract(
            contract_id,
            auth_token=args.token,
            error_handler=default_success_handler,
        )
        if "data" not in response.json().keys():
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_contracts_buyer_signer_info(
    client, args, context, contracts_ids, contracts_tokens, prefix=""
):
    logging.info("Patching contracts buyers signer info...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        contract_token = contracts_tokens[contract_index]
        data_file = "{}contract_buyer_signer_info_patch_{}.json".format(
            prefix,
            contract_index,
        )
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            contract_patch_data = json.loads(content)
            client.patch_contract_buyer_signer_info(
                contract_id,
                contract_token,
                contract_patch_data,
                auth_token=args.token,
                success_handler=default_success_handler,
            )


def patch_contracts_suppliers_signer_info(
    client, args, context, contracts_ids, contracts_tokens, prefix=""
):
    logging.info("Patching contracts suppliers signer info...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        contract_token = contracts_tokens[contract_index]
        data_file = "{}contract_suppliers_signer_info_patch_{}.json".format(
            prefix,
            contract_index,
        )
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            contract_patch_data = json.loads(content)
            client.patch_contract_suppliers_signer_info(
                contract_id,
                contract_token,
                contract_patch_data,
                auth_token=args.token,
                success_handler=default_success_handler,
            )


def patch_contracts(client, args, context, contracts_ids, contracts_tokens, prefix=""):
    logging.info("Patching contracts...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        contract_token = contracts_tokens[contract_index]
        data_file = "{}contract_patch_{}.json".format(
            prefix,
            contract_index,
        )
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            contract_patch_data = json.loads(content)
            client.patch_contract(
                contract_id,
                contract_token,
                contract_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def patch_tender_qual(client, args, context, tender_id, tender_token):
    logging.info("Approving awards by switching to next status...\n")
    data_file = "tender_patch_qual.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender(
            tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_tender_waiting(client, args, context, tender_id, tender_token):
    logging.info("Finishing first stage by switching to next status...\n")
    data_file = "tender_patch_waiting.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender(
            tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_award(
    client,
    args,
    context,
    tender_id,
    awards_ids,
    tender_token,
    action_index=0,
    prefix="",
):
    logging.info("Patching awards...\n")
    award_patch_data_files = []
    filename_base = "{}award_patch_{}".format(prefix, action_index)
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith(filename_base):
            award_patch_data_files.append(data_file)
    responses = []
    for data_file in award_patch_data_files:
        data_file_parts = data_file.split(".")
        if len(data_file_parts) != 2 and data_file_parts[-1] != "json":
            continue
        path = get_data_file_path(get_data_path(args.data), data_file)
        award_index = int(data_file_parts[0].split("_")[-1])
        awards_id = awards_ids[award_index]
        with read_file(path, context=context, exit_filename=args.stop) as content:
            award_patch_data = json.loads(content)
            response = client.patch_tender_award(
                tender_id,
                awards_id,
                tender_token,
                award_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )
            responses.append(response)
    return responses


def get_awards(client, args, context, tender_id):
    logging.info("Checking awards...\n")
    while True:
        response = client.get_tender_awards(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_tender_contracts(
    client, args, context, tender_id, contracts_ids, tender_token, prefix=""
):
    logging.info("Patching contracts...\n")
    for contract_index, contract_id in enumerate(contracts_ids):
        data_file = "{}contract_patch_{}.json".format(
            prefix,
            contract_index,
        )
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            contract_patch_data = json.loads(content)
            client.patch_tender_contract(
                tender_id,
                contract_id,
                tender_token,
                contract_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def get_tender_contracts(client, args, context, tender_id):
    logging.info("Checking contracts...\n")
    while True:
        response = client.get_tender_contracts(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_tender_pre(client, args, context, tender_id, tender_token, prefix=""):
    logging.info("Approving qualifications by switching to next status...\n")
    data_file = "{}tender_patch_pre.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender(
            tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_qualifications(
    client,
    args,
    context,
    tender_id,
    qualifications_ids,
    tender_token,
    prefix="",
):
    logging.info("Patching qualifications...\n")
    for qualification_index, qualification_id in enumerate(qualifications_ids):
        data_file = "{}qualification_patch_{}.json".format(
            prefix,
            qualification_index,
        )
        path = get_data_file_path(get_data_path(args.data), data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            qualification_patch_data = json.loads(content)
            client.patch_tender_qualification(
                tender_id,
                qualification_id,
                tender_token,
                qualification_patch_data,
                auth_token=args.token,
                success_handler=item_patch_success_handler,
            )


def get_qualifications(client, args, context, tender_id):
    logging.info("Checking qualifications...\n")
    while True:
        response = client.get_tender_qualifications(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def create_awards(client, args, context, tender_id, tender_token, prefix=""):
    logging.info("Creating awards...\n")
    award_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}award_create".format(prefix)):
            award_data_files.append(data_file)
    for award_data_file in award_data_files:
        path = get_data_file_path(get_data_path(args.data), award_data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            award_create_data = json.loads(content)
            client.post_tender_award(
                tender_id,
                tender_token,
                award_create_data,
                auth_token=args.token,
                success_handler=item_create_success_handler,
            )


def create_bids(client, ds_client, args, context, tender_id, prefix=""):
    logging.info("Creating bids...\n")
    bid_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}bid_create".format(prefix)):
            bid_data_files.append(data_file)
    responses = []
    for bid_data_file in bid_data_files:
        bid_documents = []
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith("{}bid_document".format(prefix)):
                ds_response = upload_document(ds_client, args, context, data_file)
                if ds_response:
                    document_data = ds_response.json()["data"]
                    bid_documents.append(document_data)
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith("{}bid_confidential_document".format(prefix)):
                ds_response = upload_document(ds_client, args, context, data_file)
                if ds_response:
                    document_data = ds_response.json()["data"]
                    document_data["confidentiality"] = "buyerOnly"
                    document_data["confidentialityRationale"] = (
                        f"Some {'long ' * 10}rationale"
                    )
                    bid_documents.append(document_data)
        bid_eligibility_documents = []
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith("{}bid_eligibility_document".format(prefix)):
                ds_response = upload_document(ds_client, args, context, data_file)
                if ds_response:
                    document_data = ds_response.json()["data"]
                    bid_eligibility_documents.append(document_data)
        bid_financial_documents = []
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith("{}bid_financial_document".format(prefix)):
                ds_response = upload_document(ds_client, args, context, data_file)
                if ds_response:
                    document_data = ds_response.json()["data"]
                    bid_financial_documents.append(document_data)
        bid_qualification_documents = []
        for data_file in get_data_all_files(get_data_path(args.data)):
            if data_file.startswith("{}bid_qualification_document".format(prefix)):
                ds_response = upload_document(ds_client, args, context, data_file)
                if ds_response:
                    document_data = ds_response.json()["data"]
                    bid_qualification_documents.append(document_data)
        path = get_data_file_path(get_data_path(args.data), bid_data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            bid_create_data = json.loads(content)
            bid_create_data["data"]["documents"] = bid_documents
            bid_create_data["data"]["eligibilityDocuments"] = bid_eligibility_documents
            bid_create_data["data"]["financialDocuments"] = bid_financial_documents
            bid_create_data["data"][
                "qualificationDocuments"
            ] = bid_qualification_documents
            response = client.post_tender_bid(
                tender_id,
                bid_create_data,
                auth_token=args.token,
                success_handler=bid_create_success_handler,
            )
            responses.append(response)
    return responses


def upload_document(ds_client, args, context, filename):
    path = get_data_file_path(get_data_path(args.data), filename)
    with open_file(path, mode="rb") as f:
        mime = MimeTypes()
        mime_type = mime.guess_type(path)
        ds_response = ds_client.post_document_upload(
            {"file": (filename, f, mime_type[0])}
        )
        return ds_response


def create_plans(client, args, context, prefix=""):
    logging.info("Creating plans...\n")
    plan_data_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}plan_create".format(prefix)):
            plan_data_files.append(data_file)
    responses = []
    for plan_data_file in plan_data_files:
        path = get_data_file_path(get_data_path(args.data), plan_data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            plan_create_data = json.loads(content)
            response = client.post_plan(
                plan_create_data,
                auth_token=args.token,
                success_handler=plan_create_success_handler,
            )
            responses.append(response)
    return responses


def create_plan(client, args, context, prefix=""):
    logging.info("Creating plan...\n")
    data_file = "{}plan_create.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(
        path, context=context, exit_filename=args.stop, silent_error=True
    ) as content:
        plan_create_data = json.loads(content)
        response = client.post_plan(
            plan_create_data,
            auth_token=args.token,
            success_handler=plan_create_success_handler,
        )
        return response


def patch_plan(client, args, context, plan_id, plan_token, prefix=""):
    logging.info("Patching plan...\n")
    data_file = "{}plan_patch.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(
        path, context=context, exit_filename=args.stop, silent_error=True
    ) as content:
        plan_patch_data = json.loads(content)
        response = client.patch_plan(
            plan_id,
            plan_token,
            plan_patch_data,
            auth_token=args.token,
            success_handler=plan_patch_success_handler,
        )
        return response


def create_tender(
    client,
    ds_client,
    args,
    context,
    plan_id=None,
    prefix="",
):
    logging.info("Creating tender...\n")
    data_file = "{}tender_create.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_create_data = json.loads(content)
        if plan_id:
            response = client.post_plan_tender(
                plan_id,
                tender_create_data,
                auth_token=args.token,
                success_handler=tender_create_success_handler,
            )
        else:
            response = client.post_tender(
                tender_create_data,
                auth_token=args.token,
                success_handler=tender_create_success_handler,
            )

        return response


def upload_tender_documents(
    client, ds_client, args, context, tender_id, tender_token, prefix=""
):
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}tender_document".format(prefix)):
            ds_response = upload_document(
                ds_client,
                args,
                context,
                data_file,
            )
            if ds_response:
                data = ds_response.json()["data"]
                client.post_tender_document(
                    tender_id,
                    tender_token,
                    {"data": data},
                    auth_token=args.token,
                )


def upload_tender_notice(
    client, ds_client, args, context, tender_id, tender_token, prefix=""
):
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}tender_notice".format(prefix)):
            ds_response = upload_document(
                ds_client,
                args,
                context,
                data_file,
            )
            if ds_response:
                data = ds_response.json()["data"]
                data["documentType"] = "notice"
                response = client.post_tender_document(
                    tender_id,
                    tender_token,
                    {"data": data},
                    auth_token=args.token,
                )
                return response


def upload_evaluation_report(
    client, ds_client, args, context, tender_id, tender_token, prefix=""
):
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}evaluation_report".format(prefix)):
            ds_response = upload_document(
                ds_client,
                args,
                context,
                data_file,
            )
            if ds_response:
                data = ds_response.json()["data"]
                data["documentType"] = "evaluationReports"
                response = client.post_tender_document(
                    tender_id,
                    tender_token,
                    {"data": data},
                    auth_token=args.token,
                    error_handler=allow_error_handler,  # TODO: Remove after feature release
                )
                if not response.status_code == 201:
                    return  # TODO: Remove after feature release
                return response


def re_upload_evaluation_report(
    client,
    ds_client,
    args,
    context,
    tender_id,
    document_id,
    tender_token,
    prefix="",
):
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}evaluation_report".format(prefix)):
            ds_response = upload_document(
                ds_client,
                args,
                context,
                data_file,
            )
            if ds_response:
                data = ds_response.json()["data"]
                data["documentType"] = "evaluationReports"
                client.put_tender_document(
                    tender_id,
                    document_id,
                    tender_token,
                    {"data": data},
                    auth_token=args.token,
                    error_handler=allow_error_handler,  # TODO: Remove after feature release
                )


def wait(date_str, client_timedelta=timedelta(), date_info_str=None):
    now = fix_datetime(get_utcnow(), client_timedelta)
    date_timedelta = parse_date(date_str) - now
    delta_seconds = date_timedelta.total_seconds()
    date_seconds = math.ceil(delta_seconds) if delta_seconds > 0 else 0
    info_str = " for {}".format(date_info_str) if date_info_str else ""
    logging.info(
        "Waiting {} seconds{} - {}...\n".format(
            date_seconds,
            info_str,
            date_str,
        )
    )
    sleep(date_seconds)


def wait_status(
    client, args, context, tender_id, delay, status, fail_status=None, fallback=None
):
    logging.info("Waiting for {}...\n".format(status))
    status = [status] if not isinstance(status, list) else status
    fail_status = (
        [fail_status]
        if fail_status and not isinstance(fail_status, list)
        else fail_status
    )
    while True:
        response = client.get_tender(tender_id)
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


def patch_stage2_credentials(client, args, context, stage2_tender_id, tender_token):
    logging.info("Getting credentials for second stage...\n")
    data_file = "stage2_tender_credentials.json"
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender_credentials(
            stage2_tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_create_success_handler,
        )


def patch_contract_credentials(client, args, context, contract_id, tender_token):
    logging.info("Getting credentials for contract...\n")
    return client.patch_contract_credentials(
        contract_id,
        tender_token,
        {},
        auth_token=args.token,
        success_handler=contract_credentials_success_handler,
    )


def patch_tender_tendering(client, args, context, tender_id, tender_token, prefix=""):
    logging.info("Activating tender by switching to next status...\n")
    data_file = "{}tender_patch_tendering.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender(
            tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def patch_tender_pending(client, args, context, tender_id, tender_token, prefix=""):
    logging.info("Activating tender by switching to next status...\n")
    data_file = "{}tender_patch_pending.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender(
            tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def post_criteria(client, args, context, tender_id, tender_token, prefix=""):
    logging.info("Create tender criteria...\n")
    data_file = "{}criteria_create.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        criteria_data = json.loads(content)
        return client.post_tender_criteria(
            tender_id,
            tender_token,
            criteria_data,
            auth_token=args.token,
            success_handler=tender_post_criteria_success_handler,
        )


def patch_tender(client, args, context, tender_id, tender_token, prefix=""):
    logging.info("Patching tender...\n")
    data_file = "{}tender_patch.json".format(prefix)
    path = get_data_file_path(get_data_path(args.data), data_file)
    with read_file(path, context=context, exit_filename=args.stop) as content:
        tender_patch_data = json.loads(content)
        return client.patch_tender(
            tender_id,
            tender_token,
            tender_patch_data,
            auth_token=args.token,
            success_handler=tender_patch_success_handler,
        )


def wait_edr_pre_qual(client, args, context, tender_id):
    logging.info("Waiting for {} in qualifications documents...\n".format(EDR_FILENAME))
    response = get_qualifications(client, args, context, tender_id)
    for qualification in response.json()["data"]:
        while EDR_FILENAME not in [
            doc["title"] for doc in qualification.get("documents", [])
        ]:
            sleep(TENDER_SECONDS_BUFFER)
            qualification = client.get_tender_qualification(
                tender_id,
                qualification["id"],
            ).json()["data"]


def wait_edr_qual(client, args, context, tender_id):
    logging.info("Waiting for {} in awards documents...\n".format(EDR_FILENAME))
    response = get_awards(client, args, context, tender_id)
    for award in response.json()["data"]:
        while EDR_FILENAME not in [doc["title"] for doc in award.get("documents", [])]:
            sleep(TENDER_SECONDS_BUFFER)
            award = client.get_tender_award(tender_id, award["id"]).json()["data"]


def wait_auction_participation_urls(client, args, tender_id, bids):
    logging.info("Waiting for the auction participation urls...\n")
    active_bids = [bid for bid in bids if bid["data"].get("status") != "unsuccessful"]
    active_bids_ids = [bid["data"]["id"] for bid in active_bids]
    success_bids_ids = []
    success_lots_ids = {}
    while True:
        response = client.get_tender(tender_id)
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
            response = client.get_tender_bid(
                tender_id,
                bid_id,
                bid_token,
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
                            in [
                                lot
                                for lot in tender_data["lots"]
                                if lot["id"] == value["relatedLot"]
                            ][0].keys(),
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
        sleep(TENDER_SECONDS_BUFFER)


def post_tender_plan(
    client,
    args,
    context,
    tender_id,
    tender_token,
    plan_id,
    prefix="",
):
    logging.info("Connecting plan to tender...\n")
    tender_patch_data = {"data": {"id": plan_id}}
    return client.post_tender_plan(
        tender_id,
        tender_token,
        tender_patch_data,
        auth_token=args.token,
        success_handler=tender_post_plan_success_handler,
    )


def create_complaints(
    client,
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
        logging.info(
            "Skipping complaints creating: bot and reviewer tokens are required\n"
        )
        return

    if obj_type == "award":
        logging.info("Creating award {} complaints...\n".format(obj_id))
        filename_base = "award_complaint_create_{}".format(obj_index)
    elif obj_type == "qualification":
        logging.info("Creating qualification {} complaints...\n".format(obj_id))
        filename_base = "qualification_complaint_create_{}".format(obj_index)
    else:
        logging.info("Creating complaints...\n")
        filename_base = "complaint_create"

    complaints_data_files = []
    data_path = get_data_path(
        os.path.join(args.data, "{}{}".format(prefix, file_subpath))
    )
    for data_file in get_data_all_files(data_path):
        if data_file.startswith(filename_base):
            complaints_data_files.append(data_file)
    responses = []
    for complaints_data_file in complaints_data_files:
        path = get_data_file_path(data_path, complaints_data_file)
        with read_file(path, context=context, exit_filename=args.stop) as content:
            complaints_create_data = json.loads(content)
            if obj_type == "award":
                response = client.post_tender_award_complaint(
                    tender_id,
                    obj_id,
                    acc_token,
                    complaints_create_data,
                    auth_token=args.token,
                    success_handler=tender_post_complaint_success_handler,
                )
            elif obj_type == "qualification":
                response = client.post_tender_qualification_complaint(
                    tender_id,
                    obj_id,
                    acc_token,
                    complaints_create_data,
                    auth_token=args.token,
                    success_handler=tender_post_complaint_success_handler,
                )
            else:
                response = client.post_tender_complaint(
                    tender_id,
                    acc_token,
                    complaints_create_data,
                    auth_token=args.token,
                    success_handler=tender_post_complaint_success_handler,
                )
            responses.append(response)
    return responses


def patch_complaints(
    client,
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
    def get_auth_token_for_role(role):
        if role == "bot":
            return args.bot_token
        elif role == "reviewer":
            return args.reviewer_token
        elif role == "tenderer":
            return args.token
        elif role == "complainer":
            return args.token
        else:
            error("Unknown role: {}".format(role))

    def get_access_token_for_role(role, tender_token, complaint_token):
        if role == "bot":
            return None
        elif role == "reviewer":
            return None
        elif role == "tenderer":
            return tender_token
        elif role == "complainer":
            return complaint_token
        else:
            error("Unknown role: {}".format(role))

    if not args.bot_token or not args.reviewer_token:
        logging.info(
            "Skipping complaints patching: bot and reviewer tokens are required\n"
        )
        return

    if obj_type == "award":
        logging.info("Patching award {} complaints...\n".format(obj_id))
        filename_base = "award_complaint_patch_{}".format(obj_index)
    elif obj_type == "qualification":
        logging.info("Patching qualification {} complaints...\n".format(obj_id))
        filename_base = "qualification_complaint_patch_{}".format(obj_index)
    else:
        logging.info("Patching complaints...\n")
        filename_base = "complaint_patch"

    for complaint_index, complaint_id in enumerate(complaints_ids):
        complaint_token = complaints_tokens[complaint_index]
        complaints_data_files = []
        data_path = get_data_path(
            os.path.join(args.data, "{}{}".format(prefix, file_subpath))
        )
        for data_file in get_data_all_files(data_path):
            if data_file.startswith(
                "{}_{}_".format(
                    filename_base,
                    complaint_index,
                )
            ):
                complaints_data_files.append(data_file)
        actions_count = len(complaints_data_files)
        for action_index in range(actions_count):
            complaints_action_data_files = []
            for data_file in get_data_all_files(data_path):
                if data_file.startswith(
                    "{}_{}_{}_".format(
                        filename_base,
                        complaint_index,
                        action_index,
                    )
                ):
                    complaints_action_data_files.append(data_file)
            for data_file in complaints_action_data_files:
                path = get_data_file_path(data_path, data_file)
                with read_file(
                    path, context=context, exit_filename=args.stop, silent_error=True
                ) as content:
                    complaint_patch_data = json.loads(content)
                    role = data_file.split(".")[-2].split("_")[-1]
                    role_auth_token = get_auth_token_for_role(role)
                    if not role_auth_token:
                        error("No auth token for role: {}".format(role))
                        continue
                    role_access_token = get_access_token_for_role(
                        role, tender_token, complaint_token
                    )
                    if obj_type == "award":
                        client.patch_tender_award_complaint(
                            tender_id,
                            obj_id,
                            complaint_id,
                            role_access_token,
                            complaint_patch_data,
                            auth_token=role_auth_token,
                            success_handler=item_patch_success_handler,
                        )
                    elif obj_type == "qualification":
                        client.patch_tender_qualification_complaint(
                            tender_id,
                            obj_id,
                            complaint_id,
                            role_access_token,
                            complaint_patch_data,
                            auth_token=role_auth_token,
                            success_handler=item_patch_success_handler,
                        )
                    else:
                        client.patch_tender_complaint(
                            tender_id,
                            complaint_id,
                            role_access_token,
                            complaint_patch_data,
                            auth_token=role_auth_token,
                            success_handler=item_patch_success_handler,
                        )
