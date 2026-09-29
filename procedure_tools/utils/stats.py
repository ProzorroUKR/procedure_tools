"""Timing of one HTTP request, collected from the urllib3 connection while it runs.

The timed connection classes record what they do into the ``RequestStats`` of the
current thread, so an adapter sees the connect, send and wait times of every
attempt urllib3 made for a request, including its retries.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any

from urllib3 import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.connection import HTTPConnection, HTTPSConnection

_local = threading.local()


@dataclass
class RequestStats:
    attempts: int = 0  # requests sent, more than one when urllib3 retried
    connects: int = 0  # new connections, zero when a pooled one was reused
    connect_seconds: float = 0.0  # DNS lookup and TCP connect
    tls_seconds: float = 0.0  # TLS handshake
    send_seconds: float = 0.0  # writing the request
    wait_seconds: float = 0.0  # from the request sent to the response headers
    download_seconds: float = 0.0  # reading the response body
    total_seconds: float = 0.0
    body_bytes: int | None = None


def start_collecting() -> RequestStats:
    stats = RequestStats()
    _local.stats = stats
    return stats


def stop_collecting() -> None:
    _local.stats = None


def current_stats() -> RequestStats | None:
    stats: RequestStats | None = getattr(_local, "stats", None)
    return stats


def format_ms(seconds: float) -> str:
    return f"{seconds * 1000:.0f} ms"


def format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def format_request_stats(stats: RequestStats) -> str:
    if stats.connects:
        connection = f"connect {format_ms(stats.connect_seconds)}"
        if stats.tls_seconds:
            connection += f" + tls {format_ms(stats.tls_seconds)}"
        if stats.connects > 1:
            connection += f" ({stats.connects} connections)"
    else:
        connection = "connection reused"
    parts = [
        f"total {format_ms(stats.total_seconds)}",
        connection,
        f"send {format_ms(stats.send_seconds)}",
        f"wait {format_ms(stats.wait_seconds)}",
    ]
    if stats.body_bytes is not None:
        parts.append(f"download {format_ms(stats.download_seconds)} ({format_bytes(stats.body_bytes)})")
    if stats.attempts > 1:
        parts.append(f"{stats.attempts} attempts")
    return ", ".join(parts)


class _TimedConnectionMixin:
    """Records connect, send and wait times into the stats of the current thread."""

    def _new_conn(self) -> Any:
        stats = current_stats()
        started = time.perf_counter()
        try:
            return super()._new_conn()  # type: ignore[misc]
        finally:
            if stats:
                stats.connects += 1
                stats.connect_seconds += time.perf_counter() - started

    def request(self, *args: Any, **kwargs: Any) -> None:
        stats = current_stats()
        started = time.perf_counter()
        try:
            super().request(*args, **kwargs)  # type: ignore[misc]
        finally:
            if stats:
                stats.attempts += 1
                stats.send_seconds += time.perf_counter() - started

    def getresponse(self) -> Any:
        stats = current_stats()
        started = time.perf_counter()
        try:
            return super().getresponse()  # type: ignore[misc]
        finally:
            if stats:
                stats.wait_seconds += time.perf_counter() - started


class TimedHTTPConnection(_TimedConnectionMixin, HTTPConnection):
    pass


class TimedHTTPSConnection(_TimedConnectionMixin, HTTPSConnection):
    def connect(self) -> None:
        stats = current_stats()
        started = time.perf_counter()
        connect_before = stats.connect_seconds if stats else 0.0
        try:
            super().connect()  # pylint: disable=no-member
        finally:
            if stats:
                # what connect() spent past the socket connect is the TLS handshake
                tcp_seconds = stats.connect_seconds - connect_before
                stats.tls_seconds += max(0.0, time.perf_counter() - started - tcp_seconds)


class TimedHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls = TimedHTTPConnection


class TimedHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls = TimedHTTPSConnection


TIMED_POOL_CLASSES_BY_SCHEME: dict[str, type[HTTPConnectionPool]] = {
    "http": TimedHTTPConnectionPool,
    "https": TimedHTTPSConnectionPool,
}
