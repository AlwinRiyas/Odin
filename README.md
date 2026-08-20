# Odin

Odin is a modular Python security-scanning CLI designed to grow into a maintainable security engineering project.

## Status

Current development line: `0.3.0` — Phase 2 professional CLI and scan engine.

## Installation

```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -e .
```

## CLI

```bash
odin --help
odin scan https://example.com
odin scan https://example.com --profile quick
odin scan https://example.com --modules headers
odin scan https://example.com --output json
odin modules
odin profiles
odin version
```

## Architecture

The CLI delegates target execution to the scan engine. Scanner modules produce normalized `Finding` objects, while reporters format the resulting scan data for humans or automation.

## Development

```bash
pip install -e .
pip install pytest ruff
pytest
ruff check .
```

## Responsible use

Only scan systems you own or have explicit permission to test. The project is intended for authorized security assessment and defensive engineering.

## Roadmap

- [x] Professional package foundation
- [x] CLI and scan engine
- [ ] Expanded scanner modules
- [ ] Risk/severity engine
- [ ] HTML/SARIF reporting
- [ ] Configuration files and scan profiles
- [ ] PyPI release automation
