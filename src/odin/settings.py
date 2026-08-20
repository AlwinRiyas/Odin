"""File-backed configuration for repeatable scans."""

from dataclasses import dataclass, field
from pathlib import Path

import json

from odin.active import ActiveScanPolicy
from odin.config import ScanConfig


@dataclass(slots=True)
class ProjectConfig:
    """Validated project-level scan configuration."""

    scan: ScanConfig = field(default_factory=ScanConfig)
    profile: str = "baseline"
    modules: list[str] | None = None
    output: str = "terminal"
    fail_on: str | None = None
    active: ActiveScanPolicy = field(default_factory=ActiveScanPolicy)


def _boolean(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")
    return value


def _number(value: object, name: str, minimum: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{name} must be a number >= {minimum}")
    return float(value)


def load_config(path: Path) -> ProjectConfig:
    """Load a JSON configuration file.

    JSON is used deliberately to avoid introducing another runtime dependency
    solely for configuration parsing. The file may use an .odin.json suffix.
    """
    if not path.exists():
        raise ValueError(f"Configuration file not found: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid configuration JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Configuration root must be an object")

    scan_raw = raw.get("scan", {})
    active_raw = raw.get("active", {})
    if not isinstance(scan_raw, dict) or not isinstance(active_raw, dict):
        raise ValueError("scan and active configuration must be objects")

    scan = ScanConfig(
        timeout=_number(scan_raw.get("timeout", 10), "scan.timeout", 1),
        retries=int(_number(scan_raw.get("retries", 1), "scan.retries", 0)),
        verify_tls=_boolean(scan_raw.get("verify_tls", True), "scan.verify_tls"),
        user_agent=str(scan_raw.get("user_agent", "odin-security/0.8.0")),
    )

    modules = raw.get("modules")
    if modules is not None and (
        not isinstance(modules, list) or not all(isinstance(item, str) and item.strip() for item in modules)
    ):
        raise ValueError("modules must be a list of non-empty strings")

    active = ActiveScanPolicy(
        enabled=_boolean(active_raw.get("enabled", False), "active.enabled"),
        max_requests=int(_number(active_raw.get("max_requests", 20), "active.max_requests", 1)),
        min_interval=_number(active_raw.get("min_interval", 0.25), "active.min_interval", 0),
        allow_http=_boolean(active_raw.get("allow_http", False), "active.allow_http"),
    )

    return ProjectConfig(
        scan=scan,
        profile=str(raw.get("profile", "baseline")),
        modules=modules,
        output=str(raw.get("output", "terminal")),
        fail_on=raw.get("fail_on"),
        active=active,
    )
