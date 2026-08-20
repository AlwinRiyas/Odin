"""Basic HTTP target checks."""

import requests

from odin.config import ScanConfig
from odin.exceptions import TargetError


def check_status(url: str, config: ScanConfig | None = None) -> dict[str, object]:
    """Fetch a target and return basic HTTP metadata."""
    config = config or ScanConfig()
    try:
        response = requests.get(
            url,
            timeout=config.timeout,
            verify=config.verify_tls,
            headers={"User-Agent": config.user_agent},
        )
    except requests.RequestException as exc:
        raise TargetError(f"Unable to reach target: {exc}") from exc

    return {
        "status": response.status_code,
        "server": response.headers.get("Server"),
        "final_url": str(response.url),
        "content_type": response.headers.get("Content-Type"),
    }
