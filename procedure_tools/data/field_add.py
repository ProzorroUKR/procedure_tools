import argparse
import fnmatch
import json
import os
import sys

from procedure_tools.data.field_sort import dump_kwargs
from procedure_tools.utils.file import get_project_dir


def add_field_by_jsonpath(filename, jsonpath, value):
    """
    Add field specified by jsonpath to JSON file

    Args:
        filename (str): Path to the JSON file
        jsonpath (str): JSONPath expression to identify where to add the field
        value: Value to add (can be any type: string, number, list, dict, etc.)
    """
    try:
        # Read the JSON file
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        from jsonpath_ng import parse

        # Split the path to get the parent path and field name
        parts = jsonpath.split('.')
        if len(parts) >= 2:
            # Reconstruct parent path (everything except the last part)
            parent_path = '.'.join(parts[:-1])
            field_name = parts[-1]
        else:
            print("Invalid jsonpath format")
            return False
        
        parent_expr = parse(parent_path)
        parent_matches = parent_expr.find(data)
        
        if not parent_matches:
            print(f"No locations found for parent path: {parent_path}")
            return False
        
        # Add field to each parent match
        for match in parent_matches:
            # For jsonpath like $.config.field, match.context.value is the root object
            # We need to access the actual config object
            if parent_path == '$':
                parent = match.context.value
            else:
                # Extract the actual parent object from the match
                parent = match.value
            
            if isinstance(parent, dict):
                if field_name in parent:
                    print(f"Field '{field_name}' already exists in {filename}, skipping...")
                    continue
                else:
                    parent[field_name] = value
                    print(f"Added field '{field_name}' with value {repr(value)} to {filename}")
            else:
                print(f"Cannot add field to non-dict object: {type(parent)}")

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


def find_and_process_files(filename_pattern, jsonpath, value, subdir=None):
    """
    Walk through the project data directory and find files matching the filename pattern,
    then process each matching file

    Args:
        filename_pattern (str): Filename or part of filename to search for
        jsonpath (str): JSONPath expression to identify where to add the field
        value: Value to add (can be any type: string, number, list, dict, etc.)
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

                if add_field_by_jsonpath(file_path, jsonpath, value):
                    success_count += 1

    if total_count == 0:
        print(f"No files found matching pattern: *{filename_pattern}* in {data_directory}")
        return False

    print(f"\nSummary: Found and processed {total_count} matching files, {success_count} successful updates")
    return success_count == total_count


def main():
    parser = argparse.ArgumentParser(
        description="Add fields to JSON files in project data directory using JSONPath expressions"
    )
    parser.add_argument("filename_pattern", help="Filename or part of filename to search for in project data directory")
    parser.add_argument("jsonpath", help="JSONPath expression to identify where to add the field")
    parser.add_argument("value", help="Value to add (can be any type: string, number, list, dict, etc.)")
    parser.add_argument("--subdir", "-s", help="Subdirectory within the data directory to search in")

    args = parser.parse_args()

    if not args.filename_pattern or not args.jsonpath or args.value is None:
        parser.error("filename_pattern, jsonpath, and value are required")

    try:
        parsed_value = json.loads(args.value)
    except (ValueError, json.JSONDecodeError):
        parsed_value = args.value

    # Search for files matching the pattern in the project data directory (or subdirectory)
    success = find_and_process_files(args.filename_pattern, args.jsonpath, parsed_value, args.subdir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
