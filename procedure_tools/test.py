import os
from unittest import mock

import pytest

from procedure_tools.main import main

API_HOST = "API_HOST"
API_TOKEN = "API_TOKEN"
DS_HOST = "DS_HOST"
DS_USERNAME = "DS_USERNAME"
DS_PASSWORD = "DS_PASSWORD"


REQUIRED_ENV_VARIABLES = [API_HOST, API_TOKEN, DS_HOST, DS_USERNAME, DS_PASSWORD]


skipifenv = pytest.mark.skipif(
    any([not os.environ.get(v) for v in REQUIRED_ENV_VARIABLES]),
    reason=f"One of {', '.join(REQUIRED_ENV_VARIABLES)} env variables not specified",
)


def run_test(argv):
    default_args = [
        "--acceleration",
        "10000",
        "--path",
        "/api/2.5/",
        "--submission",
        "quick(mode:no-auction)",
    ]
    args = (
        [
            os.environ.get(API_HOST),
            os.environ.get(API_TOKEN),
            os.environ.get(DS_HOST),
            os.environ.get(DS_USERNAME),
            os.environ.get(DS_PASSWORD),
        ]
        + default_args
        + argv
    )

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
def test_negotiation():
    argv = ["--data", "negotiation"]
    run_test(argv)


@skipifenv
def test_negotiation_quick():
    argv = ["--data", "negotiation.quick"]
    run_test(argv)


@skipifenv
def test_reporting():
    argv = ["--data", "reporting"]
    run_test(argv)


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
