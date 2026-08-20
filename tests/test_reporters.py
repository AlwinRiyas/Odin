import json

from odin.engine import ScanResult
from odin.models import Finding
from odin.reporters.html import render_html
from odin.reporters.json import serialize as serialize_json
from odin.reporters.sarif import serialize as serialize_sarif
from odin.risk import calculate_risk


def result() -> ScanResult:
    finding = Finding(
        id="TEST-001",
        title="Example finding",
        severity="medium",
        category="test",
        description="Example description",
        target="https://example.com",
        remediation="Example remediation",
    )
    return ScanResult(
        target="https://example.com",
        status=200,
        final_url="https://example.com/",
        findings=[finding],
        risk=calculate_risk([finding]),
    )


def test_json_contains_risk() -> None:
    data = json.loads(serialize_json(result()))
    assert "risk" in data
    assert data["finding_count"] == 1


def test_html_escapes_finding_content() -> None:
    report = render_html(result())
    assert "Odin Security Report" in report
    assert "Example finding" in report


def test_sarif_has_expected_version_and_results() -> None:
    data = json.loads(serialize_sarif(result()))
    assert data["version"] == "2.1.0"
    assert len(data["runs"][0]["results"]) == 1
