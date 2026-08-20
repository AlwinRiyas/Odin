"""TLS certificate and transport checks."""

import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse

from odin.config import ScanConfig
from odin.models import Finding


def check_tls(url: str, config: ScanConfig | None = None) -> list[Finding]:
    """Inspect the TLS certificate for HTTPS targets."""
    config = config or ScanConfig()
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return []

    host = parsed.hostname
    if not host:
        return []
    port = parsed.port or 443

    context = ssl.create_default_context()
    context.check_hostname = config.verify_tls
    context.verify_mode = ssl.CERT_REQUIRED if config.verify_tls else ssl.CERT_NONE

    try:
        with socket.create_connection((host, port), timeout=config.timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as tls_sock:
                certificate = tls_sock.getpeercert()
    except (OSError, ssl.SSLError) as exc:
        return [
            Finding(
                id="TLS-001",
                title="TLS connection could not be validated",
                severity="high" if config.verify_tls else "medium",
                category="tls",
                description=(
                    "The TLS certificate or connection could not be validated with "
                    "the configured policy."
                ),
                target=url,
                confidence="high",
                evidence=str(exc),
                remediation=(
                    "Use a valid certificate matching the hostname and a trusted "
                    "certificate chain."
                ),
                scanner="tls",
            )
        ]

    findings: list[Finding] = []
    not_after = certificate.get("notAfter")
    if not_after:
        expires = datetime.strptime(
            not_after, "%b %d %H:%M:%S %Y %Z"
        ).replace(tzinfo=timezone.utc)
        remaining_days = (expires - datetime.now(timezone.utc)).days
        if remaining_days < 0:
            findings.append(
                Finding(
                    id="TLS-002",
                    title="TLS certificate is expired",
                    severity="high",
                    category="tls",
                    description="The server certificate is past its validity period.",
                    target=url,
                    confidence="high",
                    evidence=f"Certificate expiration: {expires.isoformat()}",
                    remediation="Renew the certificate and deploy the valid certificate chain.",
                    scanner="tls",
                )
            )
        elif remaining_days <= 30:
            findings.append(
                Finding(
                    id="TLS-003",
                    title="TLS certificate expires soon",
                    severity="low",
                    category="tls",
                    description=(
                        "The certificate has 30 or fewer days remaining before expiration."
                    ),
                    target=url,
                    confidence="high",
                    evidence=f"Days remaining: {remaining_days}",
                    remediation="Renew the certificate before it expires.",
                    scanner="tls",
                )
            )

    return findings
