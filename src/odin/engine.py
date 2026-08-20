"""Scan orchestration engine."""

from dataclasses import dataclass
from typing import Callable

from odin.config import ScanConfig
from odin.models import Finding
from odin.scanners.basic import check_status
from odin.scanners.headers import check_headers

Scanner = Callable[[str, ScanConfig], list[Finding]]


@dataclass(slots=True)
class ScanResult:
    target: str
    status: int | None
    final_url: str | None
    findings: list[Finding]


SCANNERS: dict[str, Scanner] = {
    "headers": check_headers,
}

PROFILES: dict[str, list[str]] = {
    "quick": ["headers"],
    "baseline": ["headers"],
    "full": ["headers"],
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
) -> ScanResult:
    """Run selected scanner modules against a target."""
    config = config or ScanConfig()
    if profile not in PROFILES:
        raise ValueError(f"Unknown profile: {profile}")

    selected = modules if modules is not None else PROFILES[profile]
    unknown = sorted(set(selected) - set(SCANNERS))
    if unknown:
        raise ValueError(f"Unknown scanner module(s): {', '.join(unknown)}")

    basic = check_status(target, config)
    findings: list[Finding] = []
    for name in selected:
        findings.extend(SCANNERS[name](target, config))

    return ScanResult(
        target=target,
        status=int(basic["status"]),
        final_url=str(basic["final_url"]),
        findings=findings,
    )
