from unittest.mock import patch

from odin.config import ScanConfig
from odin.engine import run_scan
from odin.models import Finding


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
    scanners = {
        "http": lambda target, config: [],
        "headers": lambda target, config: [],
        "cookies": lambda target, config: [],
        "cors": lambda target, config: [],
        "disclosure": lambda target, config: [],
    }

    with patch("odin.engine.check_status", return_value=status), patch(
        "odin.engine.SCANNERS", scanners
    ):
        result = run_scan("https://example.com", ScanConfig(), profile="baseline")

    assert result.status == 200
    assert result.target == "https://example.com"
    assert result.findings == []


def test_run_scan_normalizes_findings() -> None:
    status = {"status": 200, "final_url": "https://example.com/"}
    high = Finding(
        id="HIGH-001",
        title="High finding",
        severity="high",
        category="test",
        description="Example",
        target="https://example.com",
    )
    low = Finding(
        id="LOW-001",
        title="Low finding",
        severity="low",
        category="test",
        description="Example",
        target="https://example.com",
    )

    with patch("odin.engine.check_status", return_value=status), patch(
        "odin.engine.SCANNERS", {"test": lambda target, config: [low, high, high]}
    ), patch("odin.engine.PROFILES", {"test": ["test"]}):
        result = run_scan("https://example.com", ScanConfig(), profile="test")

    assert [finding.id for finding in result.findings] == ["HIGH-001", "LOW-001"]
    assert result.severity_counts["high"] == 1
    assert result.finding_count == 2
    assert result.to_dict()["finding_count"] == 2
