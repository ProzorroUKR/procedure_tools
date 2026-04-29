import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from procedure_tools.test import WORKFLOW_TEST_CASES  # pyright: ignore[reportMissingImports]


def main() -> None:
    cases = WORKFLOW_TEST_CASES
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(f"cases={json.dumps(cases)}\n")
    else:
        print(json.dumps(cases))


if __name__ == "__main__":
    main()
