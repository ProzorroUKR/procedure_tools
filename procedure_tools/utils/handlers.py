import logging

from procedure_tools.utils.date import client_timedelta_string
from procedure_tools.utils.style import fore_error, fore_info, fore_status_code

PAD = 20

EX_OK = 0
EX_DATAERR = 65


def format_log_entry(label: str, value: str) -> str:
    return f" - {label:<{PAD}} {fore_info(value)}\n"


def parse_json_path(path: str):
    tokens = []
    buffer = []
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


def extract_path_values(payload, path: str):
    tokens = parse_json_path(path)
    if not tokens:
        return []

    values = [(payload, "")]

    for token_type, token_value in tokens:
        next_values = []
        for current_value, current_path in values:
            if token_type == "field":
                if isinstance(current_value, dict) and token_value in current_value:
                    next_value = current_value[token_value]
                    next_path = f"{current_path}.{token_value}" if current_path else token_value
                    next_values.append((next_value, next_path))
                continue

            if token_type == "index":
                if isinstance(current_value, list) and token_value < len(current_value):
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


def get_wildcard_prefix(path: str):
    wildcard_marker = "[*]"
    marker_index = path.find(wildcard_marker)
    if marker_index == -1:
        return None
    return path[: marker_index + len(wildcard_marker)]


def split_wildcard_path(path: str):
    wildcard_marker = "[*]"
    marker_index = path.find(wildcard_marker)
    if marker_index == -1:
        return path, ""
    prefix = path[:marker_index]
    suffix = path[marker_index + len(wildcard_marker) :]
    return prefix, suffix


def format_log_fields(payload: dict, fields: list[str]) -> str:
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

        groups = {}
        group_order = []

        for grouped_path in grouped_paths:
            wildcard_root, wildcard_suffix = split_wildcard_path(grouped_path)
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


def allow_null_success_handler(handler):
    def wrapper(response):
        if response.text == "null":
            return default_success_handler(response)
        handler(response)

    return wrapper


def error(text, allow_error=False):
    msg = fore_error(text)
    msg += "\n"
    logging.info(msg)
    if not allow_error:
        raise SystemExit(EX_DATAERR)


def default_error_handler(response):
    msg = "Response text:\n"
    logging.info(msg)
    error(response.text)


def allow_error_handler(response):
    msg = "Response text:\n"
    logging.info(msg)
    error(response.text, allow_error=True)


def default_success_handler(response):
    pass


def response_handler(
    response,
    success_handler=default_success_handler,
    error_handler=default_error_handler,
):
    msg = "Response status code: "
    msg += fore_status_code(response.status_code)
    msg += "\n"
    logging.info(msg)
    if 200 <= response.status_code < 300:
        success_handler(response)
    else:
        error_handler(response)


def client_init_response_handler(
    response,
    client_timedelta,
):
    response_handler(response)
    timedelta_string = client_timedelta_string(client_timedelta)
    logging.info(f"Client time delta with server: {timedelta_string}\n")


def tender_create_success_handler(response):
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

    logging.info(msg)


def framework_create_success_handler(response):
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

    logging.info(msg)


def framework_patch_success_handler(response):
    msg = "Framework patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def submission_create_success_handler(response):
    msg = "Submission created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
            "data.status",
        ],
    )

    logging.info(msg)


def framework_get_success_handler(response):
    msg = "Framework found:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
            "data.agreementID",
        ],
    )

    logging.info(msg)


def agreement_get_success_handler(response):
    msg = "Agreement found:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def plan_create_success_handler(response):
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

    logging.info(msg)


def plan_patch_success_handler(response):
    msg = "Plan patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def contract_credentials_success_handler(response):
    msg = "Contract credentials retrieved:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "access.token",
        ],
    )

    logging.info(msg)


def contract_access_success_handler(role: str, contract_id: str):
    def handler(response):
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

        logging.info(msg)

    return handler


def bid_create_success_handler(response):
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
            response = type("Response", (object,), {"json": lambda self: {"data": document}})()
            document_attach_success_handler(response)

    logging.info(msg)


def item_create_success_handler(response):
    msg = "Item created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def item_get_success_handler(response):
    for i, _item in enumerate(response.json()["data"]):
        msg = "Item found:\n"
        msg += format_log_fields(
            response.json(),
            [
                f"data[{i}].id",
                f"data[{i}].status",
            ],
        )

        logging.info(msg)


def item_patch_success_handler(response):
    msg = "Item patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def tender_patch_success_handler(response):
    msg = "Tender patched:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def tender_post_criteria_success_handler(response):
    msg = "Tender criteria created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data[*].classification.id",
        ],
    )

    logging.info(msg)


def tender_check_status_success_handler(response):
    msg = "Tender info:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def tender_check_status_invalid_handler(response):
    msg = "Tender info:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
            "data.unsuccessfulReason",
        ],
    )

    logging.info(msg)


def auction_participation_url_success_handler(response):
    msg = "Auction participation url for bid:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.participationUrl",
        ],
    )

    logging.info(msg)


def auction_multilot_participation_url_success_handler(response):
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

    logging.info(msg)


def tender_post_plan_success_handler(response):
    msg = "Tender plans:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data[*].id",
        ],
    )

    logging.info(msg)


def tender_post_complaint_success_handler(response):
    msg = "Complaint created:\n"
    msg += format_log_fields(
        response.json(),
        [
            "data.id",
            "data.status",
        ],
    )

    logging.info(msg)


def document_attach_success_handler(response):
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

    logging.info(msg)
