"""JSON serialization for scan results."""

import json

from odin.engine import ScanResult


def serialize(result: ScanResult, indent: int = 2) -> str:
    """Serialize a scan result using the public result contract."""
    return json.dumps(result.to_dict(), indent=indent)
