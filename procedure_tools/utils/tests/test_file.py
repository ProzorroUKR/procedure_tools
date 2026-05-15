import pytest

from procedure_tools.utils.file import parse_data_file_parts


def test_parse_data_file_parts_none_prefixes_legacy():
    assert parse_data_file_parts(
        "award_update_0_1_award_patch.json",
        "award_update",
        middle_parts_count=2,
    ) == (
        "award_update",
        ["0", "1"],
        "award_patch",
        ["json"],
    )


def test_parse_data_file_parts_award_update_with_prefixes():
    assert parse_data_file_parts(
        "award_update_0_award_1_award_patch.json",
        "award_update",
        middle_parts_count=2,
        middle_parts_prefixes=("", "award_"),
    ) == (
        "award_update",
        ["0", "1"],
        "award_patch",
        ["json"],
    )


def test_parse_data_file_parts_wrong_prefixes_length():
    with pytest.raises(ValueError):
        parse_data_file_parts(
            "award_update_0_award_0_award_patch.json",
            "award_update",
            middle_parts_count=2,
            middle_parts_prefixes=("", "award_", "action_"),
        )


def test_parse_data_file_parts_invalid_middle_segment():
    with pytest.raises(ValueError):
        parse_data_file_parts(
            "award_update_0_award_x_award_patch.json",
            "award_update",
            middle_parts_count=2,
            middle_parts_prefixes=("", "award_"),
        )
