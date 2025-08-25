import argparse
import difflib
import json
import os
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import standards

from procedure_tools.data.field_sort import dump_kwargs

moved_responses = [
    ### Example:
    # {
    #     "criteria_id": "CRITERION.OTHER.CONTRACT.GUARANTEE",
    #     "group_index_source": 0,
    #     "response_index_source": 0,
    #     "group_index_destination": 1,
    #     "response_index_destination": 0,
    # },
]


def update_criteria_from_standard(data, source_data):
    original_data = deepcopy(data["data"])
    updated_data = data["data"]

    for criteria_index, criteria in enumerate(updated_data):
        original_criteria = original_data[criteria_index]

        # Find matching standard criterion
        matching_criterion = None
        for standards_criterion in source_data:
            if standards_criterion.get("classification", {}).get("id") == criteria.get("classification", {}).get("id"):
                matching_criterion = deepcopy(standards_criterion)  # Make a copy to not modify the original
                break

        if matching_criterion:
            # Update criteria with standard data
            criteria.clear()
            criteria.update(deepcopy(matching_criterion))

            # Restore original fields
            if relates_to := original_criteria.get("relatesTo"):
                criteria["relatesTo"] = relates_to
            if related_item := original_criteria.get("relatedItem"):
                criteria["relatedItem"] = related_item

            # Restore some original fields
            for group_index, group in enumerate(criteria.get("requirementGroups", [])):
                for req_index, req in enumerate(group.get("requirements", [])):
                    # Generate new ID for requirement
                    req["id"] = str(uuid4().hex)

                    # Not implemented
                    req.pop("weight", None)

                    original_groups = original_criteria.get("requirementGroups", [])

                    # Check whether current response is source or destination
                    source_requirement = None
                    destination_requirement = None
                    for move in moved_responses:
                        if (
                            move["criteria_id"] == criteria.get("classification", {}).get("id")
                            and move["group_index_destination"] == group_index
                            and move["response_index_destination"] == req_index
                        ):
                            destination_requirement = move
                            break
                        elif (
                            move["criteria_id"] == criteria.get("classification", {}).get("id")
                            and move["group_index_source"] == group_index
                            and move["response_index_source"] == req_index
                        ):
                            source_requirement = move
                            break

                    if destination_requirement:
                        # If current response is destination, get original requirement
                        original_group = original_groups[destination_requirement["group_index_source"]]
                        original_requirements = original_group.get("requirements", [])
                        if destination_requirement["response_index_source"] >= len(original_requirements):
                            continue
                        original_req = original_requirements[destination_requirement["response_index_source"]]
                    elif source_requirement:
                        # If current response is source, skip
                        continue
                    else:
                        # If current response is neither source nor destination,
                        # get original requirement based on indices
                        if group_index >= len(original_groups):
                            continue
                        original_group = original_groups[group_index]
                        original_requirements = original_group.get("requirements", [])
                        if req_index >= len(original_requirements):
                            continue
                        original_req = original_requirements[req_index]

                    # Restore original IDs in same order
                    if "id" in original_req:
                        req["id"] = original_req["id"]

                    # Restore original title if it's empty
                    # (fields that supposed to be filled by user)
                    if req["title"] == "":
                        req["title"] = original_req["title"]

                    # Fill eligibleEvidences
                    if "eligibleEvidences" in req:
                        for evidence in req["eligibleEvidences"]:
                            if evidence["title"] == "":
                                evidence["title"] = "Інформаційна довідка або витяг з реєстру"


def update_criteria(original_data):
    original_data, updated_data = deepcopy(original_data), original_data

    # List of all criteria source files
    source_files = [
        "criteria/LCC.json",
        "criteria/article_16.json",
        "criteria/article_17.json",
        "criteria/investors_strategy.json",
        "criteria/local_origin_level.json",
        "criteria/other.json",
        "criteria/period.json",
        "criteria/resident.json",
    ]

    # Process each source file
    for source_file in source_files:
        try:
            source_data = standards.load(source_file)
            update_criteria_from_standard(updated_data, source_data)
        except Exception as e:
            print(f"\nError processing {source_file}: {e.__class__.__name__}: {str(e)}")
            raise e

    # show_diff(original_data, updated_data)


def show_diff(original_data, updated_data):
    updated_ids = []
    for original_criterion, updated_criterion in zip(original_data["data"], updated_data["data"]):
        # Dump original and updated data to strings
        original_data_str = json.dumps(original_criterion, **dump_kwargs)
        updated_data_str = json.dumps(updated_criterion, **dump_kwargs)
        if original_data_str != updated_data_str:
            diff = difflib.Differ().compare(
                original_data_str.splitlines(),
                updated_data_str.splitlines(),
            )
            print("=" * 100)
            print("\n".join(diff))
            updated_ids.append(updated_criterion["classification"]["id"])

    print("=" * 100)
    if len(updated_ids):
        print(f"Updated {len(updated_ids)} criteria:")
        for id in updated_ids:
            print(id)


def process_directory(directory, readonly=False):
    prefixes = ["", "stage2_", "selection_"]
    for prefix in prefixes:
        for root, _, files in os.walk(directory):
            # Process each criteria_create file separately
            for file in files:
                file_clean = "_".join(file.split("_")[1:])
                if file_clean.startswith(f"{prefix}criteria_create") and file_clean.endswith(".json"):
                    criteria_path = Path(root) / file
                    print(f"\nProcessing criteria: {criteria_path}")

                    # Process criteria file
                    with open(criteria_path, "r", encoding="utf-8") as f:
                        criteria_data = json.load(f)
                        update_criteria(criteria_data)
                        if not readonly:
                            with open(criteria_path, "w", encoding="utf-8") as f:
                                json.dump(criteria_data, f, **dump_kwargs)
                        else:
                            print("Readonly mode: Not saving changes to criteria file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update criteria and responses")
    parser.add_argument("root_dir", help="Root directory containing the files")
    parser.add_argument("--readonly", action="store_true", help="Don't modify any files, just show what would change")
    args = parser.parse_args()

    process_directory(args.root_dir, readonly=args.readonly)
