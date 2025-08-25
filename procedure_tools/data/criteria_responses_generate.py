import argparse
import json
import os
from pathlib import Path

from procedure_tools.data.field_sort import dump_kwargs

dump_kwargs = {
    "sort_keys": True,
    "indent": 2,
    "ensure_ascii": False,
}


def generate_responses_from_criteria(criteria_data):
    """Generate complete responses for all criteria in the data."""
    responses = []

    for criterion in criteria_data["data"]:
        # Skip criteria with source "procuringEntity" as they don't need responses
        if criterion.get("source") == "procuringEntity":
            continue

        criterion_id = criterion.get("classification", {}).get("id")
        criterion_source = criterion.get("source")
        print(f"Generating responses for criterion: {criterion_id}")

        # For each criterion, we'll answer the first requirement group completely
        if requirementGroups := criterion.get("requirementGroups", []):
            for group_index, group in enumerate(requirementGroups):
                # Generate responses for all requirements in this group
                for requirement in group.get("requirements", []):
                    req_id = requirement.get("id")
                    response = {"requirement": {"id": req_id}}

                    # Generate appropriate value based on requirement type
                    if "expectedValues" in requirement and requirement["expectedValues"]:
                        # Use 'values' (plural) for expectedValues requirements
                        response["values"] = [requirement["expectedValues"][0]]
                    elif "expectedValue" in requirement:
                        response["value"] = requirement["expectedValue"]
                    elif "maxValue" in requirement:
                        response["value"] = requirement["maxValue"]
                    elif "minValue" in requirement:
                        response["value"] = requirement["minValue"]
                    elif requirement.get("dataType") == "boolean":
                        response["value"] = True
                    elif requirement.get("dataType") == "string":
                        response["value"] = "Sample response"
                    elif requirement.get("dataType") == "number":
                        response["value"] = 0
                    elif requirement.get("dataType") == "integer":
                        response["value"] = 0
                    else:
                        print(f"  Warning: Could not determine appropriate value for requirement {req_id}")
                        continue

                    # Add evidences if eligibleEvidences is present in the requirement
                    # and the criterion source is NOT "winner"
                    if (
                        "eligibleEvidences" in requirement
                        and requirement["eligibleEvidences"]
                        and criterion_source != "winner"
                    ):
                        evidences = []
                        for eligible_evidence in requirement["eligibleEvidences"]:
                            evidence = {
                                "relatedDocument": {"title": "name.doc"},
                                "title": eligible_evidence.get("title", "Документ"),
                                "type": eligible_evidence.get("type", "document"),
                            }
                            evidences.append(evidence)

                        if evidences:
                            response["evidences"] = evidences
                            print(f"  Added {len(evidences)} evidences for requirement: {req_id}")

                    responses.append(response)
                    print(f"  Generated response for requirement: {req_id}")

                # Only answer the first requirement group for each criterion
                # as typically only one group should be answered
                break
        else:
            print(f"  Warning: No requirement groups found for criterion {criterion_id}")

    return {"data": responses}


def process_directory(directory, force=False):
    """Process all criteria and response files in the directory."""
    prefixes = ["", "stage2_", "selection_"]

    for prefix in prefixes:
        for root, _, files in os.walk(directory):
            # Find criteria files first
            criteria_files = []
            for file in files:
                file_clean = "_".join(file.split("_")[1:])
                if file_clean.startswith(f"{prefix}criteria_create") and file_clean.endswith(".json"):
                    criteria_files.append(file)

            # Process each criteria file
            for criteria_file in criteria_files:
                criteria_path = Path(root) / criteria_file
                print(f"\nProcessing criteria: {criteria_path}")

                # Load criteria data
                with open(criteria_path, "r", encoding="utf-8") as f:
                    criteria_data = json.load(f)

                # Find corresponding response files
                for res_file in os.listdir(root):
                    res_file_clean = "_".join(res_file.split("_")[1:])
                    if res_file_clean.startswith(f"{prefix}bid_res_post") and res_file_clean.endswith(".json"):
                        response_path = Path(root) / res_file
                        print(f"\nProcessing responses: {response_path}")

                        # Check if we should overwrite existing responses
                        if not force:
                            with open(response_path, "r", encoding="utf-8") as f:
                                existing_responses = json.load(f)
                                if existing_responses.get("data") and len(existing_responses["data"]) > 0:
                                    print("  Skipping: Response file already has data (use --force to overwrite)")
                                    continue

                        # Generate new responses
                        new_responses = generate_responses_from_criteria(criteria_data)

                        # Save the new responses
                        with open(response_path, "w", encoding="utf-8") as f:
                            json.dump(new_responses, f, **dump_kwargs)
                        print(f"  Generated {len(new_responses['data'])} responses and saved to {response_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate bid responses from criteria")
    parser.add_argument("root_dir", help="Root directory containing the files")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing responses")
    args = parser.parse_args()

    process_directory(args.root_dir, force=args.force)
