"""Common information-disclosure checks."""

import requests

from odin.config import ScanConfig
from odin.models import Finding


DISCLOSURE_HEADERS = {
    "X-Powered-By": ("DISC-001", "low"),
    "X-AspNet-Version": ("DISC-002", "low"),
    "X-AspNetMvc-Version": ("DISC-003", "low"),
}


def check_disclosure(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Detect common framework/version disclosure headers."""
    config = config or ScanConfig()
    response = requests.get(
        url,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent},
    )
    findings: list[Finding] = []

    for header, (finding_id, severity) in DISCLOSURE_HEADERS.items():
        value = response.headers.get(header)
        if value:
            findings.append(
                Finding(
                    id=finding_id,
                    title=f"{header} discloses implementation information",
                    severity=severity,
                    category="information-disclosure",
                    description="The response exposes a framework or implementation-identifying header.",
                    target=url,
                    confidence="high",
                    evidence=f"{header}: {value}",
                    remediation="Remove or minimize unnecessary framework and version disclosure headers.",
                    scanner="disclosure",
                )
            )

    return findings
