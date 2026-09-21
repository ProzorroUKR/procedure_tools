"""Question payloads."""

import pytest
from data.question import question_answer_data, question_author_data, question_data


class TestQuestionAuthor:
    def test_is_an_organization_not_a_tenderer(self):
        # there is no bid behind a question, and the API refuses "scale"
        author = question_author_data()
        assert "scale" not in author
        assert "kind" not in author

    def test_carries_what_the_api_needs(self):
        author = question_author_data()
        assert set(author) >= {"address", "contactPoint", "identifier", "name"}
        assert author["identifier"]["uri"]


class TestQuestionData:
    def test_is_about_the_tender_by_default(self):
        data = question_data()["data"]
        assert data["questionOf"] == "tender"
        assert "relatedItem" not in data

    def test_a_lot_question_names_the_lot(self):
        data = question_data(question_of="lot", related_item="lot-1")["data"]
        assert data["questionOf"] == "lot"
        assert data["relatedItem"] == "lot-1"

    def test_starts_unanswered(self):
        data = question_data()["data"]
        assert "answer" not in data

    def test_refuses_something_a_question_cannot_be_about(self):
        with pytest.raises(ValueError):
            question_data(question_of="bid")

    def test_an_answer_is_just_the_text(self):
        assert set(question_answer_data()["data"]) == {"answer"}
        assert question_answer_data(answer="бо так")["data"]["answer"] == "бо так"
