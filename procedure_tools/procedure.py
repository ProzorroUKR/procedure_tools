import logging
import random

from faker import Faker

from procedure_tools.actions import (
    create_awards,
    create_bids,
    create_complaints,
    create_framework,
    create_plan,
    create_plans,
    create_sublissions,
    create_tender,
    get_agreement,
    get_agreements,
    get_awards,
    get_contract,
    get_framework,
    get_qualifications,
    get_tender,
    get_tender_contracts,
    patch_agreements,
    patch_agreements_contracts,
    patch_award,
    patch_bids,
    patch_complaints,
    patch_contract_credentials,
    patch_contracts,
    patch_contracts_buyer_signer_info,
    patch_contracts_suppliers_signer_info,
    patch_framework_active,
    patch_framework_qualifications,
    patch_plan,
    patch_qualifications,
    patch_stage2_credentials,
    patch_submissions,
    patch_tender,
    patch_tender_pending,
    patch_tender_pre,
    patch_tender_qual,
    patch_tender_tendering,
    patch_tender_waiting,
    post_bid_res,
    post_criteria,
    post_tender_plan,
    re_upload_evaluation_report,
    upload_bids_proposal,
    upload_evaluation_report,
    upload_qualifications_evaluation_reports,
    upload_tender_documents,
    upload_tender_notice,
    wait,
    wait_auction_participation_urls,
    wait_edr_pre_qual,
    wait_edr_qual,
    wait_status,
)
from procedure_tools.client import CDBClient, DSClient
from procedure_tools.utils.data import (
    get_access,
    get_award_id,
    get_complaint_period_end_dates,
    get_config,
    get_contract_period_clarif_date,
    get_contracts_bid_tokens,
    get_data,
    get_id,
    get_ids,
    get_next_check,
    get_procurement_method,
    get_procurement_method_type,
    get_submission_method_details,
    get_token,
)
from procedure_tools.utils.file import get_data_path, get_numberless_filename

try:
    from colorama import init

    init()
except ImportError:
    pass

WAIT_EDR_QUAL = "edr-qualification"
WAIT_EDR_PRE_QUAL = "edr-pre-qualification"


def set_faker_seed(args):
    faker_seed = args.seed or random.randint(0, 1000000)
    logging.info(f"Using seed {faker_seed}\n")
    Faker.seed(faker_seed)


def init_procedure(args, session=None):
    set_faker_seed(args)

    if args.stop:
        args.stop = get_numberless_filename(args.stop)

    data_path = get_data_path(args.data)
    if data_path is None:
        logging.error("Data path not found.\n")
    else:
        process_procedure(args, session=session)
        logging.info("Completed.\n")


