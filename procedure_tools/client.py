from __future__ import absolute_import

from copy import deepcopy
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests

from procedure_tools.utils.handlers import response_handler

API_PATH_PREFIX_DEFAULT = '/api/0/'


def get_api_path(path, path_prefix=API_PATH_PREFIX_DEFAULT, acc_token=None):
    return urljoin(path_prefix, urljoin(path, '?acc_token={}'.format(acc_token) if acc_token else None))


def get_api_url(host, api_path):
    return urljoin(host, api_path)


class BaseApiClient(object):
    SPORE_PATH = 'spore'
    HEADERS_DEFAULT = {
        'Content-Type': 'application/json'
    }

    def __init__(self, host, auth_token=None, path_prefix=API_PATH_PREFIX_DEFAULT, **request_kwargs):
        self.host = host
        self.path_prefix = path_prefix
        self._set_authorization_header(request_kwargs, auth_token)
        self._set_server_id_cookie(request_kwargs)
        self.kwargs = request_kwargs

    @staticmethod
    def _pop_handlers(kwargs, success_handler=None, error_handler=None):
        return dict((k, v) for k, v in dict(
            success_handler=kwargs.pop('success_handler', success_handler),
            error_handler=kwargs.pop('error_handler', error_handler)
        ).items() if v is not None)

    def _set_authorization_header(self, request_kwargs, auth_token):
        headers = self.HEADERS_DEFAULT
        headers.update(request_kwargs.pop('headers', {}))
        if auth_token:
            headers.update({'Authorization': 'Bearer ' + auth_token})
        request_kwargs.update(dict(headers=headers))

    def _set_server_id_cookie(self, request_kwargs):
        url = self._get_api_url(get_api_path(self.SPORE_PATH, self.path_prefix))
        server_id = requests.get(url).cookies.get('SERVER_ID')
        cookies = request_kwargs.pop('cookies', {})
        cookies.update({'SERVER_ID': server_id})
        request_kwargs.update(dict(cookies=cookies))

    def _get_api_path(self, path, acc_token=None):
        return get_api_path(path, path_prefix=self.path_prefix, acc_token=acc_token)

    def _get_api_url(self, api_path):
        return get_api_url(self.host, api_path)

    def get(self, path, **kwargs):
        request_kwargs = deepcopy(self.kwargs)
        handlers = self._pop_handlers(kwargs)
        request_kwargs.update(kwargs)
        url = self._get_api_url(path)
        response = requests.get(url=url, **request_kwargs)
        response_handler(response, **handlers)
        return response

    def post(self, path, json, **kwargs):
        request_kwargs = deepcopy(self.kwargs)
        handlers = self._pop_handlers(kwargs)
        request_kwargs.update(kwargs)
        url = self._get_api_url(path)
        response = requests.post(url=url, json=json, **request_kwargs)
        response_handler(response, **handlers)
        return response

    def patch(self, path, json, **kwargs):
        request_kwargs = deepcopy(self.kwargs)
        handlers = self._pop_handlers(kwargs)
        request_kwargs.update(kwargs)
        url = self._get_api_url(path)
        response = requests.patch(url=url, json=json, **request_kwargs)
        response_handler(response, **handlers)
        return response


