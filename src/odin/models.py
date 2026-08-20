"""Core data models used by the scanner engine."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Finding:
    """A normalized security finding produced by a scanner module."""

    id: str
    title: str
    severity: str
    category: str
    description: str
    target: str
    confidence: str = "medium"
    evidence: str | None = None
    remediation: str | None = None
    references: list[str] = field(default_factory=list)
    scanner: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the finding for reporters and integrations."""
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity,
            "category": self.category,
            "description": self.description,
            "target": self.target,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "references": list(self.references),
            "scanner": self.scanner,
            "metadata": dict(self.metadata),
        }
