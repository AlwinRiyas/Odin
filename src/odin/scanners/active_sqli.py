"""Opt-in, non-destructive SQL-error indicator check.

Only a single quote is appended to the first query parameter. The scanner
reports database-error indicators as a lead, not as proof of SQL injection.
"""

import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

from odin.active import ActiveScanPolicy, validate_active_target
from odin.config import ScanConfig
from odin.models import Finding

SQL_ERROR_MARKERS = (
    "sql syntax",
    "mysql",
    "postgresql",
    "sqlite error",
    "ora-",
    "odbc",
)


def _with_quote(url: str) -> str:
    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True)
    if not query:
        return url
    key, value = query[0]
    query[0] = (key, f"{value}'")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def check_sql_errors(url: str, config: ScanConfig | None = None, policy: ActiveScanPolicy | None = None) -> list[Finding]:
    """Check for obvious database error disclosure after one benign perturbation."""
    config = config or ScanConfig()
    policy = policy or ActiveScanPolicy()
    validate_active_target(url, policy)

    target = _with_quote(url)
    if target == url:
        return []

    response = requests.get(
        target,
        timeout=config.timeout,
        verify=config.verify_tls,
        headers={"User-Agent": config.user_agent},
    )
    time.sleep(policy.min_interval)
    body = response.text.lower()
    matches = [marker for marker in SQL_ERROR_MARKERS if marker in body]

    if not matches:
        return []

    return [
        Finding(
            id="SQLI-001",
            title="Database error indicator exposed after input perturbation",
            severity="medium",
            category="sqli",
            description="A database error indicator appeared after a single benign input perturbation. This is an indicator, not proof of SQL injection.",
            target=url,
            confidence="low",
            evidence=f"Matched indicators: {', '.join(matches)}",
            remediation="Use parameterized queries and avoid exposing database error details to clients.",
            scanner="active_sqli",
        )
    ]
