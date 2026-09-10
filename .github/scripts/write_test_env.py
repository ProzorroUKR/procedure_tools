import os
import shutil
from pathlib import Path

EXAMPLE_FILE = Path(".env.test.example")
ENV_FILE = Path(".env.test")

SECRET_KEYS = (
    "API_HOST",
    "API_TOKEN",
    "API_PATH",
    "DS_HOST",
    "DS_USERNAME",
    "DS_PASSWORD",
    "REVIEWER_TOKEN",
    "BOT_TOKEN",
)


def _dotenv_value(value):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def main():
    if not EXAMPLE_FILE.is_file():
        raise SystemExit(f"Missing {EXAMPLE_FILE}")
    shutil.copyfile(EXAMPLE_FILE, ENV_FILE)
    extras = []
    for key in SECRET_KEYS:
        value = os.environ.get(key)
        if value:
            extras.append(f"{key}={_dotenv_value(value)}\n")
    if extras:
        with ENV_FILE.open("a", encoding="utf-8") as env_file:
            env_file.write("\n")
            env_file.writelines(extras)


if __name__ == "__main__":
    main()
