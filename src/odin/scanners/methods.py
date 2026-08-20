"""HTTP method exposure checks."""

import requests

from odin.config import ScanConfig
from odin.models import Finding

METHODS = ("OPTIONS", "TRACE", "PUT", "DELETE", "CONNECT")


def check_methods(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Probe potentially unnecessary HTTP methods with low-impact requests."""
    config = config or ScanConfig()
    findings: list[Finding] = []

    for method in METHODS:
        response = requests.request(
            method,
            url,
            timeout=config.timeout,
            verify=config.verify_tls,
            headers={"User-Agent": config.user_agent},
        )
        if response.status_code < 400:
            severity = "medium" if method in {"TRACE", "CONNECT"} else "low"
            findings.append(
                Finding(
                    id=f"METHOD-{method}",
                    title=f"HTTP method {method} accepted",
                    severity=severity,
                    category="http-methods",
                    description=(
                        "The target accepted a potentially unnecessary HTTP method."
                    ),
                    target=url,
                    confidence="medium",
                    evidence=f"{method} returned HTTP {response.status_code}.",
                    remediation=(
                        "Disable HTTP methods that are not required by the application "
                        "or infrastructure."
                    ),
                    scanner="methods",
                )
            )

    return findings
