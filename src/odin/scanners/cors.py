"""CORS configuration checks."""

import requests

from odin.config import ScanConfig
from odin.models import Finding


def check_cors(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Check for potentially dangerous CORS response configurations."""
    config = config or ScanConfig()
    response = requests.get(
        url,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent, "Origin": "https://odin.invalid"},
    )
    findings: list[Finding] = []
    allow_origin = response.headers.get("Access-Control-Allow-Origin", "")
    allow_credentials = response.headers.get("Access-Control-Allow-Credentials", "").lower()

    if allow_origin == "*" and allow_credentials == "true":
        findings.append(
            Finding(
                id="CORS-001",
                title="Wildcard CORS origin combined with credentials",
                severity="high",
                category="cors",
                description="The response permits all origins while also enabling credentials.",
                target=url,
                confidence="high",
                evidence=(
                    "Access-Control-Allow-Origin: *; "
                    "Access-Control-Allow-Credentials: true"
                ),
                remediation=(
                    "Restrict allowed origins to trusted origins and only enable "
                    "credentials when required."
                ),
                scanner="cors",
            )
        )
    elif allow_origin == "*":
        findings.append(
            Finding(
                id="CORS-002",
                title="Wildcard CORS origin",
                severity="low",
                category="cors",
                description="The response permits requests from any origin.",
                target=url,
                confidence="high",
                evidence="Access-Control-Allow-Origin: *",
                remediation=(
                    "Use an explicit allowlist when the application does not need "
                    "to be publicly embeddable."
                ),
                scanner="cors",
            )
        )

    return findings
