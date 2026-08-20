from odin.models import Finding


def test_finding_defaults() -> None:
    finding = Finding(
        id="TEST-001",
        title="Example finding",
        severity="low",
        category="test",
        description="Example",
        target="https://example.com",
    )

    assert finding.confidence == "medium"
    assert finding.references == []
