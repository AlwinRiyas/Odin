"""Command-line interface for Odin."""

from pathlib import Path

import typer
from rich import print

from odin import __version__
from odin.config import ScanConfig
from odin.engine import available_profiles, available_scanners, run_scan
from odin.exceptions import TargetError
from odin.reporters.html import render_html
from odin.reporters.json import serialize as serialize_json
from odin.reporters.sarif import serialize as serialize_sarif
from odin.reporters.terminal import render

app = typer.Typer(help="Modular web security scanning CLI.", no_args_is_help=True)


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target URL to scan."),
    profile: str = typer.Option("baseline", help="Scan profile."),
    modules: str | None = typer.Option(None, help="Comma-separated scanner modules."),
    output: str = typer.Option("terminal", help="Output: terminal, json, html, or sarif."),
    output_file: Path | None = typer.Option(None, help="Write report to a file."),
    timeout: float = typer.Option(10.0, min=1.0, help="HTTP timeout in seconds."),
    fail_on: str | None = typer.Option(
        None,
        help="Exit non-zero when risk rating is at or above: low, medium, high, critical.",
    ),
) -> None:
    """Run security checks against a target."""
    selected_modules = [item.strip() for item in modules.split(",") if item.strip()] if modules else None
    config = ScanConfig(timeout=timeout)

    try:
        result = run_scan(url, config=config, profile=profile, modules=selected_modules)
    except (TargetError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    format_name = output.lower()
    if format_name == "terminal":
        if output_file:
            raise typer.BadParameter("--output-file cannot be used with terminal output")
        render(result)
    elif format_name == "json":
        content = serialize_json(result)
        if output_file:
            output_file.write_text(content + "\n", encoding="utf-8")
        else:
            print(content)
    elif format_name == "html":
        content = render_html(result)
        if not output_file:
            raise typer.BadParameter("HTML output requires --output-file")
        output_file.write_text(content, encoding="utf-8")
    elif format_name == "sarif":
        content = serialize_sarif(result)
        if output_file:
            output_file.write_text(content + "\n", encoding="utf-8")
        else:
            print(content)
    else:
        raise typer.BadParameter("Output must be terminal, json, html, or sarif.")

    if fail_on:
        thresholds = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        ratings = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        threshold = thresholds.get(fail_on.lower())
        if threshold is None:
            raise typer.BadParameter("fail-on must be low, medium, high, or critical")
        if ratings[result.risk.rating] >= threshold:
            raise typer.Exit(code=2)


@app.command()
def modules() -> None:
    """List available scanner modules."""
    for name in available_scanners():
        print(name)


@app.command()
def profiles() -> None:
    """List available scan profiles."""
    for name in available_profiles():
        print(name)


@app.command()
def version() -> None:
    """Show the installed Odin version."""
    print(__version__)


if __name__ == "__main__":
    app()
