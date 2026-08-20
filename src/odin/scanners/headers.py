"""HTTP security-header checks."""

import requests

from odin.config import ScanConfig
from odin.models import Finding


SECURITY_HEADERS = {
    "Content-Security-Policy": ("HDR-001", "medium"),
    "Strict-Transport-Security": ("HDR-002", "medium"),
    "X-Content-Type-Options": ("HDR-003", "low"),
    "X-Frame-Options": ("HDR-004", "low"),
    "Referrer-Policy": ("HDR-005", "low"),
    "Permissions-Policy": ("HDR-006", "low"),
}


def check_headers(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Return normalized findings for missing common security headers."""
    config = config or ScanConfig()
    response = requests.get(
        url,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent},
    )

    findings: list[Finding] = []
    for header, (finding_id, severity) in SECURITY_HEADERS.items():
        if header not in response.headers:
            findings.append(
                Finding(
                    id=finding_id,
                    title=f"Missing {header}",
                    severity=severity,
                    category="security-headers",
                    description=f"The response does not include the {header} header.",
                    target=url,
                    confidence="high",
                    remediation=f"Configure an appropriate {header} policy for the application.",
                    scanner="headers",
                )
            )
    return findings
