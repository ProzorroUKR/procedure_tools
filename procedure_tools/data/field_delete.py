import argparse
import fnmatch
import json
import os
import sys

from procedure_tools.data.field_sort import dump_kwargs
from procedure_tools.utils.file import get_project_dir


def delete_field_by_jsonpath(filename, jsonpath):
    """
    Remove field specified by jsonpath from JSON file

    Args:
        filename (str): Path to the JSON file
        jsonpath (str): JSONPath expression to identify the field to remove
    """
    try:
        # Read the JSON file
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Parse jsonpath and find the field to remove
        from jsonpath_ng import parse

        jsonpath_expr = parse(jsonpath)

        # Find all matches for the jsonpath
        matches = jsonpath_expr.find(data)

        if not matches:
            print(f"No fields found matching jsonpath: {jsonpath}")
            return False

        # Remove the fields
        for match in matches:
            # Get the parent object and the field name
            parent = match.context.value
            field_name = match.path.fields[-1] if hasattr(match.path, 'fields') else str(match.path)

            # Remove the field from the parent object
            if isinstance(parent, dict):
                if field_name in parent:
                    del parent[field_name]
                    print(f"Removed field '{field_name}' from {filename}")
                else:
                    print(f"Field '{field_name}' not found in {filename}")
            else:
                print(f"Cannot remove field from non-dict object: {type(parent)}")

        # Write the modified data back to the file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, **dump_kwargs))

        print(f"Successfully updated {filename}")
        return True

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filename}': {e}")
        return False
    except Exception as e:
        print(f"Error processing file '{filename}': {e}")
        return False


def find_and_process_files(filename_pattern, jsonpath, subdir=None):
    """
    Walk through the project data directory and find files matching the filename pattern,
    then process each matching file

    Args:
        filename_pattern (str): Filename or part of filename to search for
        jsonpath (str): JSONPath expression to identify the field to remove
        subdir (str, optional): Subdirectory within the data directory to search in
    """
    data_directory = os.path.join(get_project_dir(), "data")

    if subdir:
        data_directory = os.path.join(data_directory, subdir)

    if not os.path.exists(data_directory):
        print(f"Error: Directory not found: {data_directory}")
        return False

    success_count = 0
    total_count = 0

    for root, dirs, files in os.walk(data_directory):
        for file in files:
            # Check if filename matches the pattern
            if fnmatch.fnmatch(file, f"*{filename_pattern}*"):
                file_path = os.path.join(root, file)
                total_count += 1
                print(f"Found matching file: {file_path}")

                if delete_field_by_jsonpath(file_path, jsonpath):
                    success_count += 1

    if total_count == 0:
        print(f"No files found matching pattern: *{filename_pattern}* in {data_directory}")
        return False

    print(f"\nSummary: Found and processed {total_count} matching files, {success_count} successful updates")
    return success_count == total_count


def main():
    parser = argparse.ArgumentParser(
        description="Remove fields from JSON files in project data directory using JSONPath expressions"
    )
    parser.add_argument("filename_pattern", help="Filename or part of filename to search for in project data directory")
    parser.add_argument("jsonpath", help="JSONPath expression to identify the field to remove")
    parser.add_argument("--subdir", "-s", help="Subdirectory within the data directory to search in")

    args = parser.parse_args()

    if not args.filename_pattern or not args.jsonpath:
        parser.error("Both filename_pattern and jsonpath are required")

    # Search for files matching the pattern in the project data directory (or subdirectory)
    success = find_and_process_files(args.filename_pattern, args.jsonpath, args.subdir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
