"""
Checks on the shape of the suite tree itself.

The conventions in TESTING.md are only worth writing down if something holds
them: a directory that quietly loses its minimal flow, or a suite that names no
procedure, is the kind of thing nobody notices until a run means less than it
appears to.
"""

from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parents[2] / "tests"
PROCEDURES = TESTS / "procedures"

# The suites are written in Robot Framework's Ukrainian localization, so the
# settings they are checked for are the Ukrainian ones (robot.conf.languages.Uk).
LANGUAGE = "language: uk"
DOCUMENTATION = "Документація"
SUITE_SETUP = "Налаштування Suite"
SUITE_TEARDOWN = "Розбірка Suite"

# Every procedure directory holds the shortest path to a completed tender, so
# there is always one suite that says what the procedure normally does.
MINIMAL_FLOW = "complete.robot"

# ... and the refusals that are the other side of it, since what a procedure
# turns down is as much part of it as what it allows.
REFUSALS = "negative"


def procedure_dirs() -> list[Path]:
    return sorted(path for path in PROCEDURES.iterdir() if path.is_dir())


def suites() -> list[Path]:
    return sorted(TESTS.rglob("*.robot"))


def test_there_are_procedure_directories():
    assert procedure_dirs(), f"no procedures under {PROCEDURES}"


@pytest.mark.parametrize("directory", procedure_dirs(), ids=lambda p: p.name)
def test_every_procedure_has_a_minimal_flow(directory):
    assert (directory / MINIMAL_FLOW).is_file(), (
        f"{directory.name} has no {MINIMAL_FLOW}; every procedure needs the shortest "
        f"path to a completed tender, and the branches are named after what they add"
    )


@pytest.mark.parametrize("directory", procedure_dirs(), ids=lambda p: p.name)
def test_the_minimal_flow_is_a_smoke_test(directory):
    # it is the suite that has to stay fast and green, so it runs on every change
    path = directory / MINIMAL_FLOW
    if not path.is_file():
        pytest.skip(f"{directory.name} has no {MINIMAL_FLOW} yet")
    assert "smoke" in path.read_text(encoding="utf-8"), f"{path.name} is not tagged smoke"


@pytest.mark.parametrize("directory", procedure_dirs(), ids=lambda p: p.name)
def test_every_procedure_has_its_refusals(directory):
    refusals = directory / REFUSALS
    assert refusals.is_dir(), (
        f"{directory.name} has no {REFUSALS}/ directory; what a procedure refuses belongs "
        f"beside the flows it is the other side of, not in a heap of its own"
    )
    assert list(refusals.glob("*.robot")), f"{directory.name}/{REFUSALS} holds no suite"


@pytest.mark.parametrize("path", suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_refusal_suite_names_its_procedure(path):
    # a run filtered to one procedure has to get that procedure's refusals too
    if path.parent.name != REFUSALS:
        pytest.skip("not a refusal suite")
    procedure = path.parent.parent.name
    text = path.read_text(encoding="utf-8")
    assert f"procedure:{procedure}" in text, f"{path.name} does not tag procedure:{procedure}"
    assert "negative" in text, f"{path.name} is not tagged negative"


EXPECT_ERROR = "Run Keyword And Expect Error"


def expected_patterns(text: str) -> list[tuple[int, str]]:
    """
    The error pattern of every ``Run Keyword And Expect Error`` in ``text``.

    The pattern is the keyword's first argument, which sits either on the same
    line or, when the call is wrapped, on the ``...`` line under it.
    """
    lines = text.splitlines()
    found: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(EXPECT_ERROR):
            continue
        rest = stripped[len(EXPECT_ERROR) :]
        number = index + 1
        while not rest.strip() and index + 1 < len(lines):
            index += 1
            rest = lines[index].strip().removeprefix("...")
            number = index + 1
        arguments = [part for part in rest.split("    ") if part.strip()]
        found.append((number, arguments[0].strip() if arguments else ""))
    return found


@pytest.mark.parametrize("path", suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_no_refusal_accepts_any_failure(path):
    # "Expect Error    *" passes on the wrong failure as readily as the right one
    if path.parent.name != REFUSALS:
        pytest.skip("not a refusal suite")
    patterns = expected_patterns(path.read_text(encoding="utf-8"))
    assert patterns, f"{path.name} is a refusal suite that expects no error"
    for number, pattern in patterns:
        assert pattern and pattern != "*", (
            f"{path.name}:{number} expects any error at all; name the reason the API gives"
        )


@pytest.mark.parametrize("path", suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_suite_says_what_it_is_for(path):
    text = path.read_text(encoding="utf-8")
    assert DOCUMENTATION in text, f"{path.name} has no documentation"


@pytest.mark.parametrize("path", suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_suite_declares_its_language(path):
    # the Ukrainian section and setting names are only recognised when the file
    # says which language it is written in, and it has to say so on line one
    first = path.read_text(encoding="utf-8").splitlines()[0]
    assert first.strip() == LANGUAGE, f"{path.name} does not start with '{LANGUAGE}'"


@pytest.mark.parametrize("path", suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_suite_closes_the_session_it_opens(path):
    text = path.read_text(encoding="utf-8")
    if SUITE_SETUP not in text:
        pytest.skip("no suite setup")
    assert SUITE_TEARDOWN in text, f"{path.name} opens a session and never closes it"
