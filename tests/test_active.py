import pytest

from odin.active import ActiveScanPolicy, validate_active_target


def test_active_scan_is_disabled_by_default() -> None:
    with pytest.raises(ValueError, match="disabled"):
        validate_active_target("https://example.com/?q=test", ActiveScanPolicy())


def test_active_scan_requires_https_by_default() -> None:
    policy = ActiveScanPolicy(enabled=True)
    with pytest.raises(ValueError, match="HTTPS"):
        validate_active_target("http://example.com/?q=test", policy)


def test_active_scan_accepts_explicit_https_policy() -> None:
    validate_active_target(
        "https://example.com/?q=test",
        ActiveScanPolicy(enabled=True, max_requests=5, min_interval=0.1),
    )
