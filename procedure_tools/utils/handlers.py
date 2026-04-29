import logging

from procedure_tools.utils.date import client_timedelta_string
from procedure_tools.utils.style import fore_error, fore_info, fore_status_code

PAD = 20

EX_OK = 0
EX_DATAERR = 65


def format_log_entry(label: str, value: str) -> str:
    """Helper function to format consistent log entries."""
    return f" - {label:<{PAD}} {fore_info(value)}\n"


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
    """Handle successful tender creation response."""
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Tender created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("token", access["token"])
    msg += format_log_entry("transfer", access["transfer"]) if "transfer" in access else ""
    msg += format_log_entry("status", data["status"])
    msg += format_log_entry("tenderID", data["tenderID"])
    msg += format_log_entry("procurementMethodType", data["procurementMethodType"])

    logging.info(msg)


def framework_create_success_handler(response):
    """Handle successful framework creation response."""
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Framework created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("token", access["token"])
    msg += format_log_entry("transfer", access["transfer"]) if "transfer" in access else ""
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def framework_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Framework patched:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def submission_create_success_handler(response):
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Submission created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("token", access["token"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def framework_get_success_handler(response):
    data = response.json()["data"]

    has_agreement_id = "agreementID" in data

    msg = "Framework found:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])
    msg += format_log_entry("agreementID", data["agreementID"]) if has_agreement_id else ""

    logging.info(msg)


def agreement_get_success_handler(response):
    data = response.json()["data"]

    msg = "Agreement found:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def plan_create_success_handler(response):
    """Handle successful plan creation response."""
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Plan created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("token", access["token"])
    msg += format_log_entry("transfer", access["transfer"]) if "transfer" in access else ""
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def plan_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Plan patched:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def contract_credentials_success_handler(response):
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Contract credentials retrieved:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("token", access["token"])

    logging.info(msg)


def contract_access_success_handler(role: str, contract_id: str):
    def handler(response):
        data = response.json()["data"]
        access = response.json()["access"]

        msg = f"Contract access for {role} retrieved:\n"
        msg += format_log_entry("id", contract_id)
        msg += format_log_entry("token", access["token"])
        msg += format_log_entry("role", role)
        msg += format_log_entry("identifier.id", data["identifier"]["id"])
        msg += format_log_entry("identifier.scheme", data["identifier"]["scheme"])

        legal_name = data["identifier"].get("legalName")
        if legal_name:
            msg += format_log_entry("identifier.legalName", legal_name)

        logging.info(msg)

    return handler


def bid_create_success_handler(response):
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Bid created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("token", access["token"])
    msg += format_log_entry("status", data["status"])

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
    data = response.json()["data"]

    msg = "Item created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def item_get_success_handler(response):
    data = response.json()["data"]
    for item in data:
        msg = "Item found:\n"
        msg += format_log_entry("id", data["id"])
        msg += format_log_entry("status", item["status"])

        logging.info(msg)


def item_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Item patched:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def tender_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Tender patched:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def tender_post_criteria_success_handler(response):
    data = response.json()["data"]

    msg = "Tender criteria created:\n"
    for item in data:
        msg += format_log_entry("classification.id", item["classification"]["id"])

    logging.info(msg)


def tender_check_status_success_handler(response):
    data = response.json()["data"]

    msg = "Tender info:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def tender_check_status_invalid_handler(response):
    data = response.json()["data"]

    has_reason = "unsuccessfulReason" in data

    msg = "Tender info:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])
    msg += format_log_entry("unsuccessfulReason", " ".join(data["unsuccessfulReason"])) if has_reason else ""

    logging.info(msg)


def auction_participation_url_success_handler(response):
    data = response.json()["data"]

    has_url = "participationUrl" in data

    msg = "Auction participation url for bid:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("url", data["participationUrl"]) if has_url else ""

    logging.info(msg)


def auction_multilot_participation_url_success_handler(response, related_lot=None):
    data = response.json()["data"]

    msg = "Auction participation url for bid:\n"
    msg += format_log_entry("id", data["id"])

    for lot_value in response.json()["data"]["lotValues"]:
        if related_lot and lot_value["relatedLot"] != related_lot:
            continue

        is_active = lot_value.get("status", "active") == "active"
        has_url = "participationUrl" in lot_value
        has_status = "status" in lot_value

        msg += "Lot value:\n"
        msg += format_log_entry("relatedLot", lot_value["relatedLot"])
        msg += format_log_entry("status", lot_value["status"]) if has_status else ""
        msg += format_log_entry("url", lot_value["participationUrl"]) if is_active and has_url else ""

    logging.info(msg)


def tender_post_plan_success_handler(response):
    data = response.json()["data"]

    msg = "Tender plans:\n"
    for plan in data:
        msg += format_log_entry("id", plan["id"])

    logging.info(msg)


def tender_post_complaint_success_handler(response):
    data = response.json()["data"]

    msg = "Complaint created:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("status", data["status"])

    logging.info(msg)


def document_attach_success_handler(response):
    """Handle successful document attachment response."""
    data = response.json()["data"]

    msg = "Document attached:\n"
    msg += format_log_entry("id", data["id"])
    msg += format_log_entry("url", data["url"]) if "url" in data else ""
    msg += format_log_entry("documentType", data["documentType"]) if "documentType" in data else ""
    msg += format_log_entry("confidentiality", data["confidentiality"]) if "confidentiality" in data else ""

    logging.info(msg)
