"""Package-specific exceptions."""


class OdinError(Exception):
    """Base exception for expected Odin errors."""


class TargetError(OdinError):
    """Raised when a scan target cannot be reached or validated."""
