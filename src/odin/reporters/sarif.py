"""SARIF 2.1.0 serialization for security findings."""

import json

from odin.engine import ScanResult


_LEVELS = {
    "critical": "error",
    "high": "error",
    "medium": "warning",
    "low": "note",
    "info": "note",
}


def serialize(result: ScanResult, indent: int = 2) -> str:
    """Serialize findings into a SARIF 2.1.0 document."""
    rules = []
    rule_ids = set()
    results = []
    for finding in result.findings:
        if finding.id not in rule_ids:
            rule_ids.add(finding.id)
            rules.append(
                {
                    "id": finding.id,
                    "name": finding.title,
                    "shortDescription": {"text": finding.description},
                    "help": {"text": finding.remediation or "Review and remediate the finding."},
                }
            )
        results.append(
            {
                "ruleId": finding.id,
                "level": _LEVELS[finding.severity],
                "message": {"text": finding.description},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": result.target}}}],
            }
        )

    document = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "Odin", "rules": rules}},
                "results": results,
            }
        ],
    }
    return json.dumps(document, indent=indent)
