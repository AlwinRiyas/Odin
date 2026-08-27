# Release Process

## Stable release checklist

Before tagging a release, verify:

- [x] Version is identical in `src/odin/__init__.py` and `pyproject.toml`.
- [x] `pytest -q` passes.
- [x] `ruff check .` passes.
- [x] `python -m build` succeeds.
- [x] `python -m twine check dist/*` succeeds.
- [x] Wheel installs in a clean virtual environment.
- [x] `odin version` reports the expected version.
- [x] `odin --help` works after installation.
- [x] JSON, HTML, and SARIF reporters produce valid output.
- [x] README installation commands match the package metadata.
- [x] LICENSE is present.
- [x] No secrets or local environment files are included in the distribution.

CI performs linting, tests, package building, and distribution validation across supported Python versions.

## TestPyPI

Configure PyPI Trusted Publishing for this GitHub repository and the `publish-testpypi.yml` workflow. The workflow is manual (`workflow_dispatch`).

After publishing, install the package from TestPyPI in a clean environment and verify:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ odin-security
odin version
odin --help
```

## GitHub release

Create and push the release tag only after the stable release checklist passes:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The tag-driven release workflow builds the wheel and source distribution, validates them with Twine, and creates a GitHub Release with the artifacts attached.

## PyPI publication

Configure PyPI Trusted Publishing for `.github/workflows/publish.yml`.

Publishing is triggered only when a GitHub Release is published. Do not store a long-lived PyPI API token in the repository.

## Post-release verification

From a clean environment:

```bash
python -m venv verify-env
# activate the environment
python -m pip install --upgrade pip
python -m pip install odin-security
odin version
odin --help
odin scan https://example.com
```

Verify that the installed version matches the GitHub release and that the CLI entry point works.

## Versioning policy

After 1.0.0, breaking CLI or configuration changes require a major version. New backward-compatible capabilities use minor releases. Bug fixes and security fixes use patch releases.

## Important

A PyPI package name is globally shared. Confirm availability and ownership of the desired distribution name before attempting the first public release. The repository currently declares `odin-security` as its distribution name.
