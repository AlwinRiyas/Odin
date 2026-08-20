"""JSON serialization for scan results."""

import json
from dataclasses import asdict

from odin.engine import ScanResult


def serialize(result: ScanResult, indent: int = 2) -> str:
    return json.dumps(asdict(result), indent=indent)
