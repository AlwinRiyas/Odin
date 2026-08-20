"""Safety controls for explicitly enabled active checks."""

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ActiveScanPolicy:
    """Boundaries applied to active HTTP testing."""

    enabled: bool = False
    max_requests: int = 20
    min_interval: float = 0.25
    allow_http: bool = False


def validate_active_target(target: str, policy: ActiveScanPolicy) -> None:
    """Reject targets that violate the active-scan safety policy."""
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Active scans require a valid HTTP(S) target URL")
    if not policy.enabled:
        raise ValueError("Active scanning is disabled; enable it explicitly")
    if parsed.scheme == "http" and not policy.allow_http:
        raise ValueError("Active scans require HTTPS unless HTTP is explicitly allowed")
    if policy.max_requests < 1:
        raise ValueError("max_requests must be at least 1")
    if policy.min_interval < 0:
        raise ValueError("min_interval cannot be negative")
