import os

from procedure_tools.utils.file import get_numberless_filename

prefix_map = {
    "stage2_": "2000",
    "selection_": "2000",
}

number_map = {
    "plan_create": "0100",
    "plan_patch": "0110",
    "framework_create": "1000",
    "framework_patch_active": "1100",
    "submission_create": "1200",
    "submission_patch": "1210",
    "qualification_evaluation_report": "1300",
    "qualification_patch": "1310",
    "tender_create": "2000",
    "tender_credentials": "2000",
    "tender_document": "2010",
    "criteria_create": "2020",
    "tender_notice": "2030",
    "tender_patch": "2040",
    "bid_create": "2100",
    "bid_document": "2110",
    "bid_confidential_document": "2110",
    "bid_eligibility_document": "2110",
    "bid_financial_document": "2110",
    "bid_qualification_document": "2110",
    "bid_res_post": "2120",
    "bid_proposal": "2130",
    "bid_patch": "2140",
    "qualification_patch": "2200",
    "evaluation_report": "2210",
    "award_create": "2300",
    "award_patch": "2310",
    "contract_buyer_signer_info_patch": "2400",
    "contract_suppliers_signer_info_patch": "2410",
    "contract_patch": "2420",
    "agreement_contracts_patch": "3500",
    "agreement_document": "3510",
    "agreement_patch": "3520",
}


def reorder_files(root_dir):
    for subdir, _, filenames in os.walk(root_dir):
        for filename in filenames:
            for key in number_map:
                numberless_filename = get_numberless_filename(filename)

                addition = "0000"

                prefixless_filename = numberless_filename
                for prefix_key in prefix_map:
                    if numberless_filename.startswith(prefix_key):
                        prefixless_filename = numberless_filename[len(prefix_key) :]
                        addition = prefix_map[prefix_key]

                if prefixless_filename.startswith(key):
                    number = number_map[key]
                    number = str(int(number) + int(addition)).zfill(max(len(number), len(addition)))
                    new_filename = number + "_" + numberless_filename
                    if filename != new_filename:
                        old_path = os.path.join(subdir, filename)
                        new_path = os.path.join(subdir, new_filename)
                        os.rename(old_path, new_path)
                        print(f"Renamed: {old_path} to {new_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rename files in a directory")
    parser.add_argument("root_dir", help="Root directory containing the files")
    args = parser.parse_args()
    reorder_files(args.root_dir)
