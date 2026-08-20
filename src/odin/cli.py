"""Command-line interface for Odin."""

import typer
from rich import print

from odin import __version__
from odin.config import ScanConfig
from odin.engine import available_profiles, available_scanners, run_scan
from odin.exceptions import TargetError
from odin.reporters.json import serialize
from odin.reporters.terminal import render

app = typer.Typer(help="Modular web security scanning CLI.", no_args_is_help=True)


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target URL to scan."),
    profile: str = typer.Option("baseline", help="Scan profile."),
    modules: str | None = typer.Option(None, help="Comma-separated scanner modules."),
    output: str = typer.Option("terminal", help="Output format: terminal or json."),
    timeout: float = typer.Option(10.0, min=1.0, help="HTTP timeout in seconds."),
) -> None:
    """Run passive security checks against a target."""
    selected_modules = [item.strip() for item in modules.split(",") if item.strip()] if modules else None
    config = ScanConfig(timeout=timeout)

    try:
        result = run_scan(url, config=config, profile=profile, modules=selected_modules)
    except (TargetError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    if output == "json":
        print(serialize(result))
    elif output == "terminal":
        render(result)
    else:
        raise typer.BadParameter("Output must be 'terminal' or 'json'.")


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
