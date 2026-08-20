from unittest.mock import patch

from odin.config import ScanConfig
from odin.engine import run_scan


def test_profile_validation() -> None:
    with patch("odin.engine.check_status"):
        try:
            run_scan("https://example.com", ScanConfig(), profile="missing")
        except ValueError as exc:
            assert "Unknown profile" in str(exc)
        else:
            raise AssertionError("Expected invalid profile to fail")


def test_run_scan_uses_baseline_profile() -> None:
    status = {"status": 200, "final_url": "https://example.com/"}
    with patch("odin.engine.check_status", return_value=status), patch(
        "odin.engine.check_headers", return_value=[]
    ):
        result = run_scan("https://example.com", ScanConfig(), profile="baseline")

    assert result.status == 200
    assert result.target == "https://example.com"
    assert result.findings == []
