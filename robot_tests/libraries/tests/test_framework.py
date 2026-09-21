"""Framework payloads."""

from data.framework import (
    FRAMEWORK_CONFIG,
    framework_config_data,
    framework_data,
    framework_patch_data,
    framework_procuring_entity_data,
)


class TestFrameworkProcuringEntity:
    def test_can_be_reached_both_ways(self):
        # a framework requires the email, unlike a tender procuring entity
        contact = framework_procuring_entity_data()["contactPoint"]
        assert contact["email"]
        assert contact["url"]

    def test_is_a_special_kind_of_buyer(self):
        assert framework_procuring_entity_data()["kind"] == "special"


class TestFrameworkData:
    def test_is_a_dynamic_purchasing_system_by_default(self):
        assert framework_data()["data"]["frameworkType"] == "dynamicPurchasingSystem"

    def test_carries_the_config_block(self):
        assert framework_data()["config"] == FRAMEWORK_CONFIG

    def test_config_options_can_be_changed_one_at_a_time(self):
        config = framework_config_data(restrictedDerivatives=True)
        assert config["restrictedDerivatives"] is True
        assert config["hasItems"] == FRAMEWORK_CONFIG["hasItems"]

    def test_acceleration_shortens_the_qualification_period_instead_of_being_sent(self):
        payload = framework_data(acceleration=460800)
        assert "acceleration" not in payload["data"]
        assert payload["data"]["frameworkDetails"] == "quick, accelerator=460800"

    def test_qualification_is_open_for_a_period(self):
        assert framework_data()["data"]["qualificationPeriod"]["endDate"]

    def test_patch_names_the_target_status(self):
        assert framework_patch_data("active") == {"data": {"status": "active"}}
