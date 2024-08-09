from __future__ import absolute_import

import json
import logging
from base64 import b64encode
from copy import copy, deepcopy
from datetime import timedelta

from procedure_tools.utils.date import get_utcnow, parse_date_header

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests

from procedure_tools.utils import adapters
from procedure_tools.utils.handlers import (
    client_init_response_handler,
    response_handler,
)
from procedure_tools.version import __version__

API_PATH_PREFIX_DEFAULT = "/api/0/"


class BaseApiClient(object):
    name = "api"

    SPORE_PATH = "spore"

    HEADERS_DEFAULT = {
        "User-Agent": "procedure_tools/{}".format(__version__),
    }

    def __init__(self, host, session=None, debug=False, **kwargs):
        logging.info(f"Initializing {self.name} client\n")
        self.host = host
        self.kwargs = kwargs
        self.debug = debug
        if session:
            self.session = session
        else:
            self.session = requests.Session()
            adapters.mount(session)
        self.headers = copy(self.HEADERS_DEFAULT)

    def get_url(self, api_path):
        return urljoin(self.host, api_path)

    def format_data(self, data):
        try:
            text = json.dumps(data, ensure_ascii=False, indent=4)
        except TypeError:
            text = str(data)
        return text

    def log_request(self, data):
        if data is not None:
            request_text = self.format_data(data)
            logging.debug(f"Request:\n {request_text}")

    def log_response(self, text):
        if text is not None:
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                response_text = text
            else:
                response_text = self.format_data(data)
            logging.debug(f"Response:\n {response_text}")

    def request(self, method, path, **kwargs):
        request_kwargs = copy(kwargs)
        auth_token = request_kwargs.pop("auth_token", None)
        success_handler = request_kwargs.pop("success_handler", None)
        error_handler = request_kwargs.pop("error_handler", None)
        request_kwargs["headers"] = copy(self.headers)
        request_kwargs["headers"].update(
            {"Authorization": "Bearer " + auth_token} if auth_token else {}
        )
        request_kwargs["headers"].update(kwargs.get("headers", {}))
        url = self.get_url(path)
        response = self.session.request(method=method, url=url, **request_kwargs)
        if self.debug:
            self.log_request(request_kwargs.get("json", None))
            self.log_response(response.text)
        if response.status_code == 409:
            response = self.request(method, path, **kwargs)
        else:
            handlers = {}
            if success_handler:
                handlers["success_handler"] = success_handler
            if error_handler:
                handlers["error_handler"] = error_handler
            response_handler(response, **handlers)
        return response

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, json=None, **kwargs):
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path, json=None, **kwargs):
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path, json=None, **kwargs):
        return self.request("PATCH", path, json=json, **kwargs)


class BaseCDBClient(BaseApiClient):
    name = "cdb"

    SPORE_PATH = "spore"

    def __init__(
        self,
        host,
        auth_token=None,
        path_prefix=API_PATH_PREFIX_DEFAULT,
        session=None,
        **request_kwargs,
    ):
        super(BaseCDBClient, self).__init__(host, session=session, **request_kwargs)
        self.path_prefix = path_prefix
        self.headers.update({"Content-Type": "application/json"})
        spore_url = self.get_url(self.get_api_path(self.SPORE_PATH))
        # GET request to retrieve cookies and server time
        response = self.session.get(spore_url)
        # Calculate client time delta with server
        client_datetime = get_utcnow()
        try:
            server_datetime = parse_date_header(response.headers.get("date"))
            self.client_timedelta = server_datetime - client_datetime
        except:
            self.client_timedelta = timedelta()
        client_init_response_handler(response, self.client_timedelta)

    def get_api_path(self, path, acc_token=None):
        return urljoin(
            self.path_prefix,
            urljoin(path, "?acc_token={}".format(acc_token) if acc_token else None),
        )


