import json
import os
from types import SimpleNamespace

import pytest

from procedure_tools.actions import ACTIONS
from procedure_tools.context import Context
from procedure_tools.steps import (
    StepError,
    discover_steps,
    find_resource_path,
    get_numberless_filename,
    split_action,
)
from procedure_tools.utils.file import get_default_data_dirs, get_default_data_path

ACTION_NAMES = [
    "tender_create",
    "tender_patch",
    "tender_award_patch",
    "tender_award_complaint_patch",
    "framework",
    "framework_patch",
]


def test_get_numberless_filename():
    assert get_numberless_filename("0010_tender_create.json") == "tender_create.json"
    assert get_numberless_filename("10_tender_create.json") == "tender_create.json"
    assert get_numberless_filename("tender_create.json") == "tender_create.json"


def test_split_action_without_parts():
    assert split_action("tender_create", ACTION_NAMES) == ("tender_create", [], "")


def test_split_action_with_parts():
    assert split_action("tender_award_patch_0", ACTION_NAMES) == ("tender_award_patch", ["0"], "")
    assert split_action("tender_award_complaint_patch_0_1_bot", ACTION_NAMES) == (
        "tender_award_complaint_patch",
        ["0", "1", "bot"],
        "",
    )


def test_split_action_prefers_longest_action_name():
    assert split_action("framework_patch_0", ACTION_NAMES) == ("framework_patch", ["0"], "")
    assert split_action("framework_0", ACTION_NAMES) == ("framework", ["0"], "")


def test_split_action_skips_stage_prefix():
    assert split_action("stage2_tender_create", ACTION_NAMES) == ("tender_create", [], "stage2_")
    assert split_action("selection_tender_award_patch_1", ACTION_NAMES) == ("tender_award_patch", ["1"], "selection_")
    assert split_action("a_b_tender_award_complaint_patch_0_1_bot", ACTION_NAMES) == (
        "tender_award_complaint_patch",
        ["0", "1", "bot"],
        "a_b_",
    )


def test_split_action_unknown():
    with pytest.raises(StepError):
        split_action("tender", ACTION_NAMES)
    with pytest.raises(StepError):
        split_action("stage2_tender_creat", ACTION_NAMES)
    with pytest.raises(StepError):
        split_action("stage2_", ACTION_NAMES)


def write(path, name, content="{}"):
    with open(os.path.join(path, name), "w", encoding="utf-8") as f:
        f.write(content)


def test_discover_steps_orders_by_number_and_skips_resources(tmp_path):
    write(tmp_path, "0020_tender_patch.json")
    write(tmp_path, "0010_tender_create.json")
    write(tmp_path, "0010_tender_document_file.txt", "document")
    write(tmp_path, "notes.md", "not an action")
    steps = discover_steps(str(tmp_path), ACTION_NAMES)
    assert [step.filename for step in steps] == ["0010_tender_create.json", "0020_tender_patch.json"]
    assert steps[0].number == "0010"
    assert steps[0].action == "tender_create"
    assert steps[0].parts == []
    assert steps[0].name == "tender_create.json"


def test_discover_steps_requires_number_prefix(tmp_path):
    write(tmp_path, "tender_create.json")
    with pytest.raises(StepError, match="number prefix"):
        discover_steps(str(tmp_path), ACTION_NAMES)


def test_discover_steps_unknown_action_lists_available(tmp_path):
    write(tmp_path, "0010_tender_creat.json")
    with pytest.raises(StepError, match="unknown action 'tender_creat'") as e:
        discover_steps(str(tmp_path), ACTION_NAMES)
    assert " - tender_create" in str(e.value)


def test_step_parts(tmp_path):
    write(tmp_path, "0010_tender_award_complaint_patch_0_1_bot.json")
    (step,) = discover_steps(str(tmp_path), ACTION_NAMES)
    assert step.index(0) == 0
    assert step.index(1) == 1
    assert step.part(2) == "bot"
    assert step.part(3) is None
    assert step.index(3, default=-1) == -1
    with pytest.raises(StepError, match="missing index"):
        step.index(3)
    with pytest.raises(StepError, match="must be an index"):
        step.index(2)


