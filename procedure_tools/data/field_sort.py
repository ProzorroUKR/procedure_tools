import json
import os

from procedure_tools.utils.file import get_project_dir

dump_kwargs = {
    "sort_keys": True,
    "indent": 2,
    "ensure_ascii": False,
}


def sort_data_json():
    for root, dirs, files in os.walk(os.path.join(get_project_dir(), "data")):
        for file in files:
            try:
                with open(os.path.join(root, file), "r") as f:
                    lines = json.loads(f.read())
                with open(os.path.join(root, file), "w", encoding="utf-8") as f:
                    f.write(json.dumps(lines, **dump_kwargs))
            except ValueError:
                pass


if __name__ == "__main__":
    sort_data_json()
