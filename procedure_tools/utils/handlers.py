import json
from pprint import pprint

EX_OK = 0
EX_DATAERR = 65


def default_error_print_handler(response):
    try:
        pprint(json.loads(response.text))
        print("")
    except ValueError:
        print(response.text)
        print("")
    raise SystemExit(EX_DATAERR)
    

def default_success_print_handler(response):
    pass


def response_handler(response,
                     success_handler=default_success_print_handler,
                     error_handler=default_error_print_handler):
    print("[{}] {}\n".format(response.request.method, response.request.url))
    if response.status_code in [200, 201]:
        success_handler(response)
    else:
        error_handler(response)


def tender_create_success_print_handler(response):
    data = response.json()['data']
    access = response.json()['access']
    print("Tender created:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - token \t\t\t{}".format(access['token']))
    if 'transfer' in access:
        print(" - transfer \t\t\t{}".format(access['transfer']))
    print(" - status \t\t\t{}".format(data['status']))
    print(" - tenderID \t\t\t{}".format(data['tenderID']))
    print(" - procurementMethodType \t{}".format(data['procurementMethodType']))
    print("")


def contract_credentials_success_print_handler(response):
    data = response.json()['data']
    access = response.json()['access']
    print("Contract patched:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - token \t\t\t{}".format(access['token']))
    print("")


def bid_create_success_print_handler(response):
    data = response.json()['data']
    access = response.json()['access']
    print("Bid created:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - token \t\t\t{}".format(access['token']))
    print(" - status \t\t\t{}".format(data['status']))
    print("")


def item_create_success_print_handler(response):
    data = response.json()['data']
    print("Item created:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - status \t\t\t{}".format(data['status']))
    print("")


def item_get_success_print_handler(response):
    data = response.json()['data']
    for item in data:
        print("Item found:")
        print(" - id \t\t\t\t{}".format(item['id']))
        print(" - status \t\t\t{}".format(item['status']))
        print("")


def item_patch_success_print_handler(response):
    data = response.json()['data']
    print("Item patched:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - status \t\t\t{}".format(data['status']))
    print("")


def tender_patch_status_success_print_handler(response):
    data = response.json()['data']
    print("Tender status patched:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - status \t\t\t{}".format(data['status']))
    print("")


def tender_check_status_success_print_handler(response):
    data = response.json()['data']
    print("Tender info:")
    print(" - id \t\t\t\t{}".format(data['id']))
    print(" - status \t\t\t{}".format(data['status']))
    print("")
