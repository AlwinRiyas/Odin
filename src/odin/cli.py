"""Command-line interface for Odin."""

import typer
from rich import print

from odin import __version__
from odin.config import ScanConfig
from odin.scanners.basic import check_status
from odin.scanners.headers import check_headers

app = typer.Typer(help="Modular web security scanning CLI.")


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target URL to scan."),
    timeout: float = typer.Option(10.0, min=1.0, help="HTTP timeout in seconds."),
) -> None:
    """Run the current baseline security checks against a target."""
    config = ScanConfig(timeout=timeout)
    print(f"[bold]Odin[/bold] {__version__}")
    print(f"Target: {url}")

    basic = check_status(url, config)
    print(f"HTTP: {basic['status']}  Final URL: {basic['final_url']}")

    findings = check_headers(url, config)
    if not findings:
        print("[green]No missing baseline security headers detected.[/green]")
        return

    print(f"Findings: {len(findings)}")
    for finding in findings:
        print(f"- [{finding.severity.upper()}] {finding.title}")


@app.command()
def version() -> None:
    """Show the installed Odin version."""
    print(__version__)


if __name__ == "__main__":
    app()
