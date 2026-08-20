# Odin

Odin is a modular Python web security-scanning CLI designed to grow from a small scanner into a maintainable security engineering project.

## Current status

Version `0.2.0` establishes the professional foundation: package layout, CLI entry point, normalized findings, runtime configuration, baseline HTTP/header checks, and automated tests.

## Quick start

```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -e .
odin scan https://example.com
```

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

- Modular scan engine
- Expanded security checks
- Structured severity and risk model
- JSON/HTML/SARIF reporting
- Configuration and scan profiles
- CI/CD and package distribution
