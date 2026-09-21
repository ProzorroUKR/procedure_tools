"""The override mechanics every data keyword is built on."""

from data.utils import apply_overrides, build, deep_merge, new_id, parse_value


class TestParseValue:
    def test_reads_back_the_literals_robot_passes_as_strings(self):
        assert parse_value("5") == 5
        assert parse_value("5.5") == 5.5
        assert parse_value("True") is True
        assert parse_value("['a', 'b']") == ["a", "b"]

    def test_keeps_plain_text_as_text(self):
        assert parse_value("active.tendering") == "active.tendering"
        assert parse_value("quick(mode:no-auction)") == "quick(mode:no-auction)"

    def test_leaves_values_that_came_from_a_variable_alone(self):
        value = {"amount": 1}
        assert parse_value(value) is value
        assert parse_value(7) == 7

    def test_reads_none(self):
        assert parse_value("None") is None
        assert parse_value("null") is None


class TestDeepMerge:
    def test_merges_dictionaries_key_by_key(self):
        merged = deep_merge({"a": {"b": 1, "c": 2}}, {"a": {"c": 3}})
        assert merged == {"a": {"b": 1, "c": 3}}

    def test_replaces_lists_as_a_whole(self):
        merged = deep_merge({"items": [1, 2, 3]}, {"items": [9]})
        assert merged == {"items": [9]}

    def test_does_not_touch_the_original(self):
        base = {"a": {"b": 1}}
        deep_merge(base, {"a": {"b": 2}})
        assert base == {"a": {"b": 1}}


class TestApplyOverrides:
    def test_sets_a_plain_field(self):
        assert apply_overrides({"status": "draft"}, {"status": "active"})["status"] == "active"

    def test_follows_a_dotted_path(self):
        data = apply_overrides({"value": {"amount": 1}}, {"value.amount": "500"})
        assert data["value"]["amount"] == 500

    def test_follows_a_list_index(self):
        data = apply_overrides({"items": [{"quantity": 1}]}, {"items.0.quantity": "5"})
        assert data["items"][0]["quantity"] == 5

    def test_merges_a_dictionary_into_an_existing_one(self):
        data = apply_overrides({"value": {"amount": 1, "currency": "UAH"}}, {"value": {"amount": 2}})
        assert data["value"] == {"amount": 2, "currency": "UAH"}

    def test_none_removes_a_field(self):
        assert "status" not in apply_overrides({"status": "draft"}, {"status": None})

    def test_does_not_touch_the_original(self):
        base = {"value": {"amount": 1}}
        apply_overrides(base, {"value.amount": 2})
        assert base["value"]["amount"] == 1


class TestBuild:
    def test_applies_the_dictionary_then_the_paths(self):
        data = build({"value": {"amount": 1, "currency": "UAH"}}, {"value": {"amount": 2}}, **{"value.currency": "EUR"})
        assert data["value"] == {"amount": 2, "currency": "EUR"}


def test_new_id_is_a_hex_identifier():
    identifier = new_id()
    assert len(identifier) == 32
    assert int(identifier, 16) >= 0
    assert new_id() != identifier
