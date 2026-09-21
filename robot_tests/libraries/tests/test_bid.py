"""Bid payloads, which are read off the tender they answer."""

from data.bid import bid_data, bid_patch_data, lot_values_data
from data.document import document_data
from data.tender import items_data, lots_data, tender_data


def created_tender(lots=0):
    """A tender as the API hands it back: its items carry ids."""
    lot_list = lots_data(lots) if lots else []
    payload = tender_data(lots=lot_list, items=items_data(lots=lot_list))
    for index, item in enumerate(payload["data"]["items"]):
        item["id"] = f"item-{index}"
    return payload["data"]


class TestLotValues:
    def test_offers_every_lot(self):
        lots = lots_data(3)
        assert [value["relatedLot"] for value in lot_values_data(lots)] == [lot["id"] for lot in lots]

    def test_stays_under_the_ceiling_of_each_lot(self):
        lots = lots_data(2, amount=1000)
        for value in lot_values_data(lots):
            assert value["value"]["amount"] < 1000

    def test_takes_the_amounts_it_is_given(self):
        lots = lots_data(2)
        values = lot_values_data(lots, amounts=[10, 20])
        assert [value["value"]["amount"] for value in values] == [10, 20]


class TestBidData:
    def test_a_tender_with_lots_is_answered_with_lot_values(self):
        data = bid_data(created_tender(lots=2))["data"]
        assert len(data["lotValues"]) == 2
        assert "value" not in data

    def test_a_tender_without_lots_is_answered_with_one_value(self):
        data = bid_data(created_tender())["data"]
        assert "lotValues" not in data
        assert data["value"]["amount"] > 0

    def test_item_prices_add_up_to_what_was_offered_for_their_lot(self):
        tender = created_tender(lots=2)
        data = bid_data(tender)["data"]
        offered = {value["relatedLot"]: value["value"]["amount"] for value in data["lotValues"]}
        priced = {item["id"]: item["unit"]["value"]["amount"] * item["quantity"] for item in data["items"]}
        for tender_item in tender["items"]:
            assert priced[tender_item["id"]] == offered[tender_item["relatedLot"]]

    def test_bid_items_reference_the_items_of_the_tender(self):
        tender = created_tender(lots=1)
        data = bid_data(tender)["data"]
        assert [item["id"] for item in data["items"]] == [item["id"] for item in tender["items"]]

    def test_is_created_as_a_draft(self):
        assert bid_data(created_tender())["data"]["status"] == "draft"

    def test_documents_travel_with_their_file_content(self):
        proposal = document_data(title="proposal.txt")
        eligibility = document_data(title="eligibility.txt")
        payload = bid_data(created_tender(), documents=[proposal], eligibility_documents=[eligibility])
        assert [d["title"] for d in payload["data"]["documents"]] == ["proposal.txt"]
        assert [d["title"] for d in payload["data"]["eligibilityDocuments"]] == ["eligibility.txt"]
        assert set(payload["contents"]) == {"proposal.txt", "eligibility.txt"}

    def test_empty_document_containers_are_left_out(self):
        data = bid_data(created_tender())["data"]
        assert "documents" not in data
        assert "eligibilityDocuments" not in data

    def test_overrides_reach_a_lot_value(self):
        data = bid_data(created_tender(lots=1), **{"lotValues.0.value.amount": "1999"})["data"]
        assert data["lotValues"][0]["value"]["amount"] == 1999


def test_bid_patch_names_the_target_status():
    assert bid_patch_data("pending") == {"data": {"status": "pending"}}