class TendersApiClient(BaseApiClient):
    TENDERS_COLLECTION_PATH = 'tenders'
    TENDERS_PATH = 'tenders/{}'
    BIDS_COLLECTION_PATH = 'tenders/{}/bids'
    AWARDS_COLLECTION_PATH = 'tenders/{}/awards'
    AWARDS_PATH = 'tenders/{}/awards/{}'
    CONTRACTS_COLLECTION_PATH = 'tenders/{}/contracts'
    CONTRACTS_PATH = 'tenders/{}/contracts/{}'
    QUALIFICATIONS_COLLECTION_PATH = 'tenders/{}/qualifications'
    QUALIFICATIONS_PATH = 'tenders/{}/qualifications/{}'
    AGREEMENTS_COLLECTION_PATH = 'tenders/{}/agreements'
    AGREEMENTS_PATH = 'tenders/{}/agreements/{}'
    AGREEMENT_CONTRACT_COLLECTION_PATH = 'tenders/{}/agreements/{}/contracts'
    AGREEMENT_CONTRACT_PATH = 'tenders/{}/agreements/{}/contracts/{}'
    CREDENTIALS_PATH = 'tenders/{}/credentials'

    def get_tender(self, tender_id, **kwargs):
        tenders_path = self.TENDERS_PATH.format(tender_id)
        path = self._get_api_path(tenders_path)
        return self.get(path, **kwargs)

    def post_tender(self, json, **kwargs):
        tenders_path = self.TENDERS_COLLECTION_PATH
        path = self._get_api_path(tenders_path)
        return self.post(path, json, **kwargs)

    def patch_tender(self, tender_id, acc_token, json, **kwargs):
        tenders_path = self.TENDERS_PATH.format(tender_id)
        path = self._get_api_path(tenders_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_bids(self, tender_id, **kwargs):
        awards_path = self.BIDS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(awards_path)
        return self.get(path, **kwargs)

    def post_bid(self, tender_id, json, **kwargs):
        bids_path = self.BIDS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(bids_path)
        return self.post(path, json, **kwargs)

    def get_qualifications(self, tender_id, **kwargs):
        qualifications_path = self.QUALIFICATIONS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(qualifications_path)
        return self.get(path, **kwargs)

    def get_qualification(self, tender_id, qualification_id, **kwargs):
        qualifications_path = self.QUALIFICATIONS_PATH.format(tender_id, qualification_id)
        path = self._get_api_path(qualifications_path)
        return self.get(path, **kwargs)

    def patch_qualification(self, tender_id, qualification_id, acc_token, json, **kwargs):
        qualifications_path = self.QUALIFICATIONS_PATH.format(tender_id, qualification_id, acc_token)
        path = self._get_api_path(qualifications_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_awards(self, tender_id, **kwargs):
        awards_path = self.AWARDS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(awards_path)
        return self.get(path, **kwargs)

    def get_award(self, tender_id, award_id, **kwargs):
        awards_path = self.AWARDS_PATH.format(tender_id, award_id)
        path = self._get_api_path(awards_path)
        return self.get(path, **kwargs)

    def post_award(self, tender_id, acc_token, json, **kwargs):
        awards_path = self.AWARDS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(awards_path, acc_token=acc_token)
        return self.post(path, json, **kwargs)

    def patch_award(self, tender_id, award_id, acc_token, json, **kwargs):
        awards_path = self.AWARDS_PATH.format(tender_id, award_id, acc_token)
        path = self._get_api_path(awards_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_contracts(self, tender_id, **kwargs):
        awards_path = self.CONTRACTS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(awards_path)
        return self.get(path, **kwargs)

    def patch_contract(self, tender_id, contract_id, acc_token, json, **kwargs):
        awards_path = self.CONTRACTS_PATH.format(tender_id, contract_id, acc_token)
        path = self._get_api_path(awards_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_agreements(self, tender_id, **kwargs):
        agreements_path = self.AGREEMENTS_COLLECTION_PATH.format(tender_id)
        path = self._get_api_path(agreements_path)
        return self.get(path, **kwargs)

    def patch_agreement(self, tender_id, agreement_id, acc_token, json, **kwargs):
        agreements_path = self.AGREEMENTS_PATH.format(tender_id, agreement_id, acc_token)
        path = self._get_api_path(agreements_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def get_agreement_contracts(self, tender_id, agreement_id, **kwargs):
        agreement_contracts_path = self.AGREEMENT_CONTRACT_COLLECTION_PATH.format(tender_id, agreement_id)
        path = self._get_api_path(agreement_contracts_path)
        return self.get(path, **kwargs)

    def patch_agreement_contract(self, tender_id, agreement_id, contract_id, acc_token, json, **kwargs):
        agreement_contracts_path = self.AGREEMENT_CONTRACT_PATH.format(tender_id, agreement_id, contract_id, acc_token)
        path = self._get_api_path(agreement_contracts_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def patch_credentials(self, tender_id, acc_token, json, **kwargs):
        credentials_path = self.CREDENTIALS_PATH.format(tender_id)
        path = self._get_api_path(credentials_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)


class AgreementsApiClient(BaseApiClient):
    AGREEMENTS_PATH = 'agreements/{}'

    def get_agreement(self, agreement_id, **kwargs):
        agreements_path = self.AGREEMENTS_PATH.format(agreement_id)
        path = self._get_api_path(agreements_path)
        return self.get(path, **kwargs)


class ContractsApiClient(BaseApiClient):
    CONTRACTS_PATH = 'contracts/{}'
    CREDENTIALS_PATH = 'contracts/{}/credentials'

    def get_contract(self, contract_id, **kwargs):
        contracts_path = self.CONTRACTS_PATH.format(contract_id)
        path = self._get_api_path(contracts_path)
        return self.get(path, **kwargs)

    def patch_credentials(self, contract_id, acc_token, json, **kwargs):
        credentials_path = self.CREDENTIALS_PATH.format(contract_id)
        path = self._get_api_path(credentials_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)


class PlansApiClient(BaseApiClient):
    PLANS_COLLECTION_PATH = 'plans'
    PLANS_PATH = 'plans/{}'
    TENDERS_COLLECTION_PATH = 'plans/{}/tenders'

    def get_plan(self, plan_id, **kwargs):
        contracts_path = self.PLANS_PATH.format(plan_id)
        path = self._get_api_path(contracts_path)
        return self.get(path, **kwargs)

    def post_plan(self, json, **kwargs):
        tenders_path = self.PLANS_COLLECTION_PATH
        path = self._get_api_path(tenders_path)
        return self.post(path, json, **kwargs)

    def patch_plan(self, plan_id, acc_token, json, **kwargs):
        tenders_path = self.PLANS_COLLECTION_PATH.format(plan_id)
        path = self._get_api_path(tenders_path, acc_token=acc_token)
        return self.patch(path, json, **kwargs)

    def post_tender(self, plan_id, json, **kwargs):
        tenders_path = self.TENDERS_COLLECTION_PATH.format(plan_id)
        path = self._get_api_path(tenders_path)
        return self.post(path, json, **kwargs)
