"""HTTP transport and response-security checks."""

from urllib.parse import urlparse

import requests

from odin.config import ScanConfig
from odin.models import Finding


def check_http(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Check transport behavior and basic response metadata."""
    config = config or ScanConfig()
    response = requests.get(
        url,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent},
        allow_redirects=True,
    )
    findings: list[Finding] = []
    parsed = urlparse(url)

    if parsed.scheme == "http":
        findings.append(
            Finding(
                id="HTTP-001",
                title="Target uses HTTP instead of HTTPS",
                severity="medium",
                category="transport-security",
                description="The supplied target uses an unencrypted HTTP URL.",
                target=url,
                confidence="high",
                evidence=f"Initial scheme: {parsed.scheme}",
                remediation=(
                    "Use HTTPS for sensitive application traffic and redirect HTTP "
                    "to HTTPS."
                ),
                scanner="http",
            )
        )

    server = response.headers.get("Server")
    if server:
        findings.append(
            Finding(
                id="HTTP-002",
                title="Server header discloses implementation details",
                severity="low",
                category="information-disclosure",
                description=(
                    "The response exposes a Server header that may reveal server "
                    "technology."
                ),
                target=url,
                confidence="high",
                evidence=f"Server: {server}",
                remediation="Consider minimizing unnecessary server identification information.",
                scanner="http",
            )
        )

    return findings
