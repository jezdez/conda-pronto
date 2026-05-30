# Changelog

User-facing release notes for `conda-ship` are documented here.

## 0.1.0 - 2026-05-29

Initial release of `conda-ship`, a generic builder for ready-to-run conda
runtimes. It provides the `cs` CLI. The Python package provides the optional
`conda ship` subcommand for conda installations that want plugin-style
integration.

### Highlights

- `cs`, a CLI for producing downstream conda runtime artifacts
  from committed project metadata and lockfiles.
- `cs inspect` preflights the selected manifest, lockfile, source
  environment, package exclusions, platforms, and package set without writing
  files.
- Downstream projects choose their own command name, package set, channels,
  documentation URL, and release channel.
- Downstream projects can configure the generated runtime's install location
  with an install scheme and install name.
- Built-in install schemes are `conda` for `~/.conda/INSTALL_NAME` and `data`
  for the platform user data directory.
- Runtime metadata protects bootstrapped prefixes from accidental overwrite or
  removal by the wrong generated runtime, and malformed runtime metadata is
  rejected before use.
- Generated runtimes also accept a global `--path` option for local override
  workflows where the default install location is not appropriate.
- `cs-runtime-template`, the generic runtime template used for generated
  downstream binaries.
- Support for `conda.toml` with `conda.lock`, `pyproject.toml` with
  `[tool.conda]` and `conda.lock`, `pixi.toml` with `pixi.lock`, and
  `pyproject.toml` with `[tool.pixi]` and `pixi.lock`.
- Packaged `cs` builds discover an installed `cs-runtime-template`
  automatically; `--template` remains available for explicit template paths,
  custom packaging, and cross-builds.
- `cs build` can read `command` and `layout` from `[tool.conda-ship]`; CLI
  flags remain available as release-job overrides.
- The `online` layout builds a runtime that downloads packages during bootstrap.
- `cs build --layout external` stages a runtime plus a separate compressed
  package bundle.
- `cs build --layout embedded` stages a runtime with the compressed package
  bundle inside the binary.
- `cs build --dry-run` and `cs bundle --dry-run` validate planned
  artifact work without compiling, downloading, stamping, or writing files.
- Package exclusion after lockfile resolution, so downstream distributions can
  trim packages from a solved environment before building a runtime.
- Package and channel intent comes from the selected manifest environment and
  lockfile; `[tool.conda-ship]` is reserved for conda-ship build policy.
- Build validation requires the selected runtime environment to contain `conda`,
  `conda-rattler-solver`, and `conda-spawn`, matching the generated runtime CLI.
- Generated runtime `.condarc` files use the channels stamped into the runtime lock.
- Generated runtimes bootstrap from the stamped runtime lock by default, or from
  an explicit lockfile passed with `--lockfile`.
- Default builds use Rustls with the `ring` provider so release builds do not
  depend on platform OpenSSL or AWS-LC. The `native-tls` feature remains
  available for downstream builds that want platform TLS explicitly.
- The `conda ship` adapter prefers the `cs` executable installed next to
  the current Python interpreter before falling back to `PATH`.
- The GitHub Action expects committed manifest and lockfile input, verifies
  downloaded release assets, runs published `conda-ship` binaries, and exposes
  `dist-path` for uploading the full generated artifact directory.
- The GitHub Action runs `cs build --dry-run` before writing artifact files.
- A reusable workflow is available for release builds that consume published
  `conda-ship` assets.
- Staged build metadata for generated runtimes includes `.runtime.lock`,
  `.packages.txt`, `.info.json`, and `.sha256` files.
- Release assets for tagged builds: `cs`, `cs-runtime-template`, and
  `SHA256SUMS`.
- Runtime template assets refuse to run directly; `cs build` must stamp a
  copy before it becomes a downstream runtime.
- PyPI packaging metadata for the optional conda plugin adapter.

### Security

- Bundle builds require SHA256 metadata in runtime locks.
- Cached, downloaded, embedded, and offline package archives are verified before
  they are staged or installed.
- The GitHub Action verifies artifact attestations for downloaded `cs`,
  `cs-runtime-template`, and `SHA256SUMS` assets before running them.
- GitHub workflows and the composite action use pinned actions, minimal
  permissions, explicit artifact verification, and no shell `eval` for user
  inputs.
- Rust advisory, license, dependency-ban, and source policies are enforced with
  `cargo deny`.
