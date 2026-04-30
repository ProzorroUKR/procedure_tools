import logging
import json
import os
import sys

from requests import ConnectionError, adapters
from urllib3 import Retry
from urllib.parse import urlsplit

from procedure_tools.utils.style import (
    fore_debug,
    fore_info,
    fore_method,
    fore_status_code,
    fore_warning,
)

try:
    from pygments import highlight
    from pygments.formatters import TerminalFormatter
    from pygments.lexers import JsonLexer
except ImportError:
    highlight = None
    TerminalFormatter = None
    JsonLexer = None

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
HTTP_LOG_PAD = 3


class RetryingHTTPAdapter(adapters.HTTPAdapter):
    def __init__(self, timeout, max_retries):
        self.timeout = timeout

        super(RetryingHTTPAdapter, self).__init__(max_retries=max_retries)

    def send(self, request, *args, **kwargs):
        last_exc = None
        for attempt in range(max(1, 1 + DEFAULT_MAX_RETRIES)):
            if attempt > 0:
                logging.info("Retrying after connection error")
            try:
                kwargs["timeout"] = self.timeout
                return super(RetryingHTTPAdapter, self).send(request, *args, **kwargs)
            except ConnectionError as err:
                last_exc = err
                logging.info("Connection error: %s", err)
                continue
        if last_exc:
            raise last_exc


class LoggingHTTPAdapter(adapters.HTTPAdapter):
    def __init__(
        self,
        transport_adapter,
        debug_request=False,
        debug_json_level=None,
        debug_exclude_paths=(),
    ):
        self.transport_adapter = transport_adapter
        self.debug_request = debug_request
        self.debug_json_level = debug_json_level
        self.debug_exclude_paths = tuple(debug_exclude_paths)
        super(LoggingHTTPAdapter, self).__init__()

    def set_debug_options(self, enabled=False, json_level=None, exclude_paths=()):
        self.debug_request = enabled
        self.debug_json_level = json_level
        self.debug_exclude_paths = tuple(exclude_paths or ())

    def fold_json(self, data, max_level, current_level=0):
        if max_level is None:
            return data

        if isinstance(data, dict):
            if current_level >= max_level:
                return {"...": f"{len(data)} keys folded"}
            return {key: self.fold_json(value, max_level, current_level + 1) for key, value in data.items()}

        if isinstance(data, list):
            if current_level >= max_level:
                return [f"... {len(data)} items folded"]
            return [self.fold_json(item, max_level, current_level + 1) for item in data]

        if isinstance(data, tuple):
            if current_level >= max_level:
                return ("... tuple folded",)
            return tuple(self.fold_json(item, max_level, current_level + 1) for item in data)

        return data

    def colorize_json_text(self, text):
        if not (highlight and TerminalFormatter and JsonLexer):
            return text
        if os.getenv("NO_COLOR"):
            return text
        try:
            if not sys.stdout.isatty():
                return text
        except Exception:
            return text
        try:
            return highlight(text, JsonLexer(), TerminalFormatter()).rstrip("\n")
        except Exception:
            return text

    def format_data(self, data):
        data = self.fold_json(data, self.debug_json_level)
        try:
            text = json.dumps(data, ensure_ascii=False, indent=4)
        except TypeError:
            text = str(data)
        return self.colorize_json_text(text)

    def format_headers(self, headers):
        return "\n".join(f"{header}: {fore_info(str(value))}" for header, value in headers.items())

    def format_cookies(self, cookies):
        return "; ".join(f"{name}={fore_info(str(value))}" for name, value in cookies.items())

    def format_http_request_start_line(self, request):
        parsed_url = urlsplit(request.url or "")
        target = parsed_url.path or "/"
        if parsed_url.query:
            target = f"{target}?{parsed_url.query}"
        method_text = fore_method(request.method)
        target_text = fore_info(target)
        protocol_text = fore_debug("HTTP/1.1")
        return f"{method_text} {target_text} {protocol_text}"

    def get_http_host_header(self, url):
        parsed_url = urlsplit(url or "")
        hostname = parsed_url.hostname
        if not hostname:
            return ""
        port = parsed_url.port
        if port and not (
            (parsed_url.scheme == "http" and port == 80) or (parsed_url.scheme == "https" and port == 443)
        ):
            return f"{hostname}:{port}"
        return hostname

    def format_http_response_start_line(self, response):
        status_text = fore_status_code(response.status_code)
        reason_text = fore_warning(response.reason) if response.reason else ""
        protocol_text = fore_debug("HTTP/1.1")
        if reason_text:
            return f"{protocol_text} {status_text} {reason_text}"
        return f"{protocol_text} {status_text}"

    def should_log_exchange(self, url):
        if not self.debug_request:
            return False
        return not any(fragment and fragment in (url or "") for fragment in self.debug_exclude_paths)

    def format_request_body(self, request):
        content_type = (request.headers or {}).get("Content-Type", "")
        body = request.body
        if body is None:
            return None
        if "multipart/form-data" in content_type:
            return "(multipart/form-data file upload)"
        if isinstance(body, bytes):
            try:
                body_text = body.decode("utf-8")
            except UnicodeDecodeError:
                body_text = body.decode("latin-1", errors="replace")
        else:
            body_text = str(body)
        if "application/json" in content_type:
            try:
                return self.format_data(json.loads(body_text))
            except (json.JSONDecodeError, TypeError):
                return body_text
        return body_text

    def pad_log_lines(self, text, pad=HTTP_LOG_PAD):
        return "\n".join(f"{'':<{pad}}{line}" for line in (text or "").splitlines())

    def get_debug_request(self, request):
        log_lines = [self.format_http_request_start_line(request)]
        request_headers = dict(request.headers or {})
        if "Host" not in request_headers:
            host_value = self.get_http_host_header(request.url)
            if host_value:
                request_headers = {"Host": host_value, **request_headers}
        if request_headers:
            log_lines.append(self.format_headers(request_headers))
            log_lines.append("")
        request_body = self.format_request_body(request)
        if request_body is not None:
            log_lines.append(request_body)
        return "\n".join(log_lines)

    def get_debug_response(self, response):
        log_lines = [self.format_http_response_start_line(response)]
        if response.headers:
            log_lines.append(self.format_headers(dict(response.headers)))
            log_lines.append("")
        text = response.text
        if text:
            try:
                response_text = self.format_data(json.loads(text))
            except json.JSONDecodeError:
                response_text = text
            log_lines.append(response_text)
        else:
            log_lines.append("(empty body)")
        return "\n".join(log_lines)

    def send(self, request, *args, **kwargs):
        logging.info(f"{request.method} {request.url}")
        if self.should_log_exchange(request.url):
            debug_request = self.get_debug_request(request)
            logging.info(f"HTTP Request:\n\n{self.pad_log_lines(debug_request)}\n")
        response = self.transport_adapter.send(request, *args, **kwargs)
        if self.should_log_exchange(request.url):
            debug_response = self.get_debug_response(response)
            logging.info(f"HTTP Response:\n\n{self.pad_log_lines(debug_response)}\n")
        else:
            status_text = fore_status_code(response.status_code)
            reason_text = fore_warning(response.reason) if response.reason else ""
            logging.info(f"Response status: {status_text} {reason_text}\n")
        return response

    def close(self):
        self.transport_adapter.close()
        super(LoggingHTTPAdapter, self).close()


