"""Cookie security checks."""

import requests

from odin.config import ScanConfig
from odin.models import Finding


def check_cookies(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Check Set-Cookie attributes visible in the response."""
    config = config or ScanConfig()
    response = requests.get(
        url,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent},
    )
    findings: list[Finding] = []

    for raw_cookie in response.raw.headers.getlist("Set-Cookie"):
        parts = [part.strip() for part in raw_cookie.split(";")]
        name = parts[0].split("=", 1)[0].strip() or "unknown"
        attributes = {part.split("=", 1)[0].strip().lower() for part in parts[1:]}

        if "secure" not in attributes and response.url.startswith("https://"):
            findings.append(
                Finding(
                    id="COOKIE-001",
                    title=f"Cookie '{name}' missing Secure attribute",
                    severity="medium",
                    category="cookie-security",
                    description="A cookie delivered over HTTPS does not declare Secure.",
                    target=url,
                    confidence="high",
                    evidence=raw_cookie,
                    remediation="Set the Secure attribute for cookies that must only travel over HTTPS.",
                    scanner="cookies",
                )
            )

        if "httponly" not in attributes:
            findings.append(
                Finding(
                    id="COOKIE-002",
                    title=f"Cookie '{name}' missing HttpOnly attribute",
                    severity="medium",
                    category="cookie-security",
                    description="The cookie does not declare HttpOnly, allowing client-side scripts to access it.",
                    target=url,
                    confidence="high",
                    evidence=raw_cookie,
                    remediation="Use HttpOnly for cookies that do not need JavaScript access.",
                    scanner="cookies",
                )
            )

        if "samesite" not in attributes:
            findings.append(
                Finding(
                    id="COOKIE-003",
                    title=f"Cookie '{name}' missing SameSite attribute",
                    severity="low",
                    category="cookie-security",
                    description="The cookie does not explicitly declare a SameSite policy.",
                    target=url,
                    confidence="medium",
                    evidence=raw_cookie,
                    remediation="Set an appropriate SameSite policy based on the application's cross-site requirements.",
                    scanner="cookies",
                )
            )

    return findings
