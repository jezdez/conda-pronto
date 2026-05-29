# Changelog

User-facing release notes for `conda-pronto` are documented here.

## 0.1.0 - 2026-05-29

Initial release of `conda-pronto`, a generic builder for ready-to-run conda
bootstrap binaries. The Rust crate is published as `conda-pronto` and installs
the `pronto` CLI. The Python package provides the optional `conda pronto`
subcommand for conda installations that want plugin-style integration.

### Highlights

- `pronto`, a CLI for producing named downstream conda bootstrap binaries from
  committed project metadata and lockfiles.
- Downstream projects choose their own binary name, package set, channels,
  documentation URL, and release channel.
- `pronto-runtime-template`, the generic runtime template used for generated
  downstream binaries.
- Support for `conda.toml` with `conda.lock`, `pixi.toml` with `pixi.lock`, and
  Pixi configuration in `pyproject.toml` with `pixi.lock`.
- `pronto build --layout online` builds a runtime that downloads packages
  during bootstrap.
- Offline bundle generation for runtimes that install from embedded or
  pre-downloaded conda package archives.
- Package exclusion after lockfile resolution, so downstream distributions can
  trim packages from a solved environment before building a runtime.
- Generated runtime `.condarc` files use the channels stamped into the runtime.
- Runtime `--channel` and `--package` flags are available for live solves with
  `--no-lock`; lockfile-based builds use the committed lockfile contents.
- Default builds use Rustls with the `ring` provider so release builds do not
  depend on platform OpenSSL or AWS-LC. The `native-tls` feature remains
  available for downstream builds that want platform TLS explicitly.
- The `conda pronto` adapter prefers the `pronto` executable installed next to
  the current Python interpreter before falling back to `PATH`.
- The GitHub Action expects committed manifest and lockfile input, verifies
  downloaded release assets, and runs published `conda-pronto` binaries.
- A reusable workflow is available for release builds that consume published
  `conda-pronto` assets.
- Staged build metadata for generated runtimes includes `.runtime.lock`,
  `.packages.txt`, `.info.json`, and `.sha256` files.
- Release assets for tagged builds: `pronto`, `pronto-runtime-template`, and
  `SHA256SUMS`.
- Crates.io and PyPI packaging metadata for publishing `conda-pronto`.

### Security

- Bundle builds require SHA256 metadata in runtime locks.
- Cached, downloaded, embedded, and offline package archives are verified before
  they are staged or installed.
- The GitHub Action verifies artifact attestations for downloaded `pronto`,
  `pronto-runtime-template`, and `SHA256SUMS` assets before running them.
- GitHub workflows and the composite action use pinned actions, minimal
  permissions, explicit artifact verification, and no shell `eval` for user
  inputs.
- Rust advisory, license, dependency-ban, and source policies are enforced with
  `cargo deny`.
