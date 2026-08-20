from unittest.mock import Mock, patch

from odin.config import ScanConfig
from odin.scanners.cors import check_cors
from odin.scanners.disclosure import check_disclosure
from odin.scanners.headers import check_headers
from odin.scanners.http import check_http
from odin.scanners.methods import check_methods


def response(headers: dict[str, str] | None = None, url: str = "https://example.com/") -> Mock:
    item = Mock()
    item.headers = headers or {}
    item.url = url
    item.status_code = 200
    return item


@patch("odin.scanners.http.requests.get")
def test_http_flags_plain_http(mock_get: Mock) -> None:
    mock_get.return_value = response({"Server": "test"}, "http://example.com/")
    findings = check_http("http://example.com", ScanConfig())
    assert any(item.id == "HTTP-001" for item in findings)


@patch("odin.scanners.headers.requests.get")
def test_headers_report_missing_policy(mock_get: Mock) -> None:
    mock_get.return_value = response({})
    findings = check_headers("https://example.com", ScanConfig())
    assert any(item.id == "HDR-001" for item in findings)


@patch("odin.scanners.cors.requests.get")
def test_cors_flags_wildcard_credentials(mock_get: Mock) -> None:
    mock_get.return_value = response(
        {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )
    findings = check_cors("https://example.com", ScanConfig())
    assert any(item.id == "CORS-001" for item in findings)


@patch("odin.scanners.disclosure.requests.get")
def test_disclosure_detects_framework_header(mock_get: Mock) -> None:
    mock_get.return_value = response({"X-Powered-By": "Example"})
    findings = check_disclosure("https://example.com", ScanConfig())
    assert any(item.id == "DISC-001" for item in findings)


@patch("odin.scanners.methods.requests.request")
def test_methods_detects_accepted_method(mock_request: Mock) -> None:
    mock_request.return_value = response({})
    findings = check_methods("https://example.com", ScanConfig())
    assert len(findings) == 5
