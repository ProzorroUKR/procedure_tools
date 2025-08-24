import json
import os
import uuid
from pathlib import Path

from procedure_tools.data.field_sort import dump_kwargs


def add_criteria(data, criteria_file):
    # Load criteria from file instead of standards
    with open(criteria_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    # Track existing classification IDs
    existing_ids = {item.get("classification", {}).get("id") for item in data["data"]}

    # Track newly added requirement IDs
    added_requirement_ids = []

    # Add each criterion if not exists
    for new_criteria in new_data["data"]:
        classification_id = new_criteria.get("classification", {}).get("id")
        if classification_id and classification_id not in existing_ids:
            criteria_copy = new_criteria.copy()

            print(f"Added criterion: {classification_id}")

            # Add relatesTo tenderer
            if "relatesTo" not in criteria_copy:
                criteria_copy["relatesTo"] = "tenderer"

            # Add lorem ipsum to requirement titles and generate IDs if missing
            for group in criteria_copy.get("requirementGroups", []):
                for req in group.get("requirements", []):
                    if "title" not in req:
                        req["title"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
                    if "id" not in req:
                        req["id"] = str(uuid.uuid4().hex)
                    added_requirement_ids.append(req["id"])
                    print(f"Added requirement from new criteria: {req['id']}")

            data["data"].append(criteria_copy)

            print(f"Added criterion: {classification_id}")

            existing_ids.add(classification_id)

    return data, added_requirement_ids


def process_directory(directory, criteria_file):
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
                    added_requirement_ids = []
                    with open(criteria_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if "data" in data:
                            data, new_ids = add_criteria(data, criteria_file)
                            added_requirement_ids.extend(new_ids)
                            with open(criteria_path, "w", encoding="utf-8") as f:
                                json.dump(data, f, **dump_kwargs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add criteria and responses to JSON files")
    parser.add_argument("root_dir", help="Root directory containing the files")
    parser.add_argument("criteria_file", help="JSON file containing criteria to add")
    args = parser.parse_args()
    root_directories = args.root_dir.split(",")
    criteria_file = args.criteria_file
    for root_directory in root_directories:
        process_directory(root_directory, criteria_file)
