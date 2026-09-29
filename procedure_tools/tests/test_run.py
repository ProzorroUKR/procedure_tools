import argparse
import logging
from typing import Any

import pytest

from procedure_tools import main
from procedure_tools.utils.handlers import EX_OK


def make_args(**overrides: Any) -> argparse.Namespace:
    values: dict[str, Any] = {
        "data": ["one", "two", "three"],
        "disable_data": None,
        "parallel": None,
        "stop": None,
        "pause": None,
        "wait": None,
        "seed": 1,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


@pytest.fixture(name="runs")
def runs_fixture(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    started: list[str] = []

    def fake_run_data_dir(args: argparse.Namespace, session: Any = None, controller: Any = None) -> tuple[int, None]:  # pylint: disable=unused-argument
        if controller:
            controller.mark_started(args.data)
        started.append(args.data)
        if controller:
            controller.mark_finished(args.data, EX_OK, None)
        return EX_OK, None

    monkeypatch.setattr(main, "run_data_dir", fake_run_data_dir)
    return started


def summary_lines(caplog: pytest.LogCaptureFixture) -> list[str]:
    for record in caplog.records:
        if record.getMessage().startswith("Summary"):
            return [line.strip() for line in record.getMessage().splitlines()[1:] if line.strip()]
    raise AssertionError("no summary logged")


def test_run_skips_disabled_data_dirs_and_marks_them_in_summary(
    runs: list[str], caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    main.run(make_args(disable_data=["two", "missing"]))
    assert runs == ["one", "three"]
    assert summary_lines(caplog) == ["- one  \tsuccess", "- two  \tdisabled", "- three\tsuccess"]


def test_run_skips_disabled_data_dirs_in_parallel(runs: list[str], caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    main.run(make_args(disable_data=["three"], parallel=0))
    assert sorted(runs) == ["one", "two"]
    assert summary_lines(caplog)[2] == "- three\tdisabled"


def test_run_with_everything_disabled_runs_nothing(runs: list[str], caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    main.run(make_args(disable_data=["one", "two", "three"]))
    assert runs == []
    assert all(line.endswith("disabled") for line in summary_lines(caplog))
