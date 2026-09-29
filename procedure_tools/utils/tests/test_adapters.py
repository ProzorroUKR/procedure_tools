import logging
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
import requests
from urllib3.exceptions import NewConnectionError

from procedure_tools.utils import adapters
from procedure_tools.utils.stats import (
    RequestStats,
    TimedHTTPConnection,
    current_stats,
    format_request_stats,
    start_collecting,
    stop_collecting,
)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep-alive, so the pool reuses the connection

    def do_GET(self) -> None:  # pylint: disable=invalid-name
        body = b'{"data": "ok"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # pylint: disable=redefined-builtin
        pass


@pytest.fixture(name="server_url")
def server_url_fixture() -> Iterator[str]:
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


def stats_lines(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.getMessage().startswith("Request stats")]


def test_debug_stats_logged_per_request(server_url: str, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    session = requests.Session()
    adapters.mount(session, debug_stats=True)
    try:
        response = session.get(f"{server_url}/first")
        assert response.json() == {"data": "ok"}
        session.get(f"{server_url}/second")
    finally:
        session.close()
    lines = stats_lines(caplog)
    assert len(lines) == 2
    assert lines[0].startswith("Request stats: total ")
    assert "connect " in lines[0] and "reused" not in lines[0]
    assert "connection reused" in lines[1]  # keep-alive pool serves the second request
    assert "tls" not in lines[0]  # plain http
    assert "wait " in lines[0] and "download " in lines[0] and "(14 B)" in lines[0]
    assert current_stats() is None


def test_stats_not_logged_without_debug(server_url: str, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    session = requests.Session()
    adapters.mount(session)
    try:
        session.get(f"{server_url}/")
    finally:
        session.close()
    assert stats_lines(caplog) == []


def test_configure_debug_logging_toggles_stats(server_url: str, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    session = requests.Session()
    adapters.mount(session)
    adapters.configure_debug_logging(session, stats=True)
    try:
        session.get(f"{server_url}/")
    finally:
        session.close()
    assert len(stats_lines(caplog)) == 1


def test_stats_logged_when_the_request_fails(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    session = requests.Session()
    adapters.mount(session, debug_stats=True, max_retries_total=0)
    try:
        with pytest.raises(requests.exceptions.ConnectionError):
            session.get("http://127.0.0.1:9/", timeout=1)
    finally:
        session.close()
    lines = stats_lines(caplog)
    assert len(lines) == 1
    assert lines[0].startswith("Request stats (failed): total ")
    assert current_stats() is None


def test_timed_connection_records_into_current_stats() -> None:
    stats = start_collecting()
    try:
        connection = TimedHTTPConnection("127.0.0.1", 9, timeout=0.2)
        with pytest.raises(NewConnectionError):
            connection.connect()
        assert stats.connects == 1
        assert stats.connect_seconds > 0
        assert stats.tls_seconds == 0
    finally:
        stop_collecting()
    assert current_stats() is None


def test_format_request_stats() -> None:
    stats = RequestStats(
        attempts=2,
        connects=1,
        connect_seconds=0.0301,
        tls_seconds=0.0152,
        send_seconds=0.0007,
        wait_seconds=0.75,
        download_seconds=0.0123,
        total_seconds=0.8123,
        body_bytes=4300,
    )
    assert format_request_stats(stats) == (
        "total 812 ms, connect 30 ms + tls 15 ms, send 1 ms, wait 750 ms, download 12 ms (4.2 KB), 2 attempts"
    )
    reused = RequestStats(attempts=1, wait_seconds=0.1, total_seconds=0.1)
    assert format_request_stats(reused) == "total 100 ms, connection reused, send 0 ms, wait 100 ms"
