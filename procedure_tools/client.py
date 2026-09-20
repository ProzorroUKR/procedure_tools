import logging
from base64 import b64encode
from collections.abc import Callable
from copy import copy
from datetime import timedelta
from typing import Any, ClassVar
from urllib.parse import urljoin

import requests

from procedure_tools.utils import adapters
from procedure_tools.utils.date import get_utcnow, parse_date_header
from procedure_tools.utils.handlers import (
    client_init_response_handler,
    response_handler,
)
from procedure_tools.version import __version__

logger = logging.getLogger(__name__)


API_PATH_PREFIX_DEFAULT = "/api/0/"


class BaseApiClient:
    name = "api"

    SPORE_PATH = "spore"

    HEADERS_DEFAULT: ClassVar[dict[str, str]] = {
        "User-Agent": f"procedure_tools/{__version__}",
    }

    def __init__(
        self,
        host: str,
        session: requests.Session | None = None,
        debug_request: bool = False,
        debug_json_level: int | None = None,
        debug: bool = False,
        **kwargs: Any,
    ) -> None:
        logger.info(f"Initializing {self.name} client\n")
        self.host = host
        self.kwargs = kwargs
        self.debug_request = debug_request
        self.debug_json_level = debug_json_level
        adapters.configure_urllib3_logging(debug)
        if session:
            self.session = session
            adapters.configure_debug_logging(
                self.session,
                enabled=self.debug_request,
                json_level=self.debug_json_level,
                exclude_paths=(self.SPORE_PATH,),
            )
        else:
            self.session = requests.Session()
            adapters.mount(
                self.session,
                debug_request=self.debug_request,
                debug_json_level=self.debug_json_level,
                debug_exclude_paths=(self.SPORE_PATH,),
            )
        self.headers = copy(self.HEADERS_DEFAULT)

    def get_url(self, api_path: str) -> str:
        return urljoin(self.host, api_path)

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        request_kwargs = copy(kwargs)
        auth_token = request_kwargs.pop("auth_token", None)
        success_handler = request_kwargs.pop("success_handler", None)
        error_handler = request_kwargs.pop("error_handler", None)
        request_kwargs["headers"] = copy(self.headers)
        request_kwargs["headers"].update({"Authorization": "Bearer " + auth_token} if auth_token else {})
        request_kwargs["headers"].update(kwargs.get("headers", {}))
        url = self.get_url(path)
        response = self.session.request(method=method, url=url, **request_kwargs)
        handlers: dict[str, Callable[..., None]] = {}
        if success_handler:
            handlers["success_handler"] = success_handler
        if error_handler:
            handlers["error_handler"] = error_handler
        response_handler(response, **handlers)
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, json: Any = None, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Any = None, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: Any = None, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, json=json, **kwargs)


class CDBClient(BaseApiClient):
    name = "cdb"

    SPORE_PATH = "spore"

    def __init__(  # pylint: disable=unused-argument
        self,
        host: str,
        auth_token: str | None = None,
        path_prefix: str = API_PATH_PREFIX_DEFAULT,
        session: requests.Session | None = None,
        **request_kwargs: Any,
    ) -> None:
        super().__init__(host, session=session, **request_kwargs)
        self.path_prefix = path_prefix
        self.headers.update({"Content-Type": "application/json"})
        # GET request to retrieve cookies and server time (via request() so debug request logging applies)
        response = self.get(self.get_api_path(self.SPORE_PATH))
        # Calculate client time delta with server
        client_datetime = get_utcnow()
        try:
            server_datetime = parse_date_header(response.headers.get("date", ""))
            self.client_timedelta = server_datetime - client_datetime
        except (TypeError, ValueError):
            self.client_timedelta = timedelta()
        client_init_response_handler(response, self.client_timedelta)

    def get_api_path(self, path: str, acc_token: str | None = None) -> str:
        return urljoin(
            self.path_prefix,
            urljoin(path, f"?acc_token={acc_token}" if acc_token else None),
        )

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        path = self.get_api_path(path, acc_token=kwargs.pop("acc_token", None))
        return super().request(method, path, **kwargs)


class DSClient(BaseApiClient):
    name = "ds"

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        session: requests.Session | None = None,
        **request_kwargs: Any,
    ) -> None:
        super().__init__(host, session=session, **request_kwargs)
        self.headers.update({"Authorization": "Basic " + b64encode(f"{username}:{password}".encode()).decode()})

    def post_document_upload(self, files: Any, **kwargs: Any) -> requests.Response:
        return self.post("upload", files=files, **kwargs)
