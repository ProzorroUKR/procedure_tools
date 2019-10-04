import json
import math

from datetime import datetime

from dateutil import parser, tz
from time import sleep

from procedure_tools.utils.contextmanagers import ignore, open_file_or_exit
from procedure_tools.utils.data import (
    TENDER_SECONDS_BUFFER,
    get_ids,
    get_items_ids,
    get_bids_ids,
    set_agreement_period,
    set_acceleration_data,
    set_agreement_id,
    set_tender_period_data,
    set_mode_data,
)
from procedure_tools.utils.file import get_data_file_path, get_data_path, get_data_all_files
from procedure_tools.utils.handlers import (
    item_patch_success_print_handler,
    tender_patch_status_success_print_handler,
    item_create_success_print_handler,
    bid_create_success_print_handler,
    tender_create_success_print_handler,
    response_handler,
    tender_check_status_success_print_handler,
    contract_credentials_success_print_handler,
    default_success_print_handler,
    plan_create_success_print_handler,
)


EDR_FILENAME = "edr_identification.yaml"


def get_bids(client, args, tender_id):
    while True:
        response = client.get_bids(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_agreements_with_contracts(client, args, tender_id, tender_token):
    print("Checking agreements...\n")
    response = get_agreements(client, args, tender_id)
    agreements_ids = get_ids(response)
    response = get_tender(client, args, tender_id)
    items_ids = get_items_ids(response)
    print("Check bids...\n")
    response = get_bids(client, args, tender_id)
    bids_ids = get_ids(response)
    for agreement_index, agreement_id in enumerate(agreements_ids):
        print("Checking agreement contracts...")

        response = get_agreement_contract(client, args, tender_id, agreement_id)
        agreement_contracts_ids = get_ids(response)
        agreement_contracts_related_bids = get_bids_ids(response)

        print("Patching agreement contracts...\n")
        patch_agreement_contract(
            client,
            args,
            tender_id,
            agreement_id,
            agreement_index,
            agreement_contracts_ids,
            bids_ids,
            agreement_contracts_related_bids,
            items_ids,
            tender_token,
        )
    print("Patching agreements...\n")
    patch_agreements(client, args, tender_id, agreements_ids, tender_token)


def patch_agreements(client, args, tender_id, agreements_ids, tender_token):
    for agreement_index, agreement_id in enumerate(agreements_ids):
        path = get_data_file_path("agreement_patch_{}.json".format(agreement_index), get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            agreement_patch_data = json.loads(f.read())
            set_agreement_period(agreement_patch_data)
            client.patch_agreement(
                tender_id,
                agreement_id,
                tender_token,
                agreement_patch_data,
                success_handler=item_patch_success_print_handler,
            )


def patch_agreement_contract(
    client,
    args,
    tender_id,
    agreement_id,
    agreement_index,
    agreement_contracts_ids,
    bids_ids,
    agreement_contracts_related_bids,
    items_ids,
    tender_token,
):
    for agreement_contract_index, agreement_contract_id in enumerate(agreement_contracts_ids):
        index = bids_ids.index(agreement_contracts_related_bids[agreement_contract_index])
        data_file = "agreement_{}_contracts_patch_{}.json".format(agreement_index, index)
        path = get_data_file_path(data_file, get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            agreement_contract_patch_data = json.loads(f.read())
            for item_index, items_id in enumerate(items_ids):
                agreement_contract_patch_data["data"]["unitPrices"][item_index]["relatedItem"] = items_id
            client.patch_agreement_contract(
                tender_id,
                agreement_id,
                agreement_contract_id,
                tender_token,
                agreement_contract_patch_data,
                success_handler=item_patch_success_print_handler,
            )


def get_agreement_contract(client, args, tender_id, agreement_id):
    while True:
        response = client.get_agreement_contracts(tender_id, agreement_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def get_tender(client, args, tender_id):
    return client.get_tender(tender_id)


def get_agreements(client, args, tender_id):
    while True:
        response = client.get_agreements(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def get_agreement(client, args, agreement_id):
    while True:
        response = client.get_agreement(agreement_id, error_handler=default_success_print_handler)
        if not "data" in response.json().keys():
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def get_contract(client, args, contract_id):
    while True:
        response = client.get_contract(contract_id, error_handler=default_success_print_handler)
        if not "data" in response.json().keys():
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_tender_qual(client, args, tender_id, tender_token):
    print("Approving awards by switching to next status...\n")
    path = get_data_file_path("tender_patch_qual.json", get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_patch_data = json.loads(f.read())
        return client.patch_tender(
            tender_id, tender_token, tender_patch_data, success_handler=tender_patch_status_success_print_handler
        )


def patch_tender_waiting(client, args, tender_id, tender_token):
    print("Finishing first stage by switching to next status...\n")
    path = get_data_file_path("tender_patch_waiting.json", get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_patch_data = json.loads(f.read())
        return client.patch_tender(
            tender_id, tender_token, tender_patch_data, success_handler=tender_patch_status_success_print_handler
        )


def patch_awards(client, args, tender_id, awards_ids, tender_token, filename_prefix=""):
    print("Patching awards...\n")
    for award_index, awards_id in enumerate(awards_ids):
        data_file = "{}award_patch_{}.json".format(filename_prefix, award_index)
        path = get_data_file_path(data_file, get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            award_patch_data = json.loads(f.read())
            client.patch_award(
                tender_id, awards_id, tender_token, award_patch_data, success_handler=item_patch_success_print_handler
            )


def get_awards(client, args, tender_id):
    print("Checking awards...\n")
    while True:
        response = client.get_awards(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_contracts(client, args, tender_id, awards_ids, tender_token, filename_prefix=""):
    print("Patching contracts...\n")
    for contract_index, contract_id in enumerate(awards_ids):
        data_file = "{}contract_patch_{}.json".format(filename_prefix, contract_index)
        path = get_data_file_path(data_file, get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            contract_patch_data = json.loads(f.read())
            client.patch_contract(
                tender_id,
                contract_id,
                tender_token,
                contract_patch_data,
                success_handler=item_patch_success_print_handler,
            )


def get_contracts(client, args, tender_id):
    print("Checking contracts...\n")
    while True:
        response = client.get_contracts(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def patch_tender_pre(client, args, tender_id, tender_token, filename_prefix=""):
    print("Approving qualifications by switching to next status...\n")
    path = get_data_file_path("{}tender_patch_pre.json".format(filename_prefix), get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_patch_data = json.loads(f.read())
        return client.patch_tender(
            tender_id, tender_token, tender_patch_data, success_handler=tender_patch_status_success_print_handler
        )


def patch_qualifications(client, args, tender_id, qualifications_ids, tender_token, filename_prefix=""):
    print("Patching qualifications...\n")
    for qualification_index, qualification_id in enumerate(qualifications_ids):
        data_file = "{}qualification_patch_{}.json".format(filename_prefix, qualification_index)
        path = get_data_file_path(data_file, get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            qualification_patch_data = json.loads(f.read())
            client.patch_qualification(
                tender_id,
                qualification_id,
                tender_token,
                qualification_patch_data,
                success_handler=item_patch_success_print_handler,
            )


def get_qualifications(client, args, tender_id):
    print("Checking qualifications...\n")
    while True:
        response = client.get_qualifications(tender_id)
        if not response.json()["data"]:
            sleep(TENDER_SECONDS_BUFFER)
        else:
            break
    return response


def create_awards(client, args, tender_id, tender_token):
    print("Creating awards...\n")
    award_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("award_create"):
            award_files.append(data_file)
    for award_file in award_files:
        path = get_data_file_path(award_file, get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            award_create_data = json.loads(f.read())
            client.post_award(
                tender_id, tender_token, award_create_data, success_handler=item_create_success_print_handler
            )


def create_bids(client, args, tender_id, filename_prefix=""):
    print("Creating bids...\n")
    bid_files = []
    for data_file in get_data_all_files(get_data_path(args.data)):
        if data_file.startswith("{}bid_create".format(filename_prefix)):
            bid_files.append(data_file)
    for bid_file in bid_files:
        path = get_data_file_path(bid_file, get_data_path(args.data))
        with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
            bid_create_data = json.loads(f.read())
            client.post_bid(tender_id, bid_create_data, success_handler=bid_create_success_print_handler)


def create_plan(client, args, filename_prefix=""):
    print("Creating plan...\n")
    path = get_data_file_path("{}plan_create.json".format(filename_prefix), get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        plan_create_data = json.loads(f.read())
        set_mode_data(plan_create_data)
        response = client.post_plan(plan_create_data, success_handler=plan_create_success_print_handler)
        return response


def create_tender(client, args, plan_id=None, agreement_id=None, filename_prefix=""):
    print("Creating tender...\n")
    path = get_data_file_path("{}tender_create.json".format(filename_prefix), get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_create_data = json.loads(f.read())
        set_mode_data(tender_create_data)
        set_acceleration_data(tender_create_data, acceleration=args.acceleration)
        if agreement_id:
            set_agreement_id(tender_create_data, agreement_id)
        if plan_id:
            response = client.post_tender(
                plan_id, tender_create_data, success_handler=tender_create_success_print_handler
            )
        else:
            response = client.post_tender(tender_create_data, success_handler=tender_create_success_print_handler)
        return response


def update_tender_period(client, args, tender_id, tender_token, acceleration):
    data = set_tender_period_data({"data": {"tenderPeriod": {}}}, acceleration=acceleration)
    client.patch_tender(tender_id, tender_token, data)


def wait(date_str, date_info_str=None):
    date_timedelta = parser.parse(date_str) - datetime.now(tz.tzutc())
    delta_seconds = date_timedelta.total_seconds()
    date_seconds = math.ceil(delta_seconds) if delta_seconds > 0 else 0
    info_str = " for {}".format(date_info_str) if date_info_str else ""
    print("Waiting {} seconds{} - {}...\n".format(date_seconds, info_str, date_str))
    sleep(date_seconds)


def wait_status(client, args, tender_id, status, fallback=None):
    print("Waiting for {}...\n".format(status))
    while True:
        response = client.get_tender(tender_id)
        if not response.json()["data"]["status"] == status:
            sleep(TENDER_SECONDS_BUFFER)
            if fallback:
                fallback()
        else:
            response_handler(response, tender_check_status_success_print_handler)
            break
    return response


def patch_stage2_credentials(client, args, stage2_tender_id, tender_token):
    print("Getting credentials for second stage...\n")
    path = get_data_file_path("stage2_tender_credentials.json", get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_patch_data = json.loads(f.read())
        return client.patch_credentials(
            stage2_tender_id, tender_token, tender_patch_data, success_handler=tender_create_success_print_handler
        )


def patch_contract_credentials(client, args, contract_id, tender_token):
    print("Getting credentials for contract...\n")
    return client.patch_credentials(
        contract_id, tender_token, {}, success_handler=contract_credentials_success_print_handler
    )


def patch_tender_tendering(client, args, tender_id, tender_token, filename_prefix=""):
    print("Activating tender by switching to next status...\n")
    path = get_data_file_path("{}tender_patch_tendering.json".format(filename_prefix), get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_patch_data = json.loads(f.read())
        return client.patch_tender(
            tender_id, tender_token, tender_patch_data, success_handler=tender_patch_status_success_print_handler
        )


def patch_tender_pending(client, args, tender_id, tender_token, filename_prefix=""):
    print("Activating tender by switching to next status...\n")
    path = get_data_file_path("{}tender_patch_pending.json".format(filename_prefix), get_data_path(args.data))
    with ignore(IOError), open_file_or_exit(path, exit_filename=args.stop) as f:
        tender_patch_data = json.loads(f.read())
        return client.patch_tender(
            tender_id, tender_token, tender_patch_data, success_handler=tender_patch_status_success_print_handler
        )


def wait_edr_pre_qual(client, args, tender_id):
    print("Waiting for {} in qualifications documents...\n".format(EDR_FILENAME))
    response = get_qualifications(client, args, tender_id)
    for qualification in response.json()["data"]:
        while EDR_FILENAME not in [doc["title"] for doc in qualification.get("documents", [])]:
            sleep(TENDER_SECONDS_BUFFER)
            qualification = client.get_qualification(tender_id, qualification["id"]).json()["data"]


def wait_edr_qual(client, args, tender_id):
    print("Waiting for {} in awards documents...\n".format(EDR_FILENAME))
    response = get_awards(client, args, tender_id)
    for award in response.json()["data"]:
        while EDR_FILENAME not in [doc["title"] for doc in award.get("documents", [])]:
            sleep(TENDER_SECONDS_BUFFER)
            award = client.get_award(tender_id, award["id"]).json()["data"]
