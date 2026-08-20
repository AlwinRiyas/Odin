from unittest.mock import Mock, patch

import pytest

from odin.config import ScanConfig
from odin.engine import run_scan


def _response() -> Mock:
    response = Mock()
    response.status_code = 200
    response.url = "https://example.com/"
    response.headers = {}
    response.text = ""
    return response


@patch("odin.scanners.basic.requests.get")
@patch("odin.scanners.headers.requests.get")
@patch("odin.scanners.http.requests.get")
def test_quick_profile_completes_with_mocked_http(mock_http, mock_headers, mock_basic) -> None:
    mock_http.return_value = _response()
    mock_headers.return_value = _response()
    mock_basic.return_value = _response()

    result = run_scan("https://example.com", ScanConfig(), profile="quick")
    assert result.status == 200
    assert result.final_url == "https://example.com/"
    assert result.risk.score >= 0


def test_unknown_profile_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown profile"):
        run_scan("https://example.com", profile="does-not-exist")


def test_unknown_module_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown scanner module"):
        run_scan("https://example.com", modules=["does-not-exist"])
