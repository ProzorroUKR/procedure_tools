import json
import re
from typing import Any
from unittest import mock

import pytest

from procedure_tools.utils import handlers
from procedure_tools.utils.handlers import (
    ProcedureExit,
    default_error_handler,
    flatten_payload,
    format_error_summary,
    format_log_all_fields,
)

ANSI = re.compile(r"\x1b\[[0-9;]*m")

ERROR_PAYLOAD: dict[str, Any] = {
    "status": "error",
    "errors": [
        {"location": "body", "name": "tendererAction", "description": "Rogue field"},
        {"location": "body", "name": "objections", "description": [{"sequenceNumber": ["This field is required."]}]},
    ],
}


class FakeResponse:
    def __init__(self, payload: Any, text: str | None = None) -> None:
        self._payload = payload
        self.text = json.dumps(payload) if text is None else text

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("not json")
        return self._payload


def test_flatten_payload_walks_to_every_leaf() -> None:
    assert flatten_payload(ERROR_PAYLOAD) == [
        ("status", "error"),
        ("errors[0].location", "body"),
        ("errors[0].name", "tendererAction"),
        ("errors[0].description", "Rogue field"),
        ("errors[1].location", "body"),
        ("errors[1].name", "objections"),
        ("errors[1].description[0].sequenceNumber[0]", "This field is required."),
    ]
    assert flatten_payload({"data": {}}) == [("data", {})]
    assert flatten_payload("plain") == [("value", "plain")]


def test_format_log_all_fields_aligns_like_success_output() -> None:
    lines = ANSI.sub("", format_log_all_fields(ERROR_PAYLOAD)).rstrip("\n").split("\n")
    assert lines[0].startswith(" - status")
    assert lines[3].startswith(" - errors[0].description")
    # values start in the same column on every line
    columns = {len(line) - len(line.split("  ")[-1].lstrip()) for line in lines if line.count("  ")}
    assert len(columns) == 1
    assert "This field is required." in lines[-1]


def test_format_error_summary_joins_errors() -> None:
    summary = format_error_summary(ERROR_PAYLOAD, json.dumps(ERROR_PAYLOAD))
    assert summary == (
        'body.tendererAction: Rogue field; body.objections: [{"sequenceNumber": ["This field is required."]}]'
    )
    assert format_error_summary(["x"], '["x"]') == '["x"]'


def logged(info: mock.Mock) -> str:
    return ANSI.sub("", "".join(str(call.args[0]) for call in info.call_args_list))


def test_default_error_handler_logs_fields_and_raises() -> None:
    with mock.patch.object(handlers.logger, "info") as info, pytest.raises(ProcedureExit) as e:
        default_error_handler(FakeResponse(ERROR_PAYLOAD))  # type: ignore[arg-type]
    assert e.value.message == (
        'body.tendererAction: Rogue field; body.objections: [{"sequenceNumber": ["This field is required."]}]'
    )
    text = logged(info)
    assert "Response error:" in text and " - errors[0].name" in text and "Rogue field" in text


def test_default_error_handler_falls_back_to_text() -> None:
    with mock.patch.object(handlers.logger, "info") as info, pytest.raises(ProcedureExit) as e:
        default_error_handler(FakeResponse(None, text="<html>Bad gateway</html>"))  # type: ignore[arg-type]
    assert e.value.message == "<html>Bad gateway</html>"
    assert "Response text:" in logged(info)
