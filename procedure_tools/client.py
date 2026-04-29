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


def configure_urllib3_logging(debug):
    level = logging.DEBUG if debug else logging.WARNING
    logging.getLogger("urllib3").setLevel(level)
    for name in logging.root.manager.loggerDict:
        if name == "urllib3" or (isinstance(name, str) and name.startswith("urllib3.")):
            logging.getLogger(name).setLevel(level)


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
        configure_urllib3_logging(debug)
        if session:
            self.session = session
        else:
            self.session = requests.Session()
            adapters.mount(self.session)
        self.headers = copy(self.HEADERS_DEFAULT)

    def get_url(self, api_path):
        return urljoin(self.host, api_path)

    def format_data(self, data):
        try:
            text = json.dumps(data, ensure_ascii=False, indent=4)
        except TypeError:
            text = str(data)
        return text

    def log_debug_exchange(self, method, url, request_kwargs, response):
        """Log method, URL, status, and bodies at INFO when --debug (visible with default logging)."""
        logging.info("%s %s -> %s", method, url, response.status_code)
        if request_kwargs.get("json") is not None:
            logging.info("Request:\n %s", self.format_data(request_kwargs["json"]))
        elif request_kwargs.get("data") is not None:
            logging.info("Request data:\n %s", request_kwargs["data"])
        elif request_kwargs.get("files"):
            logging.info("Request: multipart/form-data (file upload)")
        text = response.text
        if text:
            try:
                data = json.loads(text)
                response_text = self.format_data(data)
            except json.JSONDecodeError:
                response_text = text
            logging.info("Response:\n %s", response_text)
        else:
            logging.info("Response: (empty body)")

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
            self.log_debug_exchange(method, url, request_kwargs, response)
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
        # GET request to retrieve cookies and server time (via request() so --debug applies)
        response = self.get(self.get_api_path(self.SPORE_PATH))
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
