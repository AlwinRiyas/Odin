"""Rich terminal output."""

from rich.console import Console
from rich.table import Table

from odin.engine import ScanResult


def render(result: ScanResult, console: Console | None = None) -> None:
    console = console or Console()
    console.print(f"[bold]Target:[/bold] {result.target}")
    console.print(f"[bold]HTTP:[/bold] {result.status}  [bold]Final URL:[/bold] {result.final_url}")
    console.print(
        f"[bold]Risk:[/bold] {result.risk.score:.2f}/10 ({result.risk.rating.upper()})"
    )
    counts = result.severity_counts
    console.print(
        "  ".join(f"{key}: {value}" for key, value in counts.items() if value)
        or "No findings"
    )

    table = Table(title=f"Findings ({len(result.findings)})")
    table.add_column("Severity")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Scanner")

    for finding in result.findings:
        table.add_row(
            finding.severity.upper(),
            finding.id,
            finding.title,
            finding.scanner,
        )

    console.print(table)
