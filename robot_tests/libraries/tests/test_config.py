"""
Reading the config schemas, and what the config suites claim about them.

The second half is the useful half: it checks that a config suite is aimed at a
procedure that can actually vary the key it names. Aiming one at a procedure
where the schema pins the value is an easy mistake and an expensive one - the
suite fails against the API for a reason that has nothing to do with the
behaviour it meant to cover.
"""

import re
from pathlib import Path

import pytest
from data.config import (
    FRAMEWORK,
    TENDER,
    config_defaults,
    config_options,
    config_schema,
    is_variable,
    procedures,
    procedures_varying,
    variable_keys,
    variable_pairs,
)

CONFIG_TESTS = Path(__file__).resolve().parents[2] / "tests" / "config"
# The suites are written in Robot Framework's Ukrainian localization, so the
# tag settings are spelled the Ukrainian way ("Тестові теги", "[Теги]").
TAG_PATTERN = re.compile(r"^(?:Тестові теги|\s+\[Теги\])\s+(.+)$", re.MULTILINE)


def snake(name: str) -> str:
    """``hasAwardingOrder`` -> ``has_awarding_order``, the directory it lives in."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def suite_tags(path: Path) -> set[str]:
    tags: set[str] = set()
    for line in TAG_PATTERN.findall(path.read_text(encoding="utf-8")):
        tags.update(part.strip() for part in re.split(r"\s{2,}|\t", line) if part.strip())
    return tags


def config_suites() -> list[Path]:
    return sorted(CONFIG_TESTS.rglob("*.robot"))


class TestSchemaQueries:
    def test_knows_the_procedures_of_both_groups(self):
        assert "aboveThreshold" in procedures(TENDER)
        assert "dynamicPurchasingSystem" in procedures(FRAMEWORK)

    def test_defaults_cover_every_key_of_a_procedure(self):
        defaults = config_defaults("aboveThreshold")
        assert set(defaults) == set(config_schema("aboveThreshold"))

    def test_a_pinned_key_is_not_variable(self):
        # the API refuses anything else, which a live run confirmed
        assert not is_variable("hasAwardingOrder", "aboveThreshold")
        assert config_options("hasAwardingOrder", "aboveThreshold") == [True]

    def test_the_same_key_can_be_free_elsewhere(self):
        assert is_variable("hasAwardingOrder", "competitiveOrdering")
        assert is_variable("hasAwardingOrder", "requestForProposal")

    def test_the_same_key_can_default_differently_per_procedure(self):
        assert config_defaults("competitiveOrdering")["hasAwardingOrder"] is True
        assert config_defaults("requestForProposal")["hasAwardingOrder"] is False

    def test_above_threshold_is_nearly_fully_pinned(self):
        assert variable_keys("aboveThreshold") == ["hasAuction", "hasValueRestriction"]

    def test_unknown_names_are_refused(self):
        with pytest.raises(ValueError):
            config_schema("notAProcedure")
        with pytest.raises(ValueError):
            config_options("notAKey", "aboveThreshold")

    def test_the_test_space_is_finite_and_not_empty(self):
        pairs = variable_pairs()
        assert 10 < len(pairs) < 500
        assert ("TenderConfig", "aboveThreshold", "hasAuction") in pairs


class TestConfigSuites:
    def test_there_are_config_suites(self):
        assert config_suites(), f"no config suites under {CONFIG_TESTS}"

    @pytest.mark.parametrize("path", config_suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
    def test_a_suite_lives_in_the_directory_of_the_option_it_is_about(self, path):
        """
        One directory per config option, named after it.

        The directory is what makes the set readable: everything known about
        ``hasAuction`` is in one place, whichever procedures it covers.
        """
        tags = suite_tags(path)
        keys = [tag.split(":", 1)[1] for tag in tags if tag.startswith("config:")]
        assert keys, f"{path.name} names no config option"
        expected = {snake(key) for key in keys}
        assert path.parent.name in expected, (
            f"{path.parent.name}/{path.name} is about {keys}; it belongs in {sorted(expected)}"
        )

    @pytest.mark.parametrize("path", config_suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
    def test_a_suite_names_the_option_and_the_procedure_it_is_about(self, path):
        tags = suite_tags(path)
        assert any(tag.startswith("config:") for tag in tags), f"{path.name} names no config option"
        assert any(tag.startswith("procedure:") for tag in tags), f"{path.name} names no procedure"

    @pytest.mark.parametrize("path", config_suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
    def test_the_option_it_names_exists_in_the_procedure_it_names(self, path):
        tags = suite_tags(path)
        keys = [tag.split(":", 1)[1] for tag in tags if tag.startswith("config:")]
        names = [tag.split(":", 1)[1] for tag in tags if tag.startswith("procedure:")]
        group = FRAMEWORK if "framework" in path.parts else TENDER
        for name in names:
            if name not in procedures(group):
                pytest.fail(f"{path.name}: {name!r} is not a {group} procedure")
            for key in keys:
                assert key in config_schema(name, group), f"{path.name}: {name} has no config key {key!r}"

    @pytest.mark.parametrize("path", config_suites(), ids=lambda p: f"{p.parent.name}/{p.stem}")
    def test_a_suite_that_varies_an_option_is_aimed_where_it_can_vary(self, path):
        # a suite tagged "negative" is about the schema refusing the change, so
        # it belongs exactly where the key is pinned
        tags = suite_tags(path)
        if "negative" in tags:
            return
        keys = [tag.split(":", 1)[1] for tag in tags if tag.startswith("config:")]
        names = [tag.split(":", 1)[1] for tag in tags if tag.startswith("procedure:")]
        group = FRAMEWORK if "framework" in path.parts else TENDER
        for name in names:
            for key in keys:
                assert is_variable(key, name, group), (
                    f"{path.name}: {name} pins {key} to {config_options(key, name, group)}; "
                    f"it can vary in {procedures_varying(key, group) or 'no procedure'}"
                )
