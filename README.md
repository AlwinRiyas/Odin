# Odin

A modular Python security-scanning CLI for authorized defensive security assessment.

## 0.9.0

Odin 0.9.0 provides a maintainable CLI, configurable scan profiles, passive security scanners, controlled active checks, risk scoring, and machine-readable reporting.

## Installation

### From source

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -e .
```

Build a distributable package:

```bash
python -m pip install --upgrade build
python -m build
```

The wheel and source distribution are written to `dist/`.

### Package name

The distribution name is `odin-security` and the installed CLI command is `odin`.

## Quick start

```bash
odin --help
odin version
odin scan https://example.com
```

Odin displays scan progress, HTTP status, final URL, duration, finding counts, risk score, severity counts, and normalized findings in the terminal.

Example command output:

```text
Scanner Progress
✓ DONE    http
✓ DONE    headers
✓ DONE    cookies
✓ DONE    cors
✓ DONE    disclosure

Scan Summary
HTTP Status   200
Findings      7
Risk          3.21/10  MEDIUM
```

## CLI commands

```bash
odin scan <URL>
odin modules
odin profiles
odin version
```

### Scan options

```bash
odin scan https://example.com --profile quick
odin scan https://example.com --modules headers,tls
odin scan https://example.com --output json
odin scan https://example.com --output html --output-file report.html
odin scan https://example.com --output sarif --output-file results.sarif
odin scan https://example.com --fail-on high
odin scan https://example.com --config odin.example.json
```

Supported terminal report formats are:

- `terminal` — human-readable Rich CLI output
- `json` — structured scan results
- `html` — standalone report
- `sarif` — SARIF 2.1.0 security-results format

## Scan profiles

```text
quick
baseline
full
```

Profiles select groups of scanner modules. Individual modules can also be selected explicitly with `--modules`.

## Scanner modules

The passive scanner registry currently includes:

```text
cookies
cors
disclosure
headers
http
methods
tls
```

Controlled active modules are available only through explicit active-scan policy configuration and are disabled by default.

## Configuration

Copy `odin.example.json` to a project configuration file and adjust the settings for your authorized assessment environment.

Active scanning requires an explicitly enabled policy and is bounded by a request budget. Do not enable active checks against systems without authorization.

## Architecture

```text
CLI
  ↓
Configuration
  ↓
Scan Engine
  ↓
Scanner Registry
  ↓
Normalized Findings
  ↓
Risk Engine
  ↓
Terminal / JSON / HTML / SARIF
```

## Development

Install the project in editable mode and run the quality checks:

```bash
pip install -e .
python -m pytest -q
python -m ruff check .
```

The current test suite contains 35 tests.

## Packaging checks

Before publishing a release, build and validate the distributions:

```bash
python -m build
python -m twine check dist/*
```

For a clean installation test, install the built wheel in a fresh virtual environment and verify:

```bash
python -c "import odin; print(odin.__version__)"
odin --help
odin version
```

## Responsible use

Only scan systems you own or have explicit permission to test. Odin is intended for authorized defensive security assessment.

## Project status

- [x] Professional package foundation
- [x] CLI and scan engine
- [x] Passive scanner modules
- [x] Controlled active checks
- [x] Risk and severity engine
- [x] Terminal, JSON, HTML, and SARIF reporting
- [x] Configuration files and scan profiles
- [x] CI quality gates
- [x] Package build and release validation
- [ ] PyPI/TestPyPI publication
- [ ] Long-term release and maintenance process

## License

MIT License. See `LICENSE` for details.
