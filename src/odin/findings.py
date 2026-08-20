"""Validation and normalization helpers for scan findings."""

from collections.abc import Iterable

from odin.models import Finding

SEVERITIES = ("critical", "high", "medium", "low", "info")
CONFIDENCE_LEVELS = ("high", "medium", "low")


def validate_finding(finding: Finding) -> Finding:
    """Validate a finding before it enters a scan result."""
    if finding.severity not in SEVERITIES:
        raise ValueError(f"Invalid severity: {finding.severity}")
    if finding.confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"Invalid confidence: {finding.confidence}")
    if not finding.id.strip() or not finding.title.strip():
        raise ValueError("Finding id and title are required")
    return finding


def normalize_findings(findings: Iterable[Finding]) -> list[Finding]:
    """Validate, deduplicate, and deterministically order findings."""
    unique: dict[tuple[str, str], Finding] = {}
    for finding in findings:
        validate_finding(finding)
        key = (finding.id, finding.target)
        unique[key] = finding

    severity_order = {severity: index for index, severity in enumerate(SEVERITIES)}
    return sorted(
        unique.values(),
        key=lambda item: (severity_order[item.severity], item.category, item.id),
    )
