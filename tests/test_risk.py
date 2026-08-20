from odin.models import Finding
from odin.risk import calculate_risk


def finding(severity: str, confidence: str = "high") -> Finding:
    return Finding(
        id=f"TEST-{severity}",
        title="Test",
        severity=severity,
        category="test",
        description="Test",
        target="https://example.com",
        confidence=confidence,
    )


def test_no_findings_have_zero_risk() -> None:
    summary = calculate_risk([])
    assert summary.score == 0.0
    assert summary.rating == "info"


def test_high_confidence_high_finding_is_high_risk() -> None:
    summary = calculate_risk([finding("high")])
    assert summary.score == 8.0
    assert summary.rating == "critical"


def test_low_confidence_reduces_score() -> None:
    summary = calculate_risk([finding("high", "low")])
    assert summary.score == 4.0
    assert summary.rating == "medium"
