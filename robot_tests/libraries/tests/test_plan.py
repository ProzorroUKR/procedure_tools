"""
Plan payloads.

The API refuses a field it does not know, so most of what matters here is what
the payload must *not* contain.
"""

from data.plan import plan_data, plan_item_data, plan_organization_data, reporting_plan_data


class TestPlanOrganization:
    def test_carries_no_contact_point(self):
        # a tender procuring entity has one, a plan buyer must not
        assert "contactPoint" not in plan_organization_data()

    def test_carries_what_the_api_needs(self):
        organization = plan_organization_data()
        assert set(organization) >= {"address", "identifier", "name", "kind"}


class TestPlanItem:
    def test_leaves_out_the_fields_a_plan_item_has_no_room_for(self):
        item = plan_item_data()
        for field in ("deliveryAddress", "additionalClassifications", "description_en", "relatedLot"):
            assert field not in item

    def test_keeps_the_classification_and_the_unit(self):
        item = plan_item_data()
        assert item["classification"]["scheme"] == "ДК021"
        assert item["unit"]["code"]


class TestPlanData:
    def test_acceleration_only_shortens_dates(self):
        # it used to land in the payload, where the API called it a rogue field
        payload = plan_data(acceleration=460800)
        assert "acceleration" not in payload["data"]

    def test_names_the_procedure_the_plan_is_for(self):
        tender = plan_data("aboveThreshold")["data"]["tender"]
        assert tender["procurementMethodType"] == "aboveThreshold"
        assert tender["procurementMethod"] == "open"

    def test_reporting_plan_is_a_limited_method(self):
        tender = reporting_plan_data()["data"]["tender"]
        assert tender["procurementMethodType"] == "reporting"
        assert tender["procurementMethod"] == "limited"

    def test_is_created_as_a_draft(self):
        assert plan_data()["data"]["status"] == "draft"

    def test_is_marked_as_test_data(self):
        assert plan_data()["data"]["mode"] == "test"

    def test_takes_its_pieces_from_the_caller(self):
        buyers = [plan_organization_data(name="Замовник")]
        assert plan_data(buyers=buyers)["data"]["buyers"] == buyers
