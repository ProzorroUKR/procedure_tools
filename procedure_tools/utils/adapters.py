import logging

from requests import adapters
from urllib3 import Retry

DEFAULT_TIMEOUT = 60
DEFAULT_MAX_RETRIES = 5
DEFAULT_RETRY_FORCELIST = (408, 409, 412, 429, 500, 502, 503, 504)


class HTTPAdapter(adapters.HTTPAdapter):

    def __init__(self, timeout=DEFAULT_TIMEOUT, max_retries=DEFAULT_MAX_RETRIES, *args, **kwargs):
        self.timeout = timeout
        super(HTTPAdapter, self).__init__(max_retries=max_retries, *args, **kwargs)

    def send(self, request, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        logging.info("[{}] {}".format(request.method, request.url))
        return super(HTTPAdapter, self).send(request, *args, **kwargs)


def mount(session, max_reties=DEFAULT_MAX_RETRIES, status_forcelist=DEFAULT_RETRY_FORCELIST):
    retry_strategy = Retry(
        total=max_reties,
        status_forcelist=status_forcelist,
        raise_on_redirect=False,
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
