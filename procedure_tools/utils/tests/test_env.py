import pytest

from procedure_tools.utils.env import (
    EnvFileNotFound,
    EnvValueError,
    build_env_values,
    convert_env_value,
    list_available_envs,
    load_run_env,
    parse_env_content,
    resolve_env_path,
)


def test_parse_env_content_supports_export_quotes_and_comments():
    values = parse_env_content("""
        # comment
        export API_HOST=https://example.com
        API_TOKEN="secret value"
        EMPTY=
        INVALID
        DS_HOST='https://ds.example.com'
        """)
    assert values == {
        "API_HOST": "https://example.com",
        "API_TOKEN": "secret value",
        "EMPTY": "",
        "DS_HOST": "https://ds.example.com",
    }


def test_convert_env_value_types():
    assert convert_env_value("debug", "true") is True
    assert convert_env_value("debug_request", "0") is False
    assert convert_env_value("acceleration", "100") == 100
    assert convert_env_value("parallel", "all") == 0
    assert convert_env_value("data", "aboveThreshold, belowThreshold") == [
        "aboveThreshold",
        "belowThreshold",
    ]
    with pytest.raises(EnvValueError):
        convert_env_value("seed", "nope")


def test_build_env_values_prefers_file_over_os_environ():
    values = build_env_values(
        {"API_HOST": "from-file", "API_TOKEN": "file-token"},
        environ={"API_HOST": "from-os", "DS_HOST": "os-ds"},
    )
    assert values["host"] == "from-file"
    assert values["token"] == "file-token"
    assert values["ds_host"] == "os-ds"


def test_resolve_env_path_by_name_and_default(tmp_path):
    sandbox = tmp_path / ".env.sandbox"
    sandbox.write_text("API_HOST=https://sandbox.example\n", encoding="utf-8")
    default = tmp_path / ".env"
    default.write_text("API_HOST=https://default.example\n", encoding="utf-8")

    assert resolve_env_path("sandbox", search_dirs=[str(tmp_path)]) == str(sandbox)
    assert resolve_env_path(None, search_dirs=[str(tmp_path)]) == str(default)
    assert resolve_env_path(None, search_dirs=[str(tmp_path / "missing")]) is None


def test_resolve_env_path_from_envs_dir_and_suffix(tmp_path):
    named = tmp_path / "staging.env"
    named.write_text("API_HOST=https://staging.example\n", encoding="utf-8")
    nested_dir = tmp_path / "envs"
    nested_dir.mkdir()
    nested = nested_dir / "dev"
    nested.write_text("API_HOST=https://dev.example\n", encoding="utf-8")

    assert resolve_env_path("staging", search_dirs=[str(tmp_path)]) == str(named)
    assert resolve_env_path("dev", search_dirs=[str(tmp_path)]) == str(nested)


def test_list_available_envs_skips_examples(tmp_path):
    (tmp_path / ".env").write_text("API_HOST=a\n", encoding="utf-8")
    (tmp_path / ".env.sandbox").write_text("API_HOST=b\n", encoding="utf-8")
    (tmp_path / ".env.example").write_text("API_HOST=c\n", encoding="utf-8")
    assert list_available_envs(search_dirs=[str(tmp_path)]) == [".env", "sandbox"]


def test_load_run_env_uses_procedure_env(tmp_path):
    sandbox = tmp_path / ".env.sandbox"
    sandbox.write_text("API_HOST=https://sandbox.example\nAPI_TOKEN=token\n", encoding="utf-8")
    path, values = load_run_env(
        spec=None,
        environ={"PROCEDURE_ENV": "sandbox"},
        search_dirs=[str(tmp_path)],
    )
    assert path == str(sandbox)
    assert values["host"] == "https://sandbox.example"


def test_resolve_env_path_missing_named_file(tmp_path):
    with pytest.raises(EnvFileNotFound):
        resolve_env_path("missing", search_dirs=[str(tmp_path)])
