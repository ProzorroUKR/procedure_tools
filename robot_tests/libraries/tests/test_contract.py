"""Contract payloads, which are read off the contract the CDB created."""

from data.contract import (
    contract_active_data,
    contract_change_active_data,
    contract_change_data,
    contract_item_data,
    contract_signer_info_data,
    contract_terminated_data,
    contract_value_data,
    unit_amount,
)

CONTRACT = {
    "id": "contract-1",
    "dateModified": "2026-01-10T12:00:00+02:00",
    "value": {"amount": 1000, "currency": "UAH", "valueAddedTaxIncluded": True},
    "items": [
        {
            "id": "item-1",
            "quantity": 2,
            "description": "опис",
            "classification": {"id": "42000000-6", "scheme": "ДК021"},
            "unit": {"code": "KGM", "name": "кг"},
            "relatedLot": "lot-1",
        },
        {"id": "item-2", "quantity": 8, "unit": {"code": "KGM", "name": "кг"}},
    ],
}


class TestContractItem:
    def test_echoes_the_fields_the_contract_already_has(self):
        item = contract_item_data(CONTRACT["items"][0], amount=10)
        assert item["id"] == "item-1"
        assert item["relatedLot"] == "lot-1"
        assert item["classification"]["id"] == "42000000-6"

    def test_prices_the_unit(self):
        item = contract_item_data(CONTRACT["items"][0], amount=10)
        assert item["unit"]["value"] == {"amount": 10, "valueAddedTaxIncluded": False}

    def test_leaves_out_what_the_contract_does_not_have(self):
        assert "relatedLot" not in contract_item_data(CONTRACT["items"][1], amount=10)


class TestContractActive:
    def test_spreads_the_value_over_the_quantities(self):
        assert unit_amount(CONTRACT) == 100  # 1000 over 2 + 8 units

    def test_signs_it_on_the_date_the_contract_was_last_touched(self):
        data = contract_active_data(CONTRACT)["data"]
        assert data["dateSigned"] == CONTRACT["dateModified"]
        assert data["period"]["startDate"] == CONTRACT["dateModified"]

    def test_the_period_ends_after_it_starts(self):
        period = contract_active_data(CONTRACT)["data"]["period"]
        assert period["endDate"] > period["startDate"]

    def test_keeps_the_value_it_was_awarded(self):
        value = contract_active_data(CONTRACT)["data"]["value"]
        assert value["amount"] == 1000
        assert value["amountNet"] == value["amount"]

    def test_takes_an_amount_when_told(self):
        assert contract_active_data(CONTRACT, amount=500)["data"]["value"]["amount"] == 500

    def test_activates_it(self):
        assert contract_active_data(CONTRACT)["data"]["status"] == "active"

    def test_prices_every_item(self):
        items = contract_active_data(CONTRACT)["data"]["items"]
        assert len(items) == len(CONTRACT["items"])
        assert all(item["unit"]["value"]["amount"] for item in items)


class TestOtherContractPayloads:
    def test_signer_info_is_wrapped_the_way_the_request_expects(self):
        payload = contract_signer_info_data()
        assert set(payload) == {"data"}
        assert payload["data"]["name"]

    def test_value_change_keeps_amount_and_net_together(self):
        value = contract_value_data(475.45)["data"]["value"]
        assert value["amount"] == value["amountNet"] == 475.45

    def test_a_change_states_its_reason(self):
        data = contract_change_data("fiscalYearExtension")["data"]
        assert data["rationaleTypes"] == ["fiscalYearExtension"]
        assert data["rationale"]

    def test_a_change_is_signed_on_the_date_of_the_contract(self):
        data = contract_change_active_data(CONTRACT)["data"]
        assert data["dateSigned"] == CONTRACT["dateModified"]
        assert data["status"] == "active"

    def test_termination_states_what_was_paid(self):
        data = contract_terminated_data(900)["data"]
        assert data["amountPaid"]["amount"] == 900
        assert data["status"] == "terminated"
