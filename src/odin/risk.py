"""Risk scoring for normalized security findings.

This is an Odin risk score, not a CVSS score and must not be represented as CVSS.
"""

from dataclasses import dataclass

from odin.models import Finding

SEVERITY_WEIGHT = {
    "critical": 10.0,
    "high": 8.0,
    "medium": 5.0,
    "low": 2.5,
    "info": 0.0,
}

CONFIDENCE_FACTOR = {
    "high": 1.0,
    "medium": 0.75,
    "low": 0.5,
}


@dataclass(frozen=True, slots=True)
class RiskSummary:
    score: float
    rating: str
    finding_count: int
    severity_counts: dict[str, int]

    @property
    def is_failing(self) -> bool:
        return self.rating in {"critical", "high"}

    def to_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "rating": self.rating,
            "finding_count": self.finding_count,
            "severity_counts": dict(self.severity_counts),
        }


def _rating(score: float) -> str:
    if score >= 8:
        return "critical"
    if score >= 5:
        return "high"
    if score >= 2.5:
        return "medium"
    if score > 0:
        return "low"
    return "info"


def calculate_risk(findings: list[Finding]) -> RiskSummary:
    """Calculate a bounded 0-10 risk score from severity and confidence."""
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    raw = 0.0
    for finding in findings:
        counts[finding.severity] += 1
        raw += SEVERITY_WEIGHT[finding.severity] * CONFIDENCE_FACTOR[finding.confidence]

    # Prevent an unusually large number of low-severity findings from making
    # the score exceed the defined 0-10 scale.
    score = round(min(10.0, raw / max(1, len(findings))), 2) if findings else 0.0
    return RiskSummary(score, _rating(score), len(findings), counts)
