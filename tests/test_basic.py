from unittest.mock import Mock, patch

from odin.config import ScanConfig
from odin.scanners.basic import check_status


@patch("odin.scanners.basic.requests.get")
def test_check_status(mock_get: Mock) -> None:
    response = Mock()
    response.status_code = 200
    response.headers = {"Server": "test", "Content-Type": "text/html"}
    response.url = "https://example.com/"
    mock_get.return_value = response

    result = check_status("https://example.com", ScanConfig())

    assert result["status"] == 200
    assert result["server"] == "test"
    mock_get.assert_called_once()
