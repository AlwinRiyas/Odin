import json

import pytest

from odin.settings import load_config


def test_load_config(tmp_path) -> None:
    path = tmp_path / "odin.json"
    path.write_text(
        json.dumps(
            {
                "profile": "full",
                "output": "json",
                "fail_on": "high",
                "scan": {"timeout": 15, "retries": 2, "verify_tls": True},
                "modules": ["headers", "tls"],
                "active": {"enabled": False, "max_requests": 10, "min_interval": 0.5},
            }
        ),
        encoding="utf-8",
    )

    config = load_config(path)
    assert config.profile == "full"
    assert config.output == "json"
    assert config.scan.timeout == 15
    assert config.modules == ["headers", "tls"]
    assert config.active.max_requests == 10


def test_invalid_config_is_rejected(tmp_path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"scan": {"timeout": 0}}), encoding="utf-8")
    with pytest.raises(ValueError, match="scan.timeout"):
        load_config(path)