def process_procedure(
    args,
    context=None,
    tender_id=None,
    tender_token=None,
    prefix="",
    session=None,
):
    context = context or {}

    client = CDBClient(
        args.host,
        args.token,
        args.path,
        session=session,
        debug=args.debug,
    )
    ds_client = DSClient(
        args.ds_host,
        args.ds_username,
        args.ds_password,
        session=session,
        debug=args.debug,
    )

    context["acceleration"] = args.acceleration
    context["submission"] = args.submission
    context["client_timedelta"] = client.client_timedelta

    response = create_framework(
        client,
        args,
        context,
        prefix=prefix,
    )

    if response:
        framework_id = get_id(response)
        framework_token = get_token(response)
        response = patch_framework_active(
            client,
            args,
            context,
            framework_id,
            framework_token,
            prefix=prefix,
        )
        context["framework"] = response.json()["data"]

        responses = create_sublissions(
            client,
            ds_client,
            args,
            context,
            framework_id,
            prefix=prefix,
        )

        submissions_ids = [get_id(response) for response in responses]
        submissions_tokens = [get_token(response) for response in responses]
        responses = patch_submissions(
            client,
            args,
            context,
            submissions_ids,
            submissions_tokens,
            prefix=prefix,
        )

        qualifications_ids = [response.json()["data"]["qualificationID"] for response in responses]

        upload_qualifications_evaluation_reports(
            client,
            ds_client,
            args,
            context,
            qualifications_ids,
            framework_token,
            prefix=prefix,
        )

        responses = patch_framework_qualifications(
            client,
            args,
            context,
            qualifications_ids,
            framework_token,
            prefix=prefix,
        )

        response = get_framework(client, args, context, framework_id)
        framework = get_data(response)
        context["framework"] = framework
        agreement_id = framework["agreementID"]

        response = get_agreement(client, args, context, agreement_id)
        agreement = get_data(response)
        context["agreement"] = agreement

    if not tender_id and not tender_token:
        # It means that we are starting a new procedure
        # not a second stage of another

        response = create_plan(
            client,
            args,
            context,
            prefix=prefix,
        )

        if response:
            # Start a new procedure from a plan
            plan_id = get_id(response)
            plan_token = get_token(response)
            response = patch_plan(
                client,
                args,
                context,
                plan_id,
                plan_token,
                prefix=prefix,
            )
            response = create_tender(
                client,
                args,
                context,
                plan_id=plan_id,
                prefix=prefix,
            )
        else:
            # Start procedure without a plan
            plan_id = None
            response = create_tender(
                client,
                args,
                context,
                prefix=prefix,
            )

        if not response:
            # We haven't started a new procedure
            # That's the end
            return

        tender = get_data(response)
        context[f"{prefix}tender"] = tender

        tender_access = get_access(response)
        context[f"{prefix}tender_access"] = tender_access

        config = get_config(response)
        context[f"{prefix}tender_config"] = config

        tender_id = get_id(response)
        tender_token = get_token(response)

        if not plan_id:
            # Create multiple plans
            # Used in central kind procedures
            plans_responses = create_plans(
                client,
                args,
                context,
                prefix=prefix,
            )
            for plan_response in plans_responses:
                # Attach multiple plans to the tender
                plan_id = plan_response.json()["data"]["id"]
                post_tender_plan(
                    client,
                    args,
                    context,
                    tender_id,
                    tender_token,
                    plan_id,
                    prefix=prefix,
                )

    response = get_tender(client, args, context, tender_id)

    tender = get_data(response)
    context[f"{prefix}tender"] = tender

    config = get_config(response)
    context[f"{prefix}tender_config"] = config

    method = get_procurement_method(response)
    method_type = get_procurement_method_type(response)
    submission_method_details = get_submission_method_details(response)

    upload_tender_documents(
        client,
        ds_client,
        args,
        context,
        tender_id,
        tender_token,
        prefix=prefix,
    )

    if method_type in (
        "belowThreshold",
        "requestForProposal",
        "competitiveOrdering",
        "aboveThreshold",
        "aboveThresholdUA",
        "aboveThresholdEU",
        "closeFrameworkAgreementUA",
        "competitiveDialogueEU",
        "competitiveDialogueUA",
        "competitiveDialogueEU.stage2",
        "competitiveDialogueUA.stage2",
        "esco",
        "priceQuotation",
    ):
        criteria_response = post_criteria(
            client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )
        if criteria_response:
            tender_criteria = criteria_response.json()["data"]
        else:
            tender_criteria = None
    else:
        tender_criteria = None

    upload_tender_notice(
        client,
        ds_client,
        args,
        context,
        tender_id,
        tender_token,
        prefix=prefix,
    )

    if method_type not in (
        "closeFrameworkAgreementSelectionUA",
        "competitiveDialogueEU.stage2",
        "competitiveDialogueUA.stage2",
    ):
        response = patch_tender(
            client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )

    if method_type in ("closeFrameworkAgreementSelectionUA",):
        patch_tender_pending(
            client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )

    if method_type in ("closeFrameworkAgreementSelectionUA",):
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=1,
            status="active.enquiries",
            fail_status="draft.unsuccessful",
        )

    if method_type in (
        "belowThreshold",
        "requestForProposal",
    ):
        next_check = get_next_check(response)
        if next_check:
            wait(
                next_check,
                client_timedelta=client.client_timedelta,
                date_info_str="next chronograph check",
            )

    if method_type in (
        "belowThreshold",
        "requestForProposal",
        "closeFrameworkAgreementSelectionUA",
    ):
        response = get_tender(client, args, context, tender_id)

        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=1,
            status="active.tendering",
            fail_status="unsuccessful",
        )

    if method_type in (
        "competitiveDialogueEU.stage2",
        "competitiveDialogueUA.stage2",
    ):
        patch_tender_tendering(
            client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )

    comp_responses = create_complaints(
        client,
        args,
        context,
        tender_id,
        tender_token,
        file_subpath="complaints",
        prefix=prefix,
    )
    if comp_responses:
        comp_jsons = [comp_response.json() for comp_response in comp_responses]
        comp_ids = [comp_json["data"]["id"] for comp_json in comp_jsons]
        comp_tokens = [comp_json["access"]["token"] for comp_json in comp_jsons]
        patch_complaints(
            client,
            args,
            context,
            tender_id,
            tender_token,
            comp_ids,
            comp_tokens,
            file_subpath="complaints",
            prefix=prefix,
        )

    bids_ids = []
    bids_tokens = []

    if method != "limited":
        bids_responses = create_bids(
            client,
            ds_client,
            args,
            context,
            tender_id,
            prefix=prefix,
        )
        bids_jsons = [bids_response.json() for bids_response in bids_responses]
        bids_ids = [bid_json["data"]["id"] for bid_json in bids_jsons]
        bids_tokens = [bid_json["access"]["token"] for bid_json in bids_jsons]
        if tender_criteria:
            bids_documents = [bid_json["data"].get("documents", []) for bid_json in bids_jsons]
            post_bid_res(
                client,
                args,
                context,
                tender_id,
                bids_ids,
                bids_tokens,
                bids_documents,
                prefix=prefix,
            )
        upload_bids_proposal(
            client,
            ds_client,
            args,
            context,
            tender_id,
            bids_ids,
            bids_tokens,
            prefix=prefix,
        )
        patch_bids(
            client,
            args,
            context,
            tender_id,
            bids_ids,
            bids_tokens,
            prefix=prefix,
        )
    else:
        bids_jsons = None

    if method != "limited":
        response = get_tender(client, args, context, tender_id)
        next_check = get_next_check(response)
        if next_check:
            wait(
                next_check,
                client_timedelta=client.client_timedelta,
                date_info_str="next chronograph check",
            )

    if config["hasPrequalification"]:
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=1,
            status="active.pre-qualification",
            fail_status="unsuccessful",
        )

    if config["hasPrequalification"]:
        if WAIT_EDR_PRE_QUAL in args.wait.split(","):
            wait_edr_pre_qual(client, args, context, tender_id)

    qualifications_ids = []

    if config["hasPrequalification"]:
        response = get_qualifications(client, args, context, tender_id)
        qualifications_ids = get_ids(response)
        patch_qualifications(
            client,
            args,
            context,
            tender_id,
            qualifications_ids,
            tender_token,
            prefix=prefix,
        )

        responses = upload_evaluation_report(
            client,
            ds_client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )
        if responses and len(responses) >= 1:
            evaluation_report_document_id = get_id(responses[-1])

        patch_tender_pre(
            client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )

    if bids_tokens:
        for qualification_index, qualification_id in enumerate(qualifications_ids):
            comp_responses = create_complaints(
                client,
                args,
                context,
                tender_id,
                bids_tokens[0],  # any of suppliers can create complaint
                obj_type="qualification",
                obj_index=qualification_index,
                obj_id=qualification_id,
                file_subpath="qualifications_complaints",
                prefix=prefix,
            )
            if comp_responses:
                comp_jsons = [comp_response.json() for comp_response in comp_responses]
                comp_ids = [comp_json["data"]["id"] for comp_json in comp_jsons]
                comp_tokens = [comp_json["access"]["token"] for comp_json in comp_jsons]
                patch_complaints(
                    client,
                    args,
                    context,
                    tender_id,
                    tender_token,
                    comp_ids,
                    comp_tokens,
                    obj_type="qualification",
                    obj_index=qualification_index,
                    obj_id=qualification_id,
                    file_subpath="qualifications_complaints",
                    prefix=prefix,
                )

    response = get_tender(client, args, context, tender_id)
    tender_status = response.json()["data"]["status"]

    if tender_status == "active.pre-qualification":
        # satisfied complaint changes tender status to active.pre-qualification,
        # so we need to:
        # - upload new version of evaluation report
        # - switch again to active.pre-qualification.stand-still

        re_upload_evaluation_report(
            client,
            ds_client,
            args,
            context,
            tender_id,
            evaluation_report_document_id,
            tender_token,
            prefix=prefix,
        )

        patch_tender_pre(
            client,
            args,
            context,
            tender_id,
            tender_token,
            prefix=prefix,
        )

    if method_type in (
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=1,
            status="active.stage2.pending",
            fail_status="unsuccessful",
        )
        patch_tender_waiting(client, args, context, tender_id, tender_token)

    if method != "limited" and method_type not in (
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=1,
            status=["active.auction", "active.qualification", "active.awarded"],
            fail_status="unsuccessful",
        )

    if (
        config["hasAuction"]
        and bids_jsons
        and (
            not submission_method_details
            or all(
                [
                    "mode:fast-forward" not in submission_method_details,
                    "mode:no-auction" not in submission_method_details,
                ]
            )
        )
    ):
        wait_auction_participation_urls(client, args, tender_id, bids_jsons)

    if method != "limited" and method_type not in (
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=1,
            status=["active.qualification", "active.awarded"],
            fail_status="unsuccessful",
        )

    if method == "limited":
        create_awards(client, args, context, tender_id, tender_token)

    if method == "limited":
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=20,
            status="active",
        )

    if WAIT_EDR_QUAL in args.wait.split(","):
        wait_edr_qual(client, args, context, tender_id)

    awards_ids = []

    if method_type not in (
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        response = get_awards(client, args, context, tender_id)
        awards_ids = get_ids(response)
        award_action_index = 0
        while True:
            responses = patch_award(
                client,
                ds_client,
                args,
                context,
                tender_id,
                awards_ids,
                tender_token,
                action_index=award_action_index,
                prefix=prefix,
            )
            if not responses:
                # There were no files for this action index,
                # that means we have reached the end of actions
                break
            award_action_index += 1
            response = get_awards(client, args, context, tender_id)
            awards_ids = get_ids(response)

    if method_type in ("closeFrameworkAgreementUA",):
        patch_tender_qual(client, args, context, tender_id, tender_token)

    if bids_tokens:
        for award_index, award_id in enumerate(awards_ids):
            comp_responses = create_complaints(
                client,
                args,
                context,
                tender_id,
                bids_tokens[0],  # any of suppliers can create complaint
                obj_type="award",
                obj_index=award_index,
                obj_id=award_id,
                file_subpath="awards_complaints",
                prefix=prefix,
            )
            if comp_responses:
                comp_jsons = [comp_response.json() for comp_response in comp_responses]
                comp_ids = [comp_json["data"]["id"] for comp_json in comp_jsons]
                comp_tokens = [comp_json["access"]["token"] for comp_json in comp_jsons]
                patch_complaints(
                    client,
                    args,
                    context,
                    tender_id,
                    tender_token,
                    comp_ids,
                    comp_tokens,
                    obj_type="award",
                    obj_index=award_index,
                    obj_id=award_id,
                    file_subpath="awards_complaints",
                    prefix=prefix,
                )

    if method_type in ("closeFrameworkAgreementUA",):
        response = get_tender(client, args, context, tender_id)
        tender_status = response.json()["data"]["status"]

        if tender_status == "active.qualification":
            # satisfied complaint changes tender status to active.qualification,
            # so we need to switch it again to active.qualification.stand-still
            patch_tender_qual(client, args, context, tender_id, tender_token)

    if method_type in (
        "closeFrameworkAgreementUA",
        "aboveThresholdEU",
        "competitiveDialogueEU.stage2",
        "esco",
    ):
        wait_status(
            client,
            args,
            context,
            tender_id,
            delay=20,
            status="active.awarded",
        )

    if config["hasAwardComplaints"]:
        response = get_awards(client, args, context, tender_id)
        awards_complaint_dates = get_complaint_period_end_dates(response)
        wait(
            max(awards_complaint_dates),
            client_timedelta=client.client_timedelta,
            date_info_str="end of award complaint period",
        )

    contracts_ids = []

    if method_type not in (
        "closeFrameworkAgreementUA",
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        response = get_tender_contracts(client, args, context, tender_id)
        contracts_ids = get_ids(response, status_exclude="cancelled")

    contracts_tokens = []
    contracts_award_ids = []

    context["contracts"] = []

    if method_type not in (
        "closeFrameworkAgreementUA",
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        for contracts_id in contracts_ids:
            response = get_contract(client, args, context, contracts_id)
            context["contracts"].append(response.json()["data"])
            response = patch_contract_credentials(
                client,
                args,
                context,
                contracts_id,
                tender_token,
            )
            contracts_tokens.append(get_token(response))
            contracts_award_ids.append(get_award_id(response))

    if method != "limited" and method_type not in (
        "closeFrameworkAgreementUA",
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        patch_contracts_buyer_signer_info(
            client,
            args,
            context,
            contracts_ids,
            contracts_tokens,
            prefix=prefix,
        )

        response = get_awards(client, args, context, tender_id)
        contracts_bid_tokens = get_contracts_bid_tokens(
            response,
            bids_ids,
            bids_tokens,
            contracts_award_ids,
        )

        patch_contracts_suppliers_signer_info(
            client,
            args,
            context,
            contracts_ids,
            contracts_bid_tokens,
            prefix=prefix,
        )

    if method_type not in (
        "closeFrameworkAgreementUA",
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        patch_contracts(
            client,
            args,
            context,
            contracts_ids,
            contracts_tokens,
            prefix=prefix,
        )

    if method_type in ("closeFrameworkAgreementUA",):
        response = get_tender(client, args, context, tender_id)
        contract_period_clarif_date = get_contract_period_clarif_date(response)
        wait(
            contract_period_clarif_date,
            client_timedelta=client.client_timedelta,
            date_info_str="contract period clarifications until date",
        )
        response = get_agreements(client, args, context, tender_id)
        agreements_ids = get_ids(response)
        patch_agreements_contracts(
            client,
            args,
            context,
            tender_id,
            agreements_ids,
            tender_token,
        )
        patch_agreements(
            client,
            ds_client,
            args,
            context,
            tender_id,
            agreements_ids,
            tender_token,
        )

    wait_status(
        client,
        args,
        context,
        tender_id,
        delay=1,
        status="complete",
    )

    if method_type in (
        "competitiveDialogueEU",
        "competitiveDialogueUA",
    ):
        response = get_tender(client, args, context, tender_id)
        tender_id = response.json()["data"]["stage2TenderID"]
        response = patch_stage2_credentials(
            client,
            args,
            context,
            tender_id,
            tender_token,
        )
        tender_token = get_token(response)

        process_procedure(
            args,
            context,
            tender_id=tender_id,
            tender_token=tender_token,
            prefix="stage2_",
            session=session,
        )

    if method_type in ("closeFrameworkAgreementUA",):
        response = get_tender(client, args, context, tender_id)
        agreement_id = response.json()["data"]["agreements"][-1]["id"]

        response = get_agreement(client, args, context, agreement_id)
        context["agreement"] = response.json()["data"]

        response = create_tender(
            client,
            args,
            context,
            prefix="selection_",
        )
        tender_id = get_id(response)
        tender_token = get_token(response)

        process_procedure(
            args,
            context,
            tender_id=tender_id,
            tender_token=tender_token,
            prefix="selection_",
            session=session,
        )
