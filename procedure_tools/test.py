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


@skipifenv
def test_above_threshold():
    argv = ["--data", "aboveThreshold"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_features():
    argv = ["--data", "aboveThreshold.features"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_lcc():
    argv = ["--data", "aboveThreshold.lcc"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_econtract():
    argv = ["--data", "aboveThreshold.econtract"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_eu():
    argv = ["--data", "aboveThresholdEU"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_eu_features():
    argv = ["--data", "aboveThresholdEU.features"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_eu_lcc():
    argv = ["--data", "aboveThresholdEU.lcc"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_eu_econtract():
    argv = ["--data", "aboveThresholdEU.econtract"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_ua():
    argv = ["--data", "aboveThresholdUA"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_ua_features():
    argv = ["--data", "aboveThresholdUA.features"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_above_threshold_ua_lcc():
    argv = ["--data", "aboveThresholdUA.lcc"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_below_threshold():
    argv = ["--data", "belowThreshold"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "tender_patch.json"]
    run_test(argv)


@skipifenv
def test_below_threshold_central():
    argv = ["--data", "belowThreshold.central"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "tender_patch.json"]
    run_test(argv)


@skipifenv
def test_below_threshold_features():
    argv = ["--data", "belowThreshold.features"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "tender_patch.json"]
    run_test(argv)


@skipifenv
def test_below_threshold_econtract():
    argv = ["--data", "belowThreshold.econtract"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_close_framework_agreement_ua():
    argv = ["--data", "closeFrameworkAgreementUA"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_close_framework_agreement_ua_central():
    argv = ["--data", "closeFrameworkAgreementUA.central"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_competitive_dialogue_eu():
    argv = ["--data", "competitiveDialogueEU"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_competitive_dialogue_ua():
    argv = ["--data", "competitiveDialogueUA"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_competitive_dialogue_ua_features():
    argv = ["--data", "competitiveDialogueUA.features"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_esco():
    argv = ["--data", "esco"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_esco_features():
    argv = ["--data", "esco.features"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_complex_asset_arma():
    argv = ["--data", "complexAsset.arma"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipinactive
@skipifenv
def test_negotiation():
    argv = ["--data", "negotiation"]
    run_test(argv)


@skipinactive
@skipifenv
def test_negotiation_quick():
    argv = ["--data", "negotiation.quick"]
    run_test(argv)


@skipifenv
def test_reporting():
    argv = ["--data", "reporting"]
    run_test(argv)


@skipifenv
def test_price_quotation():
    argv = ["--data", "priceQuotation"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipinactive
@skipifenv
def test_simple_defense():
    argv = ["--data", "simple.defense"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_dynamic_purchasing_system_competitive_ordering_short():
    argv = ["--data", "dynamicPurchasingSystem.competitiveOrdering.short"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_dynamic_purchasing_system_competitive_ordering_long():
    argv = ["--data", "dynamicPurchasingSystem.competitiveOrdering.long"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_dynamic_purchasing_system_competitive_ordering_long_multi_sourcing():
    argv = ["--data", "dynamicPurchasingSystem.competitiveOrdering.long.MultiSourcing"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "bid_patch_1.json"]
    run_test(argv)


@skipifenv
def test_request_for_proposal():
    argv = ["--data", "requestForProposal"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "tender_patch.json"]
    run_test(argv)


@skipifenv
def test_international_financial_institutions_request_for_proposal():
    argv = ["--data", "internationalFinancialInstitutions.requestForProposal"]
    if os.environ.get("FAST_RUN"):
        argv += ["--stop", "tender_patch.json"]
    run_test(argv)


def has_skipinactive_marker(test_func):
    marks = getattr(test_func, "pytestmark", [])
    return any(
        all(
            (
                getattr(mark, "name", None) == "skip",
                getattr(mark, "kwargs", {}).get("reason") == INACTIVE_REASON,
            )
        )
        for mark in marks
    )


WORKFLOW_TEST_CASES = [  # pyright: ignore[reportUnusedVariable]
    name.removeprefix("test_")
    for name, test_func in globals().items()
    if all(
        (
            name.startswith("test_"),
            callable(test_func),
            not has_skipinactive_marker(test_func),
        )
    )
]
