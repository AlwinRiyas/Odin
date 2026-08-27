# Odin

A modular Python security-scanning CLI for authorized defensive web security assessment.

## Current release line

Odin provides a maintainable scanning engine with configurable scan profiles, passive security checks, controlled active checks, risk scoring, and machine-readable reporting.

## Installation

For a published installation:

```bash
pip install odin-security
```

For local development:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
```

## Quick start

```bash
odin --help
odin version
odin modules
odin profiles
odin scan https://example.com
```

Only scan systems that you own or have explicit permission to test.

## Scan profiles

- `quick` — lightweight HTTP and security-header checks
- `baseline` — standard passive security assessment
- `full` — expanded passive assessment including TLS and HTTP-method checks

Example:

```bash
odin scan https://example.com --profile full
```

Individual modules can also be selected:

```bash
odin scan https://example.com --modules headers,tls
```

Active modules require an explicitly enabled active-scan policy and are intentionally bounded.

## Reporting

Terminal output is the default. Odin also supports JSON, HTML, and SARIF reports:

```bash
odin scan https://example.com --output json --output-file results.json
odin scan https://example.com --output html --output-file report.html
odin scan https://example.com --output sarif --output-file results.sarif
```

Risk thresholds can be used for automation and CI workflows:

```bash
odin scan https://example.com --fail-on high
```

## Configuration

Use `odin.example.json` as a starting point for project-specific configuration:

```bash
odin scan https://example.com --config odin.example.json
```

Configuration can define the scan settings, profile, selected modules, output format, risk threshold, and active-scan policy.

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

## Project structure

```text
src/odin/
├── cli.py
├── engine.py
├── active.py
├── findings.py
├── models.py
├── risk.py
├── settings.py
├── scanners/
└── reporters/

tests/
docs/
```

## Development

Install the project and development tools:

```bash
pip install -e .
pip install pytest ruff
```

Run the quality checks:

```bash
python -m pytest -q
python -m ruff check .
```

Build the distributable package:

```bash
python -m pip install --upgrade build
python -m build
python -m twine check dist/*
```

## Package information

- Distribution: `odin-security`
- CLI command: `odin`
- Current version: `0.9.0`
- License: MIT
- Supported Python: 3.10+

## Security and responsible use

Odin is intended for authorized defensive security assessment. Do not use it to scan systems without permission. Active checks are disabled by default and subject to an explicit request budget.

## Documentation

Release and maintenance procedures are documented in `docs/RELEASING.md`. Version-readiness information is available in `docs/V1_READINESS.md`.

## Roadmap

- [x] Professional package foundation
- [x] CLI and scan engine
- [x] Expanded passive scanner modules
- [x] Controlled active checks
- [x] Risk/severity engine
- [x] Terminal/JSON/HTML/SARIF reporting
- [x] Configuration files and scan profiles
- [x] CI quality gates
- [ ] PyPI/TestPyPI publication
- [ ] Long-term release and maintenance process
