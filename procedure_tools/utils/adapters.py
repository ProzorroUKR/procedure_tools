import logging

from requests import ConnectionError, adapters
from urllib3 import Retry

DEFAULT_TIMEOUT = 60
DEFAULT_MAX_RETRIES = 5
DEFAULT_RETRY_FORCELIST = (408, 409, 412, 429, 500, 502, 503, 504)
DEFAULT_RETRY_ALLOWED_METHODS = frozenset(
    (
        "HEAD",
        "GET",
        "PUT",
        "PATCH",
        "POST",
        "DELETE",
        "OPTIONS",
        "TRACE",
    )
)
DEFAULT_RETRY_BACKOFF_FACTOR = 0.5
DEFAULT_RETRY_BACKOFF_MAX = 60.0


class HTTPAdapter(adapters.HTTPAdapter):
    def __init__(self, timeout, max_retries):
        self.timeout = timeout
        super(HTTPAdapter, self).__init__(max_retries=max_retries)

    def send(self, request, *args, **kwargs):
        exc = None
        for attempt in range(max(1, 1 + DEFAULT_MAX_RETRIES)):
            if attempt > 0:
                logging.info("Retrying after connection error")
            try:
                kwargs["timeout"] = self.timeout
                logging.info(f"[{request.method}] {request.url}")
                return super(HTTPAdapter, self).send(request, *args, **kwargs)
            except ConnectionError as exc:
                logging.info("Connection error: %s", exc)
                continue
        if exc:
            raise exc


def mount(
    session,
    timeout=DEFAULT_TIMEOUT,
    max_retries_total=DEFAULT_MAX_RETRIES,
    status_forcelist=DEFAULT_RETRY_FORCELIST,
    allowed_methods=DEFAULT_RETRY_ALLOWED_METHODS,
    backoff_factor=DEFAULT_RETRY_BACKOFF_FACTOR,
    backoff_max=DEFAULT_RETRY_BACKOFF_MAX,
):
    max_retries = Retry(
        total=max_retries_total,
        status_forcelist=status_forcelist,
        allowed_methods=allowed_methods,
        backoff_factor=backoff_factor,
        backoff_max=backoff_max,
        raise_on_redirect=False,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(timeout, max_retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
