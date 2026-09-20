import json
import logging
from collections.abc import Callable
from datetime import timedelta
from typing import Any

import requests

from procedure_tools.utils.date import client_timedelta_string
from procedure_tools.utils.style import fore_error, fore_info

logger = logging.getLogger(__name__)


PAD = 20

EX_OK = 0
EX_DATAERR = 65


class ProcedureExit(SystemExit):
    def __init__(self, code: int, message: str | None = None) -> None:
        super().__init__(code)
        self.message = message


def format_log_entry(label: str, value: str) -> str:
    return f" - {label:<{PAD}} {fore_info(value)}\n"


def parse_json_path(path: str) -> list[tuple[str, str | int | None]]:
    tokens: list[tuple[str, str | int | None]] = []
    buffer: list[str] = []
    i = 0
    while i < len(path):
        char = path[i]
        if char == ".":
            if buffer:
                tokens.append(("field", "".join(buffer)))
                buffer = []
            i += 1
            continue

        if char == "[":
            if buffer:
                tokens.append(("field", "".join(buffer)))
                buffer = []

            close_bracket_index = path.find("]", i + 1)
            if close_bracket_index == -1:
                return []

            index = path[i + 1 : close_bracket_index]
            if index == "*":
                tokens.append(("wildcard", None))
            elif index.isdigit():
                tokens.append(("index", int(index)))
            else:
                return []

            i = close_bracket_index + 1
            continue

        buffer.append(char)
        i += 1

    if buffer:
        tokens.append(("field", "".join(buffer)))

    return tokens


def extract_path_values(payload: Any, path: str) -> list[tuple[Any, str]]:
    tokens = parse_json_path(path)
    if not tokens:
        return []

    values: list[tuple[Any, str]] = [(payload, "")]

    for token_type, token_value in tokens:
        next_values: list[tuple[Any, str]] = []
        for current_value, current_path in values:
            if token_type == "field":
                if isinstance(current_value, dict) and isinstance(token_value, str) and token_value in current_value:
                    next_value = current_value[token_value]
                    next_path = f"{current_path}.{token_value}" if current_path else token_value
                    next_values.append((next_value, next_path))
                continue

            if token_type == "index":
                if (
                    isinstance(current_value, list)
                    and isinstance(token_value, int)
                    and token_value < len(current_value)
                ):
                    next_value = current_value[token_value]
                    next_path = f"{current_path}[{token_value}]"
                    next_values.append((next_value, next_path))
                continue

            if token_type == "wildcard" and isinstance(current_value, list):
                for i, next_value in enumerate(current_value):
                    next_path = f"{current_path}[{i}]"
                    next_values.append((next_value, next_path))

        values = next_values
        if not values:
            break

    return values


def get_wildcard_prefix(path: str) -> str | None:
    wildcard_marker = "[*]"
    marker_index = path.find(wildcard_marker)
    if marker_index == -1:
        return None
    return path[: marker_index + len(wildcard_marker)]


def split_wildcard_path(path: str) -> tuple[str, str]:
    wildcard_marker = "[*]"
    marker_index = path.find(wildcard_marker)
    if marker_index == -1:
        return path, ""
    prefix = path[:marker_index]
    suffix = path[marker_index + len(wildcard_marker) :]
    return prefix, suffix


def format_log_fields(payload: Any, fields: list[str]) -> str:
    msg = ""
    index = 0
    while index < len(fields):
        path = fields[index]
        wildcard_prefix = get_wildcard_prefix(path)

        if not wildcard_prefix:
            for value, resolved_path in extract_path_values(payload, path):
                msg += format_log_entry(resolved_path, str(value))
            index += 1
            continue

        grouped_paths = [path]
        next_index = index + 1
        while next_index < len(fields):
            next_path = fields[next_index]
            if get_wildcard_prefix(next_path) != wildcard_prefix:
                break
            grouped_paths.append(next_path)
            next_index += 1

        groups: dict[str, list[tuple[str, Any]]] = {}
        group_order: list[str] = []

        for grouped_path in grouped_paths:
            _, wildcard_suffix = split_wildcard_path(grouped_path)
            for value, resolved_path in extract_path_values(payload, grouped_path):
                group_key = resolved_path
                if wildcard_suffix and resolved_path.endswith(wildcard_suffix):
                    group_key = resolved_path[: -len(wildcard_suffix)]

                if group_key not in groups:
                    groups[group_key] = []
                    group_order.append(group_key)

                groups[group_key].append((resolved_path, value))

        for group_key in group_order:
            for resolved_path, value in groups[group_key]:
                msg += format_log_entry(resolved_path, str(value))

        index = next_index

    return msg


def allow_null_success_handler(
    handler: Callable[[requests.Response], None],
) -> Callable[[requests.Response], None]:
    def wrapper(response: requests.Response) -> None:
        if response.text == "null":
            return default_success_handler(response)
        return handler(response)

    return wrapper


def format_response_text(text: str) -> str:
    if not text:
        return text
    try:
        return json.dumps(json.loads(text), ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        return text


def error(text: str, allow_error: bool = False) -> None:
    msg = fore_error(text)
    msg += "\n"
    logger.info(msg)
    if not allow_error:
        raise ProcedureExit(EX_DATAERR, text)


def default_error_handler(response: requests.Response) -> None:
    msg = "Response text:\n"
    logger.info(msg)
    error(format_response_text(response.text))


def allow_error_handler(response: requests.Response) -> None:
    msg = "Response text:\n"
    logger.info(msg)
    error(format_response_text(response.text), allow_error=True)


def default_success_handler(_response: requests.Response) -> None:
    pass


def response_handler(
    response: requests.Response,
    success_handler: Callable[[requests.Response], None] = default_success_handler,
    error_handler: Callable[[requests.Response], None] = default_error_handler,
) -> None:
    if 200 <= response.status_code < 300:
        success_handler(response)
    else:
        error_handler(response)


def client_init_response_handler(
    response: requests.Response,
    client_timedelta: timedelta,
) -> None:
    response_handler(response)
    timedelta_string = client_timedelta_string(client_timedelta)
    logger.info(f"Client time delta with server: {timedelta_string}\n")


def tender_create_success_handler(response: requests.Response) -> None:
    msg = "Tender created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
            "access.transfer",
            "data.status",
            "data.tenderID",
            "data.procurementMethodType",
        ],
    )

    logger.info(msg)


