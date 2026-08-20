# Odin

A modular Python security-scanning CLI built for maintainability, automation, and authorized defensive security assessment.

## Current release line

`0.9.0` — configuration, reporting, risk scoring, passive scanners, controlled active checks, and CI quality gates.

## Installation

### Development

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
```

### Build a distributable package

```bash
python -m pip install --upgrade build
python -m build
```

This produces a wheel and source distribution under `dist/`.

## CLI

```bash
odin --help
odin scan https://example.com
odin scan https://example.com --profile quick
odin scan https://example.com --modules headers,tls
odin scan https://example.com --output json
odin scan https://example.com --output html --output-file report.html
odin scan https://example.com --output sarif --output-file results.sarif
odin scan https://example.com --fail-on high
odin scan https://example.com --config odin.example.json
odin modules
odin profiles
odin version
```

## Configuration

Copy `odin.example.json` to a project configuration file and adjust the settings for your authorized assessment environment.

Active scanning is disabled by default and requires an explicit policy. Do not enable active checks against systems without authorization.

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

```bash
pip install -e .
pip install pytest ruff
pytest
ruff check .
```

## Packaging

Before publishing, build and inspect the package locally:

```bash
python -m pip install --upgrade build
python -m build
python -m pip install dist/*.whl
odin version
```

The package metadata currently uses the distribution name `odin-security` and the CLI command `odin`.

## Responsible use

Only scan systems you own or have explicit permission to test. Active checks are intentionally bounded and disabled by default.

## Roadmap

- [x] Professional package foundation
- [x] CLI and scan engine
- [x] Expanded passive scanner modules
- [x] Controlled active checks
- [x] Risk/severity engine
- [x] Terminal/JSON/HTML/SARIF reporting
- [x] Configuration files and scan profiles
- [x] CI quality matrix
- [ ] Release automation
- [ ] PyPI/TestPyPI publication
- [ ] Long-term release and maintenance process
