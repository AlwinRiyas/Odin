import json
from pathlib import Path

from odin import __version__
from odin.engine import ScanResult
from odin.models import Finding
from odin.reporters.html import render_html
from odin.reporters.sarif import serialize as serialize_sarif
from odin.risk import calculate_risk


ROOT = Path(__file__).resolve().parents[1]


def make_result() -> ScanResult:
    finding = Finding(
        id="REL-001",
        title="Release contract test",
        severity="low",
        category="test",
        description="Release verification finding",
        target="https://example.com",
        confidence="high",
        remediation="No action required",
    )
    return ScanResult(
        target="https://example.com",
        status=200,
        final_url="https://example.com/",
        findings=[finding],
        risk=calculate_risk([finding]),
    )


def test_version_is_consistent() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version = "{__version__}"' in pyproject


def test_release_artifacts_exist() -> None:
    assert (ROOT / "LICENSE").is_file()
    assert (ROOT / ".github/workflows/ci.yml").is_file()
    assert (ROOT / ".github/workflows/release.yml").is_file()
    assert (ROOT / ".github/workflows/publish.yml").is_file()


def test_sarif_is_valid_json() -> None:
    document = json.loads(serialize_sarif(make_result()))
    assert document["version"] == "2.1.0"
    assert document["runs"][0]["tool"]["driver"]["name"] == "Odin"


def test_html_is_standalone_document() -> None:
    document = render_html(make_result())
    assert document.startswith("<!doctype html>")
    assert "Release contract test" in document
