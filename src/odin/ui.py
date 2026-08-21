"""Rich terminal UI for Odin."""

from __future__ import annotations

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from odin import __version__

console = Console()


SEVERITY_STYLES = {
    "critical": "bold red",
    "high": "bold red",
    "medium": "bold yellow",
    "low": "bold blue",
    "info": "bold cyan",
}


def render_banner() -> None:
    """Render the Odin banner."""
    title = Text()
    title.append("ODIN", style="bold cyan")
    title.append(f"  v{__version__}", style="dim")

    console.print(
        Panel(
            title,
            subtitle="Web Security Scanner",
            border_style="cyan",
            padding=(0, 2),
        )
    )


def render_scan_start(
    target: str,
    profile: str,
    modules: list[str] | None,
) -> None:
    """Render scan metadata."""
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
    )

    table.add_row("Target", target)
    table.add_row("Profile", profile)
    table.add_row(
        "Modules",
        ", ".join(modules) if modules else "profile defaults",
    )

    console.print(table)
    console.print()


def build_progress_table(
    modules: list[str],
    states: dict[str, str],
) -> Table:
    """Build the scanner progress table."""
    table = Table(
        title="Scanner Progress",
        expand=True,
    )

    table.add_column("Status", width=10)
    table.add_column("Module")

    for module in modules:
        state = states.get(module, "pending")

        if state == "completed":
            status = Text("✓ DONE", style="bold green")
        elif state == "running":
            status = Text("● RUN", style="bold yellow")
        else:
            status = Text("○ WAIT", style="dim")

        table.add_row(status, module)

    return table


def run_with_progress(
    scan_function,
    target: str,
    config,
    profile: str,
    modules: list[str] | None,
    active_policy,
):
    """Run the scan while displaying live scanner progress."""
    from odin.engine import PROFILES

    selected = modules if modules is not None else PROFILES[profile]

    states = {module: "pending" for module in selected}

    def callback(module: str, state: str) -> None:
        states[module] = state

    with Live(
        build_progress_table(selected, states),
        console=console,
        refresh_per_second=10,
    ) as live:

        def progress_callback(module: str, state: str) -> None:
            callback(module, state)
            live.update(
                build_progress_table(
                    selected,
                    states,
                )
            )

        return scan_function(
            target,
            config=config,
            profile=profile,
            modules=modules,
            active_policy=active_policy,
            progress_callback=progress_callback,
        )


def render_summary(result, duration: float) -> None:
    """Render the scan summary."""
    rating = result.risk.rating.lower()

    rating_style = {
        "critical": "bold red",
        "high": "bold red",
        "medium": "bold yellow",
        "low": "bold blue",
        "info": "bold cyan",
    }.get(rating, "bold")

    table = Table(
        title="Scan Summary",
        show_header=False,
        expand=True,
    )

    table.add_row("HTTP Status", str(result.status))
    table.add_row("Final URL", str(result.final_url))
    table.add_row("Duration", f"{duration:.2f}s")
    table.add_row("Findings", str(result.finding_count))

    risk = Text()
    risk.append(
        f"{result.risk.score:.2f}/10",
        style="bold",
    )
    risk.append("  ")
    risk.append(
        result.risk.rating.upper(),
        style=rating_style,
    )

    table.add_row("Risk", risk)

    console.print(table)


def render_severity_summary(result) -> None:
    """Render severity counts."""
    counts = result.severity_counts

    table = Table(
        title="Severity",
        show_header=False,
        expand=True,
    )

    for severity in (
        "critical",
        "high",
        "medium",
        "low",
        "info",
    ):
        count = counts.get(severity, 0)

        if count == 0:
            continue

        table.add_row(
            Text(
                severity.upper(),
                style=SEVERITY_STYLES[severity],
            ),
            str(count),
        )

    if result.finding_count == 0:
        table.add_row(
            Text(
                "NONE",
                style="bold green",
            ),
            "0",
        )

    console.print(table)


def render_findings(findings) -> None:
    """Render detailed findings."""
    if not findings:
        console.print(
            Panel(
                "[bold green]No security findings detected.[/bold green]",
                border_style="green",
            )
        )
        return

    table = Table(
        title=f"Findings ({len(findings)})",
        expand=True,
    )

    table.add_column("Severity", width=10)
    table.add_column("ID", width=10)
    table.add_column("Title")
    table.add_column("Scanner", width=14)

    for finding in findings:
        severity = finding.severity.lower()

        table.add_row(
            Text(
                severity.upper(),
                style=SEVERITY_STYLES.get(
                    severity,
                    "bold",
                ),
            ),
            finding.id,
            finding.title,
            finding.scanner or "-",
        )

    console.print(table)


def render_scan_result(result, duration: float) -> None:
    """Render the final scan result."""
    console.print()

    render_summary(
        result,
        duration,
    )

    console.print()

    render_severity_summary(result)

    console.print()

    render_findings(
        result.findings,
    )

    console.print()

    if result.finding_count:
        console.print(
            Panel(
                Text.assemble(
                    ("✓ ", "bold yellow"),
                    ("Scan completed with ", "bold"),
                    (
                        str(result.finding_count),
                        "bold",
                    ),
                    (" finding(s).", "bold"),
                ),
                border_style="yellow",
            )
        )
    else:
        console.print(
            Panel(
                "[bold green]✓ Scan completed successfully.[/bold green]",
                border_style="green",
            )
        )