def framework_create_success_handler(response: requests.Response) -> None:
    msg = "Framework created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
            "access.transfer",
            "data.status",
        ],
    )

    logger.info(msg)


def framework_patch_success_handler(response: requests.Response) -> None:
    msg = "Framework patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def submission_create_success_handler(response: requests.Response) -> None:
    msg = "Submission created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
            "data.status",
        ],
    )

    logger.info(msg)


def framework_get_success_handler(response: requests.Response) -> None:
    msg = "Framework found:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
            "data.agreementID",
        ],
    )

    logger.info(msg)


def plan_create_success_handler(response: requests.Response) -> None:
    """Handle successful plan creation response."""
    msg = "Plan created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
            "access.transfer",
            "data.status",
        ],
    )

    logger.info(msg)


def plan_patch_success_handler(response: requests.Response) -> None:
    msg = "Plan patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def contract_credentials_success_handler(response: requests.Response) -> None:
    msg = "Contract credentials retrieved:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
        ],
    )

    logger.info(msg)


def contract_post_success_handler(response: requests.Response) -> None:
    msg = "Contract created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def contract_access_success_handler(role: str, contract_id: str) -> Callable[[requests.Response], None]:
    def handler(response: requests.Response) -> None:
        msg = f"Contract access for {role} retrieved:\n"
        msg += format_log_entry("id", contract_id)
        msg += format_log_fields(
            response.json(),
            [
                "access.token",
                "data.identifier.id",
                "data.identifier.scheme",
                "data.identifier.legalName",
            ],
        )
        msg += format_log_entry("role", role)

        logger.info(msg)

    return handler


def bid_create_success_handler(response: requests.Response) -> None:
    data = response.json()["data"]

    msg = "Bid created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
            "data.status",
        ],
    )

    for bid_document_container in (
        "documents",
        "eligibilityDocuments",
        "financialDocuments",
        "qualificationDocuments",
    ):
        for document in data.get(bid_document_container, []):
            document_response: Any = type(
                "Response", (object,), {"json": lambda self, document=document: {"data": document}}
            )()
            document_attach_success_handler(document_response)

    logger.info(msg)


def item_create_success_handler(response: requests.Response) -> None:
    msg = "Item created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def item_get_success_handler(response: requests.Response) -> None:
    for i, _item in enumerate(response.json()["data"]):
        msg = "Item found:\n"
        msg += format_log_fields(
            response.json(),
            [
                f"data[{i}].id",
                f"data[{i}].status",
            ],
        )

        logger.info(msg)


def item_patch_success_handler(response: requests.Response) -> None:
    msg = "Item patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def signatory_post_success_handler(response: requests.Response) -> None:
    msg = "Signatory created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.role",
        ],
    )

    logger.info(msg)


def tender_patch_success_handler(response: requests.Response) -> None:
    msg = "Tender patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def tender_post_criteria_success_handler(response: requests.Response) -> None:
    msg = "Tender criteria created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data[*].classification.id",
        ],
    )

    logger.info(msg)


def tender_check_status_success_handler(response: requests.Response) -> None:
    msg = "Tender info:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def tender_check_status_invalid_handler(response: requests.Response) -> None:
    msg = "Tender info:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
            "data.unsuccessfulReason",
        ],
    )

    logger.info(msg)


def auction_participation_url_success_handler(response: requests.Response) -> None:
    msg = "Auction participation url for bid:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.participationUrl",
        ],
    )

    logger.info(msg)


def auction_multilot_participation_url_success_handler(response: requests.Response) -> None:
    msg = "Auction participation urls for bid:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.lotValues[*].relatedLot",
            "data.lotValues[*].status",
            "data.lotValues[*].participationUrl",
        ],
    )

    logger.info(msg)


def tender_post_plan_success_handler(response: requests.Response) -> None:
    msg = "Tender plans:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data[*].id",
        ],
    )

    logger.info(msg)


def tender_post_complaint_success_handler(response: requests.Response) -> None:
    msg = "Complaint created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logger.info(msg)


def complaints_get_success_handler(kind_type: str, complaints: list[dict[str, Any]]) -> None:
    """Log the listed complaints or claims of an object."""
    if not complaints:
        logger.info(f"No {kind_type}s found\n")
        return
    for complaint in complaints:
        msg = f"{kind_type.capitalize()} found:\n"
        msg += format_log_fields(
            {"data": complaint},
            [
                "data.id",
                "data.status",
                "data.resolutionType",
                "data.satisfied",
                "data.cancellationReason",
            ],
        )
        logger.info(msg)


def question_success_handler(response: requests.Response) -> None:
    msg = "Question:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.questionOf",
            "data.title",
            "data.answer",
        ],
    )
    logger.info(msg)


def complaint_post_success_handler(response: requests.Response) -> None:
    msg = "Complaint post created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.recipient",
            "data.relatedPost",
            "data.title",
        ],
    )
    logger.info(msg)


def document_attach_success_handler(response: requests.Response) -> None:
    msg = "Document attached:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.url",
            "data.documentType",
            "data.confidentiality",
        ],
    )

    logger.info(msg)
