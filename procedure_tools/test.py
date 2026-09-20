import os
from unittest import mock

import pytest

from procedure_tools.main import main
from procedure_tools.utils.env import REQUIRED_ARGS, EnvFileNotFound, load_run_env

INACTIVE_REASON = "Currently inactive procedure"
skipinactive = pytest.mark.skip(reason=INACTIVE_REASON)

TEST_ENV = os.environ.get("PROCEDURE_ENV", "test")
SKIP_REQUIRED = REQUIRED_ARGS + (
    ("reviewer_token", "REVIEWER_TOKEN"),
    ("bot_token", "BOT_TOKEN"),
)


def _load_test_env():
    try:
        return load_run_env(TEST_ENV or None)
    except EnvFileNotFound:
        return None, {}


_ENV_FILE, _ENV_VALUES = _load_test_env()
_MISSING_ENV = [label for dest, label in SKIP_REQUIRED if not _ENV_VALUES.get(dest)]
if _ENV_FILE is None:
    _MISSING_ENV = [f"env file for {TEST_ENV!r} (copy .env.{TEST_ENV}.example to .env.{TEST_ENV})"]

skipifenv = pytest.mark.skipif(
    bool(_MISSING_ENV),
    reason=f"Env not specified: {', '.join(_MISSING_ENV)}",
)


def run_test(argv):
    args = ["--env", TEST_ENV]
    args.extend(argv)

    print("\n\nTest with args: %s\n\n" % (args))

    with mock.patch("sys.argv", [""] + args), pytest.raises(SystemExit) as e:
        main()

    assert e.type == SystemExit
    assert e.value.code == 0


def run_data(data_dir, fast_stop=None):
    argv = ["--data", data_dir]
    if fast_stop and os.environ.get("FAST_RUN"):
        argv += ["--stop", fast_stop]
    run_test(argv)


@skipifenv
def test_above_threshold():
    run_data("aboveThreshold", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_features():
    run_data("aboveThreshold.features", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_lcc():
    run_data("aboveThreshold.lcc", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_econtract():
    run_data("aboveThreshold.econtract", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_eu():
    run_data("aboveThresholdEU", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_eu_features():
    run_data("aboveThresholdEU.features", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_eu_lcc():
    run_data("aboveThresholdEU.lcc", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_eu_econtract():
    run_data("aboveThresholdEU.econtract", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_ua():
    run_data("aboveThresholdUA", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_ua_features():
    run_data("aboveThresholdUA.features", "tender_bid_patch_1.json")


@skipifenv
def test_above_threshold_ua_lcc():
    run_data("aboveThresholdUA.lcc", "tender_bid_patch_1.json")


@skipifenv
def test_below_threshold():
    run_data("belowThreshold", "tender_patch.json")


@skipifenv
def test_below_threshold_central():
    run_data("belowThreshold.central", "tender_patch.json")


@skipifenv
def test_below_threshold_features():
    run_data("belowThreshold.features", "tender_patch.json")


@skipifenv
def test_below_threshold_econtract():
    run_data("belowThreshold.econtract", "tender_bid_patch_1.json")


@skipifenv
def test_close_framework_agreement_ua():
    run_data("closeFrameworkAgreementUA", "tender_bid_patch_1.json")


@skipifenv
def test_close_framework_agreement_ua_central():
    run_data("closeFrameworkAgreementUA.central", "tender_bid_patch_1.json")


@skipifenv
def test_competitive_dialogue_eu():
    run_data("competitiveDialogueEU", "tender_bid_patch_1.json")


@skipifenv
def test_competitive_dialogue_ua():
    run_data("competitiveDialogueUA", "tender_bid_patch_1.json")


@skipifenv
def test_competitive_dialogue_ua_features():
    run_data("competitiveDialogueUA.features", "tender_bid_patch_1.json")


@skipifenv
def test_esco():
    run_data("esco", "tender_bid_patch_1.json")


@skipifenv
def test_esco_features():
    run_data("esco.features", "tender_bid_patch_1.json")


@skipifenv
def test_complex_asset_arma():
    run_data("complexAsset.arma", "tender_bid_patch_1.json")


@skipifenv
def test_negotiation():
    run_data("negotiation")


@skipifenv
def test_negotiation_local():
    run_data("negotiation.local")


@skipifenv
def test_negotiation_quick():
    run_data("negotiation.quick")


@skipifenv
def test_reporting():
    run_data("reporting")


@skipifenv
def test_reporting_local():
    run_data("reporting.local")


@skipifenv
def test_price_quotation():
    run_data("priceQuotation", "tender_bid_patch_1.json")


@skipinactive
@skipifenv
def test_simple_defense():
    run_data("simple.defense", "tender_bid_patch_1.json")


@skipifenv
def test_dynamic_purchasing_system_competitive_ordering_short():
    run_data("dynamicPurchasingSystem.competitiveOrdering.short", "tender_bid_patch_1.json")


@skipifenv
def test_dynamic_purchasing_system_competitive_ordering_long():
    run_data("dynamicPurchasingSystem.competitiveOrdering.long", "tender_bid_patch_1.json")


@skipifenv
def test_dynamic_purchasing_system_competitive_ordering_long_multi_sourcing():
    run_data("dynamicPurchasingSystem.competitiveOrdering.long.MultiSourcing", "tender_bid_patch_1.json")


@skipifenv
def test_request_for_proposal():
    run_data("requestForProposal", "tender_patch.json")


@skipifenv
def test_international_financial_institutions_request_for_proposal():
    run_data("internationalFinancialInstitutions.requestForProposal", "tender_patch.json")


def has_skipinactive_marker(test_func):
    marks = getattr(test_func, "pytestmark", [])
    return any(
        getattr(mark, "name", None) == "skip" and getattr(mark, "kwargs", {}).get("reason") == INACTIVE_REASON
        for mark in marks
    )


WORKFLOW_TEST_CASES = [  # pyright: ignore[reportUnusedVariable]
    name.removeprefix("test_")
    for name, test_func in globals().items()
    if name.startswith("test_") and callable(test_func) and not has_skipinactive_marker(test_func)
]
