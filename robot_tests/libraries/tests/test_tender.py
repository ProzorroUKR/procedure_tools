"""Tender payloads and the config block that decides how the CDB behaves."""

from data.tender import (
    ABOVE_THRESHOLD_CONFIG,
    REPORTING_CONFIG,
    items_data,
    lots_data,
    milestones_data,
    procurement_method_details,
    reporting_tender_data,
    tender_data,
    tender_patch_data,
)


class TestProcurementMethodDetails:
    def test_names_the_accelerator_the_cdb_expects(self):
        assert procurement_method_details(460800) == "quick, accelerator=460800"

    def test_is_empty_without_acceleration(self):
        assert procurement_method_details(None) == ""
        assert procurement_method_details(0) == ""


class TestLotsAndItems:
    def test_every_lot_gets_its_own_id(self):
        lots = lots_data(3)
        assert len({lot["id"] for lot in lots}) == 3

    def test_items_are_spread_over_the_lots(self):
        lots = lots_data(2)
        items = items_data(lots=lots)
        # every lot needs at least one item of its own
        assert {item["relatedLot"] for item in items} == {lot["id"] for lot in lots}

    def test_items_without_lots_carry_no_lot(self):
        assert all("relatedLot" not in item for item in items_data(count=2))

    def test_milestones_are_per_lot(self):
        lots = lots_data(2)
        milestones = milestones_data(lots)
        assert {milestone["relatedLot"] for milestone in milestones} == {lot["id"] for lot in lots}

    def test_every_lot_has_a_financing_and_a_delivery_milestone(self):
        lots = lots_data(1)
        kinds = {milestone["type"] for milestone in milestones_data(lots)}
        assert kinds == {"financing", "delivery"}


class TestTenderData:
    def test_carries_a_config_block(self):
        payload = tender_data()
        assert payload["config"] == ABOVE_THRESHOLD_CONFIG

    def test_config_can_be_replaced_whole(self):
        payload = tender_data(config={"hasAuction": False})
        assert payload["config"] == {"hasAuction": False}

    def test_lots_appear_only_when_there_are_any(self):
        assert "lots" not in tender_data()["data"]
        assert len(tender_data(lots=lots_data(2))["data"]["lots"]) == 2

    def test_submission_appears_only_when_given(self):
        assert "submissionMethodDetails" not in tender_data()["data"]
        details = tender_data(submission="quick(mode:no-auction)")["data"]["submissionMethodDetails"]
        assert details == "quick(mode:no-auction)"

    def test_acceleration_shortens_the_tender_period_instead_of_being_sent(self):
        payload = tender_data(acceleration=460800)
        assert "acceleration" not in payload["data"]
        assert payload["data"]["procurementMethodDetails"] == "quick, accelerator=460800"

    def test_is_created_as_a_draft_test_tender(self):
        data = tender_data()["data"]
        assert data["status"] == "draft"
        assert data["mode"] == "test"

    def test_overrides_reach_nested_fields(self):
        data = tender_data(**{"value.amount": "5000"})["data"]
        assert data["value"]["amount"] == 5000


class TestReportingTenderData:
    def test_is_a_limited_procedure(self):
        data = reporting_tender_data()["data"]
        assert data["procurementMethod"] == "limited"
        assert data["procurementMethodType"] == "reporting"

    def test_names_the_legal_ground(self):
        assert reporting_tender_data()["data"]["causeDetails"]["scheme"] == "DECREE1275"

    def test_has_no_tender_period_because_there_is_no_tendering(self):
        assert "tenderPeriod" not in reporting_tender_data()["data"]

    def test_config_switches_off_what_reporting_does_not_have(self):
        config = reporting_tender_data()["config"]
        assert config == REPORTING_CONFIG
        assert config["hasAuction"] is False
        assert config["hasAwardComplaints"] is False


def test_tender_patch_names_the_target_status():
    assert tender_patch_data("active.tendering") == {"data": {"status": "active.tendering"}}


class TestLotsWithoutAnAuction:
    def test_a_lot_carries_a_minimal_step_by_default(self):
        assert "minimalStep" in lots_data(1)[0]

    def test_a_lot_of_a_tender_without_an_auction_carries_none(self):
        # there is no step to improve on, and the API calls the field rogue
        lot = lots_data(1, with_minimal_step=False)[0]
        assert "minimalStep" not in lot
        assert lot["value"]["amount"]
        assert lot["guarantee"]["amount"]


class TestTenderWithoutAnAuction:
    def test_the_submission_method_is_left_out(self):
        # there is nothing to submit into, and the API calls the field rogue
        config = dict(ABOVE_THRESHOLD_CONFIG, hasAuction=False)
        data = tender_data(config=config, submission="quick(mode:fast-forward)")["data"]
        assert "submissionMethodDetails" not in data

    def test_the_lots_lose_their_minimal_step(self):
        config = dict(ABOVE_THRESHOLD_CONFIG, hasAuction=False)
        data = tender_data(lots=lots_data(2), config=config)["data"]
        assert all("minimalStep" not in lot for lot in data["lots"])
        assert all(lot["value"]["amount"] for lot in data["lots"])

    def test_an_auction_tender_keeps_both(self):
        data = tender_data(lots=lots_data(1), submission="quick(mode:fast-forward)")["data"]
        assert data["submissionMethodDetails"] == "quick(mode:fast-forward)"
        assert "minimalStep" in data["lots"][0]
