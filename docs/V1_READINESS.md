# v1.0.0 Readiness

## Scope

Version 1.0.0 represents a stable public CLI and package contract, not feature completeness.

## Required gates

- [x] CI passes on every supported Python version.
- [x] Package wheel and source distribution build successfully.
- [x] Twine validation passes.
- [x] Clean wheel installation succeeds.
- [x] `odin version` reports the release version.
- [x] `odin --help` and core scan commands work after installation.
- [x] JSON, HTML, and SARIF output remain valid.
- [x] Active scanning remains disabled by default.
- [x] Configuration validation rejects invalid values.
- [x] No secrets are present in repository or package artifacts.
- [x] README and release documentation match the shipped CLI.
- [ ] TestPyPI installation succeeds before production publication.
- [ ] GitHub Release notes accurately describe the release.

## Stability policy

After 1.0.0, breaking CLI/configuration changes require a major version. New scanners and backward-compatible capabilities should use minor releases. Bug fixes and security fixes should use patch releases.

## Maintenance cycle

1. Review issues and dependency updates.
2. Add or update regression tests.
3. Run CI and package validation.
4. Update changelog and release notes.
5. Publish only when the release checklist passes.
6. Keep the default scan safe and backward compatible.
