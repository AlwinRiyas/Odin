import pytest

from odin.active import ActiveScanPolicy
from odin.engine import run_scan


def test_active_module_count_respects_request_budget() -> None:
    with pytest.raises(ValueError, match="request budget"):
        run_scan(
            "https://example.com/?q=test",
            modules=["active_xss", "active_sqli"],
            active_policy=ActiveScanPolicy(enabled=True, max_requests=1),
        )
