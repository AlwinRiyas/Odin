# Release Process

## 1. Prepare the release

1. Update the version in `src/odin/__init__.py` and `pyproject.toml`.
2. Update the README and release notes.
3. Run the test suite and lint locally.
4. Build the package and validate the distributions.

```bash
python -m pip install --upgrade build twine
pytest
ruff check .
python -m build
python -m twine check dist/*
```

## 2. TestPyPI

Configure PyPI Trusted Publishing for this GitHub repository and the `publish-testpypi.yml` workflow. The workflow is manual (`workflow_dispatch`).

After publishing, install the package from TestPyPI in a clean environment and verify:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ odin-security
odin version
odin --help
```

## 3. GitHub release

Create and push a version tag:

```bash
git tag v0.9.0
git push origin v0.9.0
```

The tag-driven release workflow builds the wheel and source distribution, validates them with Twine, and creates a GitHub Release with the artifacts attached.

## 4. PyPI publication

Configure PyPI Trusted Publishing for `.github/workflows/publish.yml`.

Publishing is triggered only when a GitHub Release is published. Do not store a long-lived PyPI API token in the repository.

## 5. Post-release verification

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
