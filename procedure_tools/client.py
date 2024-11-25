import json
import logging
from base64 import b64encode
from copy import copy
from datetime import timedelta
from urllib.parse import urljoin

import requests

from procedure_tools.utils import adapters
from procedure_tools.utils.date import get_utcnow, parse_date_header
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
        "User-Agent": f"procedure_tools/{__version__}",
    }

    def __init__(
        self,
        host,
        session=None,
        debug=False,
        **kwargs,
    ):
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
        request_kwargs["headers"].update({"Authorization": "Bearer " + auth_token} if auth_token else {})
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


class CDBClient(BaseApiClient):
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
        super(CDBClient, self).__init__(host, session=session, **request_kwargs)
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
            urljoin(path, f"?acc_token={acc_token}" if acc_token else None),
        )

    def request(self, method, path, **kwargs):
        path = self.get_api_path(path, acc_token=kwargs.pop("acc_token", None))
        return super(CDBClient, self).request(method, path, **kwargs)


class DSClient(BaseApiClient):
    name = "ds"

    def __init__(
        self,
        host,
        username=None,
        password=None,
        session=None,
        **request_kwargs,
    ):
        super(DSClient, self).__init__(host, session=session, **request_kwargs)
        self.headers.update({"Authorization": "Basic " + b64encode(f"{username}:{password}".encode()).decode()})

    def post_document_upload(self, files, **kwargs):
        return self.post("upload", files=files, **kwargs)
