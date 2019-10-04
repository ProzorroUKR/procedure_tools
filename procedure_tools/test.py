import pytest

try:
    from unittest import mock
except ImportError:
    import mock
import os

from procedure_tools.procedure import main


@pytest.mark.skipif(
    not os.environ.get("HOST") or not os.environ.get("TOKEN"), reason="Either HOST or TOKEN env variables not specified"
)
@pytest.mark.parametrize(
    "argv",
    [
        (["--data", "reporting"]),
        (["--data", "negotiation", "--stop", "tender_create.json"]),
        (["--data", "negotiation.quick", "--stop", "tender_create.json"]),
        (["--data", "belowThreshold", "--stop", "tender_create.json"]),
        (["--data", "aboveThresholdEU", "--stop", "tender_create.json"]),
        (["--data", "aboveThresholdEU.multilot", "--stop", "tender_create.json"]),
        (["--data", "aboveThresholdUA", "--stop", "tender_create.json"]),
        (["--data", "aboveThresholdUA.defense", "--stop", "tender_create.json"]),
        (["--data", "closeFrameworkAgreementUA", "--stop", "tender_create.json"]),
        (["--data", "competitiveDialogueEU", "--stop", "tender_create.json"]),
        (["--data", "competitiveDialogueUA", "--stop", "tender_create.json"]),
        (["--data", "esco", "--stop", "tender_create.json"]),
        (["--wait", "edr-qualification"]),
    ],
)
def test_main(argv):
    host = os.environ.get("HOST")
    token = os.environ.get("TOKEN")

    default_args = ["--acceleration", "1000000", "--path", "/api/2.5/"]

    print("\n\nTest with args: %s\n\n" % ([host, "*" * 32] + default_args + argv))

    with mock.patch("sys.argv", ["", host, token] + default_args + argv), pytest.raises(SystemExit) as e:
        main()
    assert e.type == SystemExit
    assert e.value.code == 0
