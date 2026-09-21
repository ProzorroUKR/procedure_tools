"""
Criteria and the bid answers derived from them.

This is the one place where the data has to agree with what the API sent back,
so the tests are about that agreement rather than about shapes.
"""

import pytest
from data.criteria import (
    LOT_RELATED,
    classification_ids,
    criteria_data,
    criterion,
    folder_criteria,
    requirement_responses_data,
    requirement_value,
)
from data.criteria_templates import TEMPLATES
from data.tender import lots_data


def requirements(criteria):
    return [
        requirement for item in criteria for group in item["requirementGroups"] for requirement in group["requirements"]
    ]


class TestTemplates:
    def test_every_template_keeps_the_law_its_legislation_points_at(self):
        # the generator used to strip every "id", including this one, and the
        # API refuses a legislation entry without it
        for classification_id, template in TEMPLATES.items():
            for entry in template.get("legislation", []):
                assert entry["identifier"].get("id"), f"{classification_id} lost its legislation id"

    def test_no_template_carries_a_requirement_id(self):
        for classification_id, template in TEMPLATES.items():
            for group in template["requirementGroups"]:
                for requirement in group["requirements"]:
                    assert "id" not in requirement, f"{classification_id} carries a stale requirement id"

    def test_every_template_has_a_source_and_a_relates_to(self):
        for classification_id, template in TEMPLATES.items():
            assert template.get("source"), classification_id
            assert template.get("relatesTo"), classification_id


class TestCriterion:
    def test_sets_the_classification_it_was_asked_for(self):
        built = criterion("CRITERION.EXCLUSION.BUSINESS.BANKRUPTCY")
        assert built["classification"]["id"] == "CRITERION.EXCLUSION.BUSINESS.BANKRUPTCY"

    def test_gives_every_requirement_a_fresh_id(self):
        first = requirements([criterion("CRITERION.OTHER.BID.GUARANTEE", related_item="lot-1")])
        second = requirements([criterion("CRITERION.OTHER.BID.GUARANTEE", related_item="lot-1")])
        assert {r["id"] for r in first}.isdisjoint({r["id"] for r in second})

    def test_binds_a_lot_criterion_to_its_lot(self):
        built = criterion(LOT_RELATED[0], related_item="lot-1")
        assert built["relatesTo"] == "lot"
        assert built["relatedItem"] == "lot-1"

    def test_falls_back_to_the_tender_when_there_is_no_lot(self):
        built = criterion(LOT_RELATED[0])
        assert built["relatesTo"] == "tender"
        assert "relatedItem" not in built

    def test_refuses_an_unknown_classification(self):
        with pytest.raises(ValueError):
            criterion("CRITERION.DOES.NOT.EXIST")


class TestCriteriaData:
    def test_builds_what_the_data_folder_posts(self):
        # not the whole catalogue: a criterion valid in one procedure is
        # refused in another, so the folder decides the set
        expected = folder_criteria("aboveThreshold")
        built = [item["classification"]["id"] for item in criteria_data(folder="aboveThreshold")["data"]]
        assert built == expected

    def test_a_folder_with_its_own_criteria_gets_them(self):
        lcc = folder_criteria("aboveThreshold.lcc")
        base = folder_criteria("aboveThreshold")
        assert set(lcc) > set(base), "the lcc folder adds life cycle cost criteria"

    def test_refuses_a_folder_that_posts_none(self):
        with pytest.raises(ValueError):
            criteria_data(folder="notAFolder")

    def test_repeats_the_lot_criteria_for_every_lot(self):
        lots = lots_data(3)
        criteria = criteria_data(lots=lots)["data"]
        per_lot = [item for item in criteria if item.get("relatesTo") == "lot"]
        in_folder = [key for key in folder_criteria("aboveThreshold") if key in LOT_RELATED]
        assert len(per_lot) == len(in_folder) * 3
        assert {item["relatedItem"] for item in per_lot} == {lot["id"] for lot in lots}

    def test_an_item_criterion_is_bound_to_the_item_it_is_given(self):
        criteria = criteria_data(folder="reporting.local", related_item="item-1")["data"]
        assert [item["relatedItem"] for item in criteria] == ["item-1"]

    def test_requirement_ids_are_unique_across_the_whole_payload(self):
        criteria = criteria_data(lots=lots_data(2))["data"]
        ids = [requirement["id"] for requirement in requirements(criteria)]
        assert len(ids) == len(set(ids))

    def test_include_and_exclude_narrow_the_set(self):
        chosen = classification_ids()[:2]
        assert len(criteria_data(include=chosen)["data"]) == 2
        base = len(folder_criteria("aboveThreshold"))
        dropped = [key for key in chosen if key in folder_criteria("aboveThreshold")]
        assert len(criteria_data(exclude=chosen)["data"]) == base - len(dropped)