def mount(
    session,
    timeout=DEFAULT_TIMEOUT,
    max_retries_total=DEFAULT_MAX_RETRIES,
    status_forcelist=DEFAULT_RETRY_FORCELIST,
    allowed_methods=DEFAULT_RETRY_ALLOWED_METHODS,
    backoff_factor=DEFAULT_RETRY_BACKOFF_FACTOR,
    backoff_max=DEFAULT_RETRY_BACKOFF_MAX,
    debug_request=False,
    debug_json_level=None,
    debug_exclude_paths=(),
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
    transport_adapter = RetryingHTTPAdapter(
        timeout=timeout,
        max_retries=max_retries,
    )
    adapter = LoggingHTTPAdapter(
        transport_adapter=transport_adapter,
        debug_request=debug_request,
        debug_json_level=debug_json_level,
        debug_exclude_paths=debug_exclude_paths,
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)


def configure_debug_logging(session, enabled=False, json_level=None, exclude_paths=()):
    for adapter in set(session.adapters.values()):
        if isinstance(adapter, LoggingHTTPAdapter):
            adapter.set_debug_options(enabled=enabled, json_level=json_level, exclude_paths=exclude_paths)


def configure_urllib3_logging(debug):
    level = logging.DEBUG if debug else logging.WARNING
    logging.getLogger("urllib3").setLevel(level)
    for name in logging.root.manager.loggerDict:
        if name == "urllib3" or (isinstance(name, str) and name.startswith("urllib3.")):
            logging.getLogger(name).setLevel(level)
