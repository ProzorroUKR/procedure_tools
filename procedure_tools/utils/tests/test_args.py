import pytest

from procedure_tools.main import parse_args

REQUIRED = [
    "https://api.example",
    "api-token",
    "https://ds.example",
    "ds-user",
    "ds-pass",
]


def test_parse_args_positional_cli_still_works():
    args = parse_args(REQUIRED + ["--data", "aboveThreshold"], environ={}, search_dirs=["/nonexistent"])
    assert args.host == "https://api.example"
    assert args.token == "api-token"
    assert args.ds_host == "https://ds.example"
    assert args.ds_username == "ds-user"
    assert args.ds_password == "ds-pass"
    assert args.data == ["aboveThreshold"]
    assert args.env_file is None


def test_parse_args_loads_env_file_and_cli_overrides(tmp_path):
    env_file = tmp_path / ".env.sandbox"
    env_file.write_text(
        "\n".join(
            [
                "API_HOST=https://from-env",
                "API_TOKEN=env-token",
                "DS_HOST=https://ds-from-env",
                "DS_USERNAME=env-user",
                "DS_PASSWORD=env-pass",
                "API_PATH=/api/from-env/",
                "DATA=reporting,aboveThreshold",
                "ACCELERATION=123",
                "DEBUG=true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    args = parse_args(
        ["--env", "sandbox", "--token", "cli-token", "--data", "belowThreshold", "--path", "/api/cli/"],
        environ={},
        search_dirs=[str(tmp_path)],
    )
    assert args.env_file == str(env_file)
    assert args.host == "https://from-env"
    assert args.token == "cli-token"
    assert args.ds_host == "https://ds-from-env"
    assert args.ds_username == "env-user"
    assert args.ds_password == "env-pass"
    assert args.path == "/api/cli/"
    assert args.data == ["belowThreshold"]
    assert args.acceleration == 123
    assert args.debug is True


def test_parse_args_named_flags_override_positionals_and_env(tmp_path):
    (tmp_path / ".env").write_text(
        "\n".join(
            [
                "API_HOST=https://from-env",
                "API_TOKEN=env-token",
                "DS_HOST=https://ds-from-env",
                "DS_USERNAME=env-user",
                "DS_PASSWORD=env-pass",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    args = parse_args(
        ["https://from-positional", "--host", "https://from-flag"],
        environ={},
        search_dirs=[str(tmp_path)],
    )
    assert args.host == "https://from-flag"
    assert args.token == "env-token"


def test_parse_args_requires_connection_settings(tmp_path):
    with pytest.raises(SystemExit):
        parse_args([], environ={}, search_dirs=[str(tmp_path)])


def test_parse_args_cli_env_overrides_procedure_env(tmp_path):
    for name, host in (("dev", "https://dev.example"), ("sandbox", "https://sandbox.example")):
        (tmp_path / f".env.{name}").write_text(
            "\n".join(
                [
                    f"API_HOST={host}",
                    "API_TOKEN=token",
                    "DS_HOST=https://ds.example",
                    "DS_USERNAME=user",
                    "DS_PASSWORD=pass",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
    args = parse_args(
        ["--env", "sandbox"],
        environ={"PROCEDURE_ENV": "dev"},
        search_dirs=[str(tmp_path)],
    )
    assert args.host == "https://sandbox.example"
    assert args.env_file.endswith(".env.sandbox")


def test_parse_args_missing_env_file(tmp_path):
    with pytest.raises(SystemExit):
        parse_args(["--env", "missing"], environ={}, search_dirs=[str(tmp_path)])