class TestRequirementValue:
    def test_a_boolean_answers_what_is_expected(self):
        assert requirement_value({"dataType": "boolean", "expectedValue": True}) == {"value": True}
        assert requirement_value({"dataType": "boolean", "expectedValue": False}) == {"value": False}

    def test_a_choice_answers_with_allowed_values(self):
        answer = requirement_value(
            {"dataType": "string", "expectedValues": ["Українська", "Англійська"], "expectedMinItems": 1}
        )
        assert answer == {"values": ["Українська"]}

    def test_a_number_answers_within_its_bounds(self):
        assert requirement_value({"dataType": "number", "minValue": 0.5, "maxValue": 3.0}) == {"value": 3.0}
        assert requirement_value({"dataType": "integer", "minValue": 90}) == {"value": 90}

    def test_every_catalogue_requirement_gets_an_answer_that_satisfies_it(self):
        for requirement in requirements(criteria_data(lots=lots_data(1))["data"]):
            answer = requirement_value(requirement)
            value = answer.get("value")
            if requirement.get("minValue") is not None:
                assert value >= requirement["minValue"], requirement["title"]
            if requirement.get("maxValue") is not None:
                assert value <= requirement["maxValue"], requirement["title"]
            if requirement.get("expectedValue") is not None:
                assert value == requirement["expectedValue"], requirement["title"]
            if requirement.get("expectedValues") is not None:
                assert set(answer["values"]) <= set(requirement["expectedValues"]), requirement["title"]


class TestRequirementResponses:
    def setup_method(self):
        self.criteria = criteria_data(lots=lots_data(1))["data"]

    def test_answers_only_the_first_requirement_group(self):
        answered = {response["requirement"]["id"] for response in requirement_responses_data(self.criteria)["data"]}
        for item in self.criteria:
            if item.get("source") == "procuringEntity":
                continue
            first, *rest = item["requirementGroups"]
            assert all(requirement["id"] in answered for requirement in first["requirements"])
            for group in rest:
                assert all(requirement["id"] not in answered for requirement in group["requirements"])

    def test_leaves_out_what_the_procuring_entity_answers(self):
        answered = {response["requirement"]["id"] for response in requirement_responses_data(self.criteria)["data"]}
        for item in self.criteria:
            if item.get("source") != "procuringEntity":
                continue
            assert all(requirement["id"] not in answered for requirement in requirements([item]))

    def test_sends_no_evidences_without_a_document(self):
        responses = requirement_responses_data(self.criteria)["data"]
        assert all("evidences" not in response for response in responses)

    def test_sends_evidences_only_for_what_the_bidder_answers_now(self):
        # the API refuses evidences for criteria the winner answers later
        winner_requirements = {
            requirement["id"]
            for item in self.criteria
            if item.get("source") != "tenderer"
            for requirement in requirements([item])
        }
        responses = requirement_responses_data(self.criteria, document_title="proposal.txt")["data"]
        with_evidences = [response for response in responses if response.get("evidences")]
        assert with_evidences, "expected evidences for the tenderer criteria"
        assert all(response["requirement"]["id"] not in winner_requirements for response in with_evidences)

    def test_evidences_point_at_the_document_of_the_bid(self):
        responses = requirement_responses_data(self.criteria, document_title="proposal.txt")["data"]
        for response in responses:
            for evidence in response.get("evidences", []):
                assert evidence["type"] == "document"
                assert evidence["relatedDocument"]["title"] == "proposal.txt"

    def test_accepts_the_payload_the_api_returned(self):
        wrapped = requirement_responses_data({"data": self.criteria})
        assert wrapped == requirement_responses_data(self.criteria)
