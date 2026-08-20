"""Opt-in, low-volume reflected-XSS indicator check.

This module intentionally performs only a single benign marker request. It does
not execute JavaScript or attempt persistence, authentication bypass, or
exploit chaining.
"""

import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

from odin.active import ActiveScanPolicy, validate_active_target
from odin.config import ScanConfig
from odin.models import Finding

MARKER = "odin-xss-marker-7f3a"


def _with_marker(url: str) -> str:
    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True)
    if not query:
        return url
    key, _ = query[0]
    query[0] = (key, MARKER)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def check_reflection(url: str, config: ScanConfig | None = None, policy: ActiveScanPolicy | None = None) -> list[Finding]:
    """Look for a benign marker reflected into an HTML response."""
    config = config or ScanConfig()
    policy = policy or ActiveScanPolicy()
    validate_active_target(url, policy)

    target = _with_marker(url)
    if target == url:
        return []

    response = requests.get(
        target,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent},
    )
    time.sleep(policy.min_interval)

    if MARKER not in response.text:
        return []

    return [
        Finding(
            id="XSS-001",
            title="User-controlled query marker reflected in response",
            severity="medium",
            category="xss",
            description="A benign marker inserted into a query parameter was reflected in the response body. Reflection alone does not prove executable XSS.",
            target=url,
            confidence="low",
            evidence=f"Marker '{MARKER}' was found in the response body.",
            remediation="Contextually encode untrusted output and apply an appropriate Content Security Policy.",
            scanner="active_xss",
        )
    ]
