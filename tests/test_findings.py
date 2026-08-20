import pytest

from odin.findings import normalize_findings, validate_finding
from odin.models import Finding


def make_finding(finding_id: str, severity: str = "low") -> Finding:
    return Finding(
        id=finding_id,
        title="Test finding",
        severity=severity,
        category="test",
        description="Test description",
        target="https://example.com",
    )


def test_invalid_severity_is_rejected() -> None:
    with pytest.raises(ValueError, match="Invalid severity"):
        validate_finding(make_finding("TEST-001", "unknown"))


def test_invalid_confidence_is_rejected() -> None:
    finding = make_finding("TEST-001")
    finding.confidence = "unknown"
    with pytest.raises(ValueError, match="Invalid confidence"):
        validate_finding(finding)


def test_findings_are_deduplicated_and_sorted_by_severity() -> None:
    findings = normalize_findings(
        [
            make_finding("LOW-001", "low"),
            make_finding("HIGH-001", "high"),
            make_finding("HIGH-001", "high"),
        ]
    )

    assert [item.id for item in findings] == ["HIGH-001", "LOW-001"]


def test_finding_serializes_to_dict() -> None:
    finding = make_finding("TEST-001")
    data = finding.to_dict()

    assert data["id"] == "TEST-001"
    assert data["severity"] == "low"
    assert data["references"] == []
