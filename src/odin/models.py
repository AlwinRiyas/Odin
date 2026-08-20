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
