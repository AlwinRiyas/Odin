"""Standalone HTML security report renderer."""

from html import escape

from odin.engine import ScanResult


def render_html(result: ScanResult) -> str:
    """Return a self-contained HTML report with escaped finding content."""
    rows = []
    for finding in result.findings:
        rows.append(
            "<tr>"
            f"<td>{escape(finding.severity.upper())}</td>"
            f"<td>{escape(finding.id)}</td>"
            f"<td>{escape(finding.title)}</td>"
            f"<td>{escape(finding.category)}</td>"
            f"<td>{escape(finding.description)}</td>"
            f"<td>{escape(finding.remediation or 'N/A')}</td>"
            "</tr>"
        )

    body = "".join(rows) or '<tr><td colspan="6">No findings detected.</td></tr>'
    risk = (
        f'<div class="metric"><strong>Risk</strong><br><span class="score">'
        f"{result.risk.score:.2f}/10</span> "
        f"({escape(result.risk.rating.upper())})</div>"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Odin Security Report</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #222; }}
header {{ margin-bottom: 2rem; }}
.metric {{ display: inline-block; margin-right: 2rem; }}
.score {{ font-size: 2rem; font-weight: 700; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 1.5rem; }}
th, td {{ border: 1px solid #ddd; padding: .7rem; text-align: left; vertical-align: top; }}
th {{ background: #f5f5f5; }}
code {{ word-break: break-word; }}
</style>
</head>
<body>
<header>
<h1>Odin Security Report</h1>
<div class="metric"><strong>Target</strong><br><code>{escape(result.target)}</code></div>
<div class="metric"><strong>HTTP</strong><br>{result.status}</div>
<div class="metric"><strong>Findings</strong><br>{result.finding_count}</div>
{risk}
</header>
<h2>Severity Summary</h2>
<ul>
{''.join(f'<li>{escape(k.title())}: {v}</li>' for k, v in result.severity_counts.items())}
</ul>
<h2>Findings</h2>
<table>
<thead><tr><th>Severity</th><th>ID</th><th>Title</th><th>Category</th><th>Description</th><th>Remediation</th></tr></thead>
<tbody>{body}</tbody>
</table>
</body>
</html>
"""
