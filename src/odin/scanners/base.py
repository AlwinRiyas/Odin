"""Contracts shared by scanner modules."""

from typing import Protocol

from odin.config import ScanConfig
from odin.models import Finding


class Scanner(Protocol):
    """Protocol implemented by scanner callables."""

    def __call__(self, target: str, config: ScanConfig) -> list[Finding]: ...
