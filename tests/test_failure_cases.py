from unittest.mock import Mock, patch

import requests

from odin.config import ScanConfig
from odin.scanners.tls import check_tls


@patch("odin.scanners.tls.socket.create_connection", side_effect=OSError("connection refused"))
def test_tls_connection_failure_becomes_finding(mock_connection) -> None:
    findings = check_tls("https://example.com", ScanConfig())
    assert any(item.id == "TLS-001" for item in findings)


def test_scan_config_has_secure_defaults() -> None:
    config = ScanConfig()
    assert config.verify_tls is True
    assert config.timeout >= 1
