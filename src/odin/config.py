"""Runtime configuration for scans."""

from dataclasses import dataclass


@dataclass(slots=True)
class ScanConfig:
    timeout: float = 10.0
    retries: int = 1
    verify_tls: bool = True
    user_agent: str = "odin-security/0.2.0"
