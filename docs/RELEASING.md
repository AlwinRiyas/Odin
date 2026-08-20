# Release Process

## Release candidate checklist

Before tagging a release, verify:

- [ ] Version is identical in `src/odin/__init__.py` and `pyproject.toml`.
- [ ] `pytest -q` passes.
- [ ] `ruff check .` passes.
- [ ] `python -m build` succeeds.
- [ ] `python -m twine check dist/*` succeeds.
- [ ] Wheel installs in a clean virtual environment.
- [ ] `odin version` reports the expected version.
- [ ] `odin --help` works after installation.
- [ ] JSON, HTML, and SARIF reporters produce valid output.
- [ ] README installation commands match the package metadata.
- [ ] LICENSE is present.
- [ ] No secrets or local environment files are included in the distribution.

The CI workflow now performs linting, tests, package building, and Twine validation across supported Python versions.

## TestPyPI

Configure PyPI Trusted Publishing for this GitHub repository and the `publish-testpypi.yml` workflow. The workflow is manual (`workflow_dispatch`).

After publishing, install the package from TestPyPI in a clean environment and verify:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ odin-security
odin version
odin --help
```

## GitHub release

Create and push a version tag only after the release candidate checklist passes:

```bash
git tag v0.9.0
git push origin v0.9.0
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
```

Verify that the installed version matches the GitHub release and that the CLI entry point works.

## Important

A PyPI package name is globally shared. Confirm availability and ownership of the desired distribution name before attempting the first public release. The repository currently declares `odin-security` as its distribution name.
