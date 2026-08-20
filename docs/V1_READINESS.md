# v1.0.0 Readiness

## Scope

Version 1.0.0 should represent a stable public CLI and package contract, not feature completeness.

## Required gates

- [ ] CI passes on every supported Python version.
- [ ] Package wheel and source distribution build successfully.
- [ ] Twine validation passes.
- [ ] Clean wheel installation succeeds.
- [ ] `odin version` reports the release version.
- [ ] `odin --help` and core scan commands work after installation.
- [ ] JSON, HTML, and SARIF output remain valid.
- [ ] Active scanning remains disabled by default.
- [ ] Configuration validation rejects invalid values.
- [ ] No secrets are present in repository or package artifacts.
- [ ] README and release documentation match the shipped CLI.
- [ ] TestPyPI installation succeeds before production publication.
- [ ] GitHub Release notes accurately describe the release.

## Stability policy

After 1.0.0, breaking CLI/configuration changes require a major version. New scanners and backward-compatible capabilities should use minor releases. Bug fixes and security fixes should use patch releases.

## Weekly maintenance cycle

1. Review issues and dependency updates.
2. Add or update regression tests.
3. Run CI and package validation.
4. Update changelog/release notes.
5. Publish a release only when the release checklist passes.
6. Keep the default scan safe and backward compatible.
