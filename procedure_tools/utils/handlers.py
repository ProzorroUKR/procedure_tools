import logging

from procedure_tools.utils.date import client_timedelta_string
from procedure_tools.utils.style import fore_error, fore_info, fore_status_code

EX_OK = 0
EX_DATAERR = 65


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
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Tender created:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - token \t\t\t{}\n".format(fore_info(access["token"]))
    if "transfer" in access:
        msg += " - transfer \t\t\t{}\n".format(fore_info(access["transfer"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))
    msg += " - tenderID \t\t\t{}\n".format(fore_info(data["tenderID"]))
    msg += " - procurementMethodType \t{}\n".format(
        fore_info(data["procurementMethodType"])
    )

    logging.info(msg)


def plan_create_success_handler(response):
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Plan created:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - token \t\t\t{}\n".format(fore_info(access["token"]))
    if "transfer" in access:
        msg += " - transfer \t\t\t{}\n".format(fore_info(access["transfer"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    logging.info(msg)


def plan_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Plan patched:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    logging.info(msg)


def contract_credentials_success_handler(response):
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Contract patched:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - token \t\t\t{}\n".format(fore_info(access["token"]))

    logging.info(msg)


def bid_create_success_handler(response):
    data = response.json()["data"]
    access = response.json()["access"]

    msg = "Bid created:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - token \t\t\t{}\n".format(fore_info(access["token"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    for bid_document_container in (
        "documents",
        "eligibilityDocuments",
        "financialDocuments",
        "qualificationDocuments",
    ):
        for document in data.get(bid_document_container, []):
            response = type(
                "Response", (object,), {"json": lambda self: {"data": document}}
            )()
            document_attach_success_handler(response)

    logging.info(msg)


def item_create_success_handler(response):
    data = response.json()["data"]

    msg = "Item created:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    logging.info(msg)


def item_get_success_handler(response):
    data = response.json()["data"]
    for item in data:
        msg = "Item found:\n"
        msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
        msg += " - status \t\t\t{}\n".format(fore_info(item["status"]))

        logging.info(msg)


def item_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Item patched:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    logging.info(msg)


def tender_patch_success_handler(response):
    data = response.json()["data"]

    msg = "Tender patched:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    logging.info(msg)


def tender_post_criteria_success_handler(response):
    data = response.json()["data"]

    msg = "Tender criteria created:\n"
    for item in data:
        msg += " - classification.id \t\t{}\n".format(
            fore_info(item["classification"]["id"])
        )

    logging.info(msg)


def tender_check_status_success_handler(response):
    data = response.json()["data"]

    msg = "Tender info:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))

    logging.info(msg)


def tender_check_status_invalid_handler(response):
    data = response.json()["data"]

    msg = "Tender info:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(data["status"]))
    if "unsuccessfulReason" in data:
        msg += " - unsuccessfulReason \t\t{}\n".format(
            fore_info(" ".join(data["unsuccessfulReason"]))
        )

    logging.info(msg)


def auction_participation_url_success_handler(response):
    data = response.json()["data"]

    msg = "Auction participation url for bid:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    if "participationUrl" in data:
        msg += " - url \t\t\t\t{}\n".format(fore_info(data["participationUrl"]))

    logging.info(msg)


def auction_multilot_participation_url_success_handler(response, related_lot=None):
    data = response.json()["data"]

    msg = "Auction participation url for bid:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    for lot_value in response.json()["data"]["lotValues"]:
        if related_lot and lot_value["relatedLot"] != related_lot:
            continue
        msg += "Lot value:\n"
        msg += " - relatedLot\t\t\t{}\n".format(fore_info(lot_value["relatedLot"]))
        if "status" in lot_value:
            msg += " - status \t\t\t{}\n".format(fore_info(lot_value["status"]))
        if "participationUrl" in lot_value:
            if lot_value.get("status", "active") == "active":
                msg += " - url \t\t\t\t{}\n".format(
                    fore_info(lot_value["participationUrl"])
                )

    logging.info(msg)


def tender_post_plan_success_handler(response):
    data = response.json()["data"]

    msg = "Tender plans:\n"
    for plan in response.json()["data"]:
        msg += " - id \t\t\t\t{}\n".format(fore_info(plan["id"]))

    logging.info(msg)


def tender_post_complaint_success_handler(response):
    data = response.json()["data"]

    msg = "Complaint created:\n"
    complaint = response.json()["data"]
    msg += " - id \t\t\t\t{}\n".format(fore_info(complaint["id"]))
    msg += " - status \t\t\t{}\n".format(fore_info(complaint["status"]))

    logging.info(msg)


def document_attach_success_handler(response):
    data = response.json()["data"]

    msg = "Document attached:\n"
    msg += " - id \t\t\t\t{}\n".format(fore_info(data["id"]))
    if "url" in data:
        msg += " - url \t\t\t\t{}\n".format(fore_info(data["url"]))
    if "documentType" in data:
        msg += " - documentType \t\t{}\n".format(fore_info(data["documentType"]))
    if "confidentiality" in data:
        msg += " - confidentiality \t\t{}\n".format(fore_info(data["confidentiality"]))

    logging.info(msg)
