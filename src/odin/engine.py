"""Scan orchestration engine."""

from dataclasses import dataclass
from typing import Callable

from odin.active import ActiveScanPolicy
from odin.config import ScanConfig
from odin.findings import normalize_findings
from odin.models import Finding
from odin.scanners.active_sqli import check_sql_errors
from odin.scanners.active_xss import check_reflection
from odin.scanners.basic import check_status
from odin.scanners.cookies import check_cookies
from odin.scanners.cors import check_cors
from odin.scanners.disclosure import check_disclosure
from odin.scanners.headers import check_headers
from odin.scanners.http import check_http
from odin.scanners.methods import check_methods
from odin.scanners.tls import check_tls

Scanner = Callable[[str, ScanConfig], list[Finding]]


@dataclass(slots=True)
class ScanResult:
    target: str
    status: int | None
    final_url: str | None
    findings: list[Finding]

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    @property
    def severity_counts(self) -> dict[str, int]:
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for finding in self.findings:
            counts[finding.severity] += 1
        return counts

    def to_dict(self) -> dict[str, object]:
        return {
            "target": self.target,
            "status": self.status,
            "final_url": self.final_url,
            "finding_count": self.finding_count,
            "severity_counts": self.severity_counts,
            "findings": [finding.to_dict() for finding in self.findings],
        }


SCANNERS: dict[str, Scanner] = {
    "http": check_http,
    "headers": check_headers,
    "cookies": check_cookies,
    "cors": check_cors,
    "tls": check_tls,
    "methods": check_methods,
    "disclosure": check_disclosure,
}

PROFILES: dict[str, list[str]] = {
    "quick": ["http", "headers"],
    "baseline": ["http", "headers", "cookies", "cors", "disclosure"],
    "full": ["http", "headers", "cookies", "cors", "tls", "methods", "disclosure"],
}


def available_scanners() -> list[str]:
    return sorted(SCANNERS)


def available_profiles() -> list[str]:
    return sorted(PROFILES)


def run_scan(
    target: str,
    config: ScanConfig | None = None,
    profile: str = "baseline",
    modules: list[str] | None = None,
    active_policy: ActiveScanPolicy | None = None,
) -> ScanResult:
    """Run passive modules, with active checks available only by explicit module selection."""
    config = config or ScanConfig()
    if profile not in PROFILES:
        raise ValueError(f"Unknown profile: {profile}")

    selected = modules if modules is not None else PROFILES[profile]
    active_modules = {"active_xss", "active_sqli"}
    if active_modules.intersection(selected):
        policy = active_policy or ActiveScanPolicy()
        if not policy.enabled:
            raise ValueError("Active modules require an explicitly enabled active-scan policy")
    else:
        policy = active_policy or ActiveScanPolicy()

    registry: dict[str, Callable[..., list[Finding]]] = {
        **SCANNERS,
        "active_xss": lambda target, cfg: check_reflection(target, cfg, policy),
        "active_sqli": lambda target, cfg: check_sql_errors(target, cfg, policy),
    }
    unknown = sorted(set(selected) - set(registry))
    if unknown:
        raise ValueError(f"Unknown scanner module(s): {', '.join(unknown)}")

    basic = check_status(target, config)
    findings: list[Finding] = []
    for name in selected:
        findings.extend(registry[name](target, config))

    return ScanResult(
        target=target,
        status=int(basic["status"]),
        final_url=str(basic["final_url"]),
        findings=normalize_findings(findings),
    )