class CDBClient(BaseCDBClient):
    name = "tenders"

    PLANS_COLLECTION_PATH = "plans"
    PLANS_PATH = "plans/{}"
    PLANS_TENDERS_COLLECTION_PATH = "plans/{}/tenders"

    TENDERS_COLLECTION_PATH = "tenders"
    TENDERS_PATH = "tenders/{}"
    TENDERS_PLANS_PATH = "tenders/{}/plans"
    TENDERS_DOCUMENTS_COLLECTION_PATH = "tenders/{}/documents"
    TENDERS_DOCUMENTS_PATH = "tenders/{}/documents/{}"
    TENDERS_CRITERIA_COLLECTION_PATH = "tenders/{}/criteria"
    TENDERS_BIDS_COLLECTION_PATH = "tenders/{}/bids"
    TENDERS_BIDS_PATH = "tenders/{}/bids/{}"
    TENDERS_BIDS_RES_COLLECTION_PATH = "tenders/{}/bids/{}/requirement_responses"
    TENDERS_AWARDS_COLLECTION_PATH = "tenders/{}/awards"
    TENDERS_AWARDS_PATH = "tenders/{}/awards/{}"
    TENDERS_CONTRACTS_COLLECTION_PATH = "tenders/{}/contracts"
    TENDERS_CONTRACTS_PATH = "tenders/{}/contracts/{}"
    TENDERS_QUALIFICATIONS_COLLECTION_PATH = "tenders/{}/qualifications"
    TENDERS_QUALIFICATIONS_PATH = "tenders/{}/qualifications/{}"
    TENDERS_AGREEMENTS_COLLECTION_PATH = "tenders/{}/agreements"
    TENDERS_AGREEMENTS_PATH = "tenders/{}/agreements/{}"
    TENDERS_AGREEMENTS_DOCUMENTS_COLLECTION_PATH = "tenders/{}/agreements/{}/documents"
    TENDERS_AGREEMENTS_CONTRACTS_COLLECTION_PATH = "tenders/{}/agreements/{}/contracts"
    TENDERS_AGREEMENTS_CONTRACTS_PATH = "tenders/{}/agreements/{}/contracts/{}"
    TENDERS_CREDENTIALS_PATH = "tenders/{}/credentials"
    TENDERS_COMPLAINTS_COLLECTION_PATH = "tenders/{}/complaints"
    TENDERS_COMPLAINTS_PATH = "tenders/{}/complaints/{}"
    TENDERS_AWARDS_COMPLAINTS_COLLECTION_PATH = "tenders/{}/awards/{}/complaints"
    TENDERS_AWARDS_COMPLAINTS_PATH = "tenders/{}/awards/{}/complaints/{}"
    TENDERS_QUALIFICATIONS_COMPLAINTS_COLLECTION_PATH = (
        "tenders/{}/qualifications/{}/complaints"
    )
    TENDERS_QUALIFICATIONS_COMPLAINTS_PATH = (
        "tenders/{}/qualifications/{}/complaints/{}"
    )

    CONTRACTS_PATH = "contracts/{}"
    CONTRACTS_BUYERS_SIGNER_INFO_PATH = "contracts/{}/buyer/signer_info"
    CONTRACTS_SUPPLIERS_SIGNER_INFO_PATH = "contracts/{}/suppliers/signer_info"
    CONTRACTS_CREDENTIALS_PATH = "contracts/{}/credentials"

    AGREEMENTS_PATH = "agreements/{}"

    def get_plan(self, plan_id, **kwargs):
        contracts_path = self.PLANS_PATH.format(plan_id)
        path = self.get_api_path(contracts_path)
        return self.get(path, **kwargs)

    def post_plan(self, json, **kwargs):
        tenders_path = self.PLANS_COLLECTION_PATH
        path = self.get_api_path(tenders_path)
        return self.post(path, json, **kwargs)

    def patch_plan(self, plan_id, acc_token, json, **kwargs):
        tenders_path = self.PLANS_PATH.format(plan_id)
        path = self.get_api_path(tenders_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def post_plan_tender(self, plan_id, json, **kwargs):
        tenders_path = self.PLANS_TENDERS_COLLECTION_PATH.format(plan_id)
        path = self.get_api_path(tenders_path)
        return self.post(path, json, **kwargs)

    def get_tender(self, tender_id, **kwargs):
        tenders_path = self.TENDERS_PATH.format(tender_id)
        path = self.get_api_path(tenders_path)
        return self.get(path, **kwargs)

    def post_tender(self, json, **kwargs):
        tenders_path = self.TENDERS_COLLECTION_PATH
        path = self.get_api_path(tenders_path)
        return self.post(path, json, **kwargs)

    def patch_tender(self, tender_id, acc_token, json, **kwargs):
        tenders_path = self.TENDERS_PATH.format(tender_id)
        path = self.get_api_path(tenders_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def post_tender_plan(self, tender_id, acc_token, json, **kwargs):
        tenders_path = self.TENDERS_PLANS_PATH.format(tender_id)
        path = self.get_api_path(tenders_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def post_tender_document(self, tender_id, acc_token, json, **kwargs):
        documents_path = self.TENDERS_DOCUMENTS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(documents_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def put_tender_document(self, tender_id, document_id, acc_token, json, **kwargs):
        documents_path = self.TENDERS_DOCUMENTS_PATH.format(tender_id, document_id)
        path = self.get_api_path(documents_path, acc_token=acc_token)
        return self.put(path, json, **kwargs)

    def post_tender_criteria(self, tender_id, acc_token, json, **kwargs):
        criteria_path = self.TENDERS_CRITERIA_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(criteria_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def get_tender_bids(self, tender_id, **kwargs):
        bid_path = self.TENDERS_BIDS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(bid_path)
        return self.get(path, **kwargs)

    def get_tender_bid(self, tender_id, bid_id, acc_token, **kwargs):
        bid_path = self.TENDERS_BIDS_PATH.format(tender_id, bid_id)
        path = self.get_api_path(bid_path, acc_token=acc_token)
        return self.get(path, **kwargs)

    def post_tender_bid(self, tender_id, json, **kwargs):
        bids_path = self.TENDERS_BIDS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(bids_path)
        return self.post(path, json, **kwargs)

    def patch_tender_bid(self, tender_id, bid_id, acc_token, json, **kwargs):
        bid_path = self.TENDERS_BIDS_PATH.format(tender_id, bid_id)
        path = self.get_api_path(bid_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def post_tender_bid_res(self, tender_id, bid_id, acc_token, json, **kwargs):
        bid_res_path = self.TENDERS_BIDS_RES_COLLECTION_PATH.format(tender_id, bid_id)
        path = self.get_api_path(bid_res_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def get_tender_complaints(self, tender_id, **kwargs):
        complaints_path = self.TENDERS_COMPLAINTS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(complaints_path)
        return self.get(path, **kwargs)

    def get_tender_complaint(self, tender_id, complaint_id, **kwargs):
        complaints_path = self.TENDERS_COMPLAINTS_PATH.format(tender_id, complaint_id)
        path = self.get_api_path(complaints_path)
        return self.get(path, **kwargs)

    def post_tender_complaint(self, tender_id, acc_token, json, **kwargs):
        complaints_path = self.TENDERS_COMPLAINTS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(complaints_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def patch_tender_complaint(
        self, tender_id, complaint_id, acc_token, json, **kwargs
    ):
        complaints_path = self.TENDERS_COMPLAINTS_PATH.format(tender_id, complaint_id)
        path = self.get_api_path(complaints_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_tender_qualifications(self, tender_id, **kwargs):
        qualifications_path = self.TENDERS_QUALIFICATIONS_COLLECTION_PATH.format(
            tender_id
        )
        path = self.get_api_path(qualifications_path)
        return self.get(path, **kwargs)

    def get_tender_qualification(self, tender_id, qualification_id, **kwargs):
        qualifications_path = self.TENDERS_QUALIFICATIONS_PATH.format(
            tender_id, qualification_id
        )
        path = self.get_api_path(qualifications_path)
        return self.get(path, **kwargs)

    def patch_tender_qualification(
        self, tender_id, qualification_id, acc_token, json, **kwargs
    ):
        qualifications_path = self.TENDERS_QUALIFICATIONS_PATH.format(
            tender_id, qualification_id, acc_token
        )
        path = self.get_api_path(qualifications_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_tender_qualification_complaints(
        self, tender_id, qualification_id, **kwargs
    ):
        complaints_path = self.TENDERS_QUALIFICATIONS_COMPLAINTS_COLLECTION_PATH.format(
            tender_id, qualification_id
        )
        path = self.get_api_path(complaints_path)
        return self.get(path, **kwargs)

    def get_tender_qualification_complaint(
        self, tender_id, qualification_id, complaint_id, **kwargs
    ):
        complaints_path = self.TENDERS_QUALIFICATIONS_COMPLAINTS_PATH.format(
            tender_id, qualification_id, complaint_id
        )
        path = self.get_api_path(complaints_path)
        return self.get(path, **kwargs)

    def post_tender_qualification_complaint(
        self, tender_id, qualification_id, acc_token, json, **kwargs
    ):
        complaints_path = self.TENDERS_QUALIFICATIONS_COMPLAINTS_COLLECTION_PATH.format(
            tender_id, qualification_id
        )
        path = self.get_api_path(complaints_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def patch_tender_qualification_complaint(
        self, tender_id, qualification_id, complaint_id, acc_token, json, **kwargs
    ):
        complaints_path = self.TENDERS_QUALIFICATIONS_COMPLAINTS_PATH.format(
            tender_id, qualification_id, complaint_id
        )
        path = self.get_api_path(complaints_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_tender_awards(self, tender_id, **kwargs):
        awards_path = self.TENDERS_AWARDS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(awards_path)
        return self.get(path, **kwargs)

    def get_tender_award(self, tender_id, award_id, **kwargs):
        awards_path = self.TENDERS_AWARDS_PATH.format(tender_id, award_id)
        path = self.get_api_path(awards_path)
        return self.get(path, **kwargs)

    def post_tender_award(self, tender_id, acc_token, json, **kwargs):
        awards_path = self.TENDERS_AWARDS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(awards_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def patch_tender_award(self, tender_id, award_id, acc_token, json, **kwargs):
        awards_path = self.TENDERS_AWARDS_PATH.format(tender_id, award_id, acc_token)
        path = self.get_api_path(awards_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_tender_award_complaints(self, tender_id, award_id, **kwargs):
        complaints_path = self.TENDERS_AWARDS_COMPLAINTS_COLLECTION_PATH.format(
            tender_id, award_id
        )
        path = self.get_api_path(complaints_path)
        return self.get(path, **kwargs)

    def get_tender_award_complaint(self, tender_id, award_id, complaint_id, **kwargs):
        complaints_path = self.TENDERS_AWARDS_COMPLAINTS_PATH.format(
            tender_id, award_id, complaint_id
        )
        path = self.get_api_path(complaints_path)
        return self.get(path, **kwargs)

    def post_tender_award_complaint(
        self, tender_id, award_id, acc_token, json, **kwargs
    ):
        complaints_path = self.TENDERS_AWARDS_COMPLAINTS_COLLECTION_PATH.format(
            tender_id, award_id
        )
        path = self.get_api_path(complaints_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def patch_tender_award_complaint(
        self, tender_id, award_id, complaint_id, acc_token, json, **kwargs
    ):
        complaints_path = self.TENDERS_AWARDS_COMPLAINTS_PATH.format(
            tender_id, award_id, complaint_id
        )
        path = self.get_api_path(complaints_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_tender_contracts(self, tender_id, **kwargs):
        awards_path = self.TENDERS_CONTRACTS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(awards_path)
        return self.get(path, **kwargs)

    def patch_tender_contract(self, tender_id, contract_id, acc_token, json, **kwargs):
        awards_path = self.TENDERS_CONTRACTS_PATH.format(
            tender_id, contract_id, acc_token
        )
        path = self.get_api_path(awards_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_tender_agreements(self, tender_id, **kwargs):
        agreements_path = self.TENDERS_AGREEMENTS_COLLECTION_PATH.format(tender_id)
        path = self.get_api_path(agreements_path)
        return self.get(path, **kwargs)

    def patch_tender_agreement(
        self, tender_id, agreement_id, acc_token, json, **kwargs
    ):
        agreements_path = self.TENDERS_AGREEMENTS_PATH.format(
            tender_id, agreement_id, acc_token
        )
        path = self.get_api_path(agreements_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def post_tender_agreement_document(
        self, tender_id, agreement_id, acc_token, json, **kwargs
    ):
        agreements_path = self.TENDERS_AGREEMENTS_DOCUMENTS_COLLECTION_PATH.format(
            tender_id, agreement_id
        )
        path = self.get_api_path(agreements_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def get_tender_agreement_contracts(self, tender_id, agreement_id, **kwargs):
        agreement_contracts_path = (
            self.TENDERS_AGREEMENTS_CONTRACTS_COLLECTION_PATH.format(
                tender_id, agreement_id
            )
        )
        path = self.get_api_path(agreement_contracts_path)
        return self.get(path, **kwargs)

    def patch_tender_agreement_contract(
        self, tender_id, agreement_id, contract_id, acc_token, json, **kwargs
    ):
        agreement_contracts_path = self.TENDERS_AGREEMENTS_CONTRACTS_PATH.format(
            tender_id, agreement_id, contract_id, acc_token
        )
        path = self.get_api_path(agreement_contracts_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def patch_tender_credentials(self, tender_id, acc_token, json, **kwargs):
        credentials_path = self.TENDERS_CREDENTIALS_PATH.format(tender_id)
        path = self.get_api_path(credentials_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_contract(self, contract_id, **kwargs):
        contracts_path = self.CONTRACTS_PATH.format(contract_id)
        path = self.get_api_path(contracts_path)
        return self.get(path, **kwargs)

    def patch_contract(self, contract_id, acc_token, json, **kwargs):
        contracts_path = self.CONTRACTS_PATH.format(contract_id)
        path = self.get_api_path(contracts_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def patch_contract_buyer_signer_info(self, contract_id, acc_token, json, **kwargs):
        contracts_path = self.CONTRACTS_BUYERS_SIGNER_INFO_PATH.format(contract_id)
        path = self.get_api_path(contracts_path, acc_token=acc_token)
        return self.put(path, json, **kwargs)

    def patch_contract_suppliers_signer_info(
        self, contract_id, acc_token, json, **kwargs
    ):
        contracts_path = self.CONTRACTS_SUPPLIERS_SIGNER_INFO_PATH.format(contract_id)
        path = self.get_api_path(contracts_path, acc_token=acc_token)
        return self.put(path, json, **kwargs)

    def patch_contract_credentials(self, contract_id, acc_token, json, **kwargs):
        credentials_path = self.CONTRACTS_CREDENTIALS_PATH.format(contract_id)
        path = self.get_api_path(credentials_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_agreement(self, agreement_id, **kwargs):
        agreements_path = self.AGREEMENTS_PATH.format(agreement_id)
        path = self.get_api_path(agreements_path)
        return self.get(path, **kwargs)


class DsApiClient(BaseApiClient):
    name = "ds"

    UPLOAD_PATH = "upload"

    def __init__(
        self, host, username=None, password=None, session=None, **request_kwargs
    ):
        super(DsApiClient, self).__init__(host, session=session, **request_kwargs)
        self.headers.update(
            {
                "Authorization": "Basic "
                + b64encode("{}:{}".format(username, password).encode()).decode()
            }
        )

    def post_document_upload(self, files, **kwargs):
        path = self.UPLOAD_PATH
        return self.post(path, files=files, **kwargs)
