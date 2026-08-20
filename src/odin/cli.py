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
from odin.settings import load_config

app = typer.Typer(help="Modular web security scanning CLI.", no_args_is_help=True)


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target URL to scan."),
    profile: str | None = typer.Option(None, help="Scan profile (overrides config)."),
    modules: str | None = typer.Option(None, help="Comma-separated modules (overrides config)."),
    output: str | None = typer.Option(None, help="Output format (overrides config)."),
    output_file: Path | None = typer.Option(None, help="Write report to a file."),
    timeout: float | None = typer.Option(None, min=1.0, help="HTTP timeout in seconds."),
    fail_on: str | None = typer.Option(None, help="Risk threshold (overrides config)."),
    config_file: Path | None = typer.Option(None, "--config", help="Project configuration JSON file."),
) -> None:
    """Run security checks against a target."""
    try:
        project = load_config(config_file) if config_file else None
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    selected_modules = (
        [item.strip() for item in modules.split(",") if item.strip()]
        if modules
        else (project.modules if project else None)
    )
    config = project.scan if project else ScanConfig()
    if timeout is not None:
        config.timeout = timeout

    selected_profile = profile or (project.profile if project else "baseline")
    format_name = (output or (project.output if project else "terminal")).lower()
    threshold_name = fail_on if fail_on is not None else (project.fail_on if project else None)
    active_policy = project.active if project else None

    try:
        result = run_scan(
            url,
            config=config,
            profile=selected_profile,
            modules=selected_modules,
            active_policy=active_policy,
        )
    except (TargetError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

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
        if not output_file:
            raise typer.BadParameter("HTML output requires --output-file")
        output_file.write_text(render_html(result), encoding="utf-8")
    elif format_name == "sarif":
        content = serialize_sarif(result)
        if output_file:
            output_file.write_text(content + "\n", encoding="utf-8")
        else:
            print(content)
    else:
        raise typer.BadParameter("Output must be terminal, json, html, or sarif.")

    if threshold_name:
        thresholds = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        threshold = thresholds.get(threshold_name.lower())
        if threshold is None:
            raise typer.BadParameter("fail-on must be info, low, medium, high, or critical")
        if thresholds[result.risk.rating] >= threshold:
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