def test_discover_steps_keeps_prefix(tmp_path):
    write(tmp_path, "4010_stage2_tender_patch.json")
    (step,) = discover_steps(str(tmp_path), ACTION_NAMES)
    assert (step.action, step.parts, step.prefix) == ("tender_patch", [], "stage2_")
    assert step.stem == "stage2_tender_patch"
    assert step.matches("stage2_tender_patch.json")


def test_step_matches_with_or_without_number(tmp_path):
    write(tmp_path, "0010_tender_create.json")
    (step,) = discover_steps(str(tmp_path), ACTION_NAMES)
    assert step.matches("0010_tender_create.json")
    assert step.matches("tender_create.json")
    assert step.matches("0999_tender_create.json")
    assert not step.matches("tender_patch.json")
    assert not step.matches(None)


def test_find_resource_path_ignores_number_prefix(tmp_path):
    write(tmp_path, "0010_tender_document_file.txt", "document")
    write(tmp_path, "plain.txt", "document")
    assert find_resource_path(str(tmp_path), "tender_document_file.txt") == str(
        tmp_path / "0010_tender_document_file.txt"
    )
    assert find_resource_path(str(tmp_path), "plain.txt") == str(tmp_path / "plain.txt")
    assert find_resource_path(str(tmp_path), "missing.txt") is None


def make_context(data_path, steps=()):
    args = SimpleNamespace(token="token", bot_token=None, reviewer_token=None, stop=None, pause=None, wait=[])
    return Context(args, client=None, ds_client=None, data_path=data_path, steps=list(steps))


def test_context_load_renders_templates(tmp_path):
    write(tmp_path, "0010_tender_patch.json", '{"data": {"id": "{{ tender.id }}", "n": {{ acceleration }}}}')
    (step,) = discover_steps(str(tmp_path), ACTION_NAMES)
    context = make_context(str(tmp_path), [step])
    context["tender"] = {"id": "abc"}
    context["acceleration"] = 5
    assert context.load(step) == {"data": {"id": "abc", "n": 5}}


def test_context_load_empty_file_is_empty_object(tmp_path):
    write(tmp_path, "0010_tender_patch.json", "\n")
    (step,) = discover_steps(str(tmp_path), ACTION_NAMES)
    assert make_context(str(tmp_path), [step]).load(step) == {}


def test_context_lists():
    context = make_context(".")
    context.set_item("bids", 2, {"id": "b"})
    assert context["bids"] == [None, None, {"id": "b"}]
    assert context.item("bids", 2) == {"id": "b"}
    with pytest.raises(SystemExit):
        context.item("bids", 0)
    with pytest.raises(SystemExit):
        context.require("tender")


@pytest.mark.parametrize("data_dir", sorted(get_default_data_dirs()))
def test_bundled_data_dirs_discover(data_dir):
    """Every bundled data folder resolves to known actions, valid JSON and existing resources."""
    data_path = get_default_data_path(data_dir)
    steps = discover_steps(data_path, ACTIONS)
    assert steps, data_dir
    for step in steps:
        with open(step.path, encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            continue
        # resources are referenced by title (or an explicit "file") in attach files and bid documents
        if step.action.endswith("_document_attach") or step.action == "tender_document_put":
            data = json.loads(content)
            resource = data.get("file") or data["data"]["title"]
            assert find_resource_path(data_path, resource), f"{step.filename}: resource {resource} missing"
        if step.action == "tender_bid_create":
            data = json.loads(content)
            for container in ("documents", "eligibilityDocuments", "financialDocuments", "qualificationDocuments"):
                for document in data["data"].get(container, []):
                    resource = document.get("file") or document["title"]
                    assert find_resource_path(data_path, resource), f"{step.filename}: {resource}"
