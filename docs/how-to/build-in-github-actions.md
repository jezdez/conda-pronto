# Build In GitHub Actions

Use the composite action when a downstream distribution repository wants
conda-ship to build release artifacts in CI.

The action is the public CI interface for conda-ship-built runtimes.
Downstream repositories, including conda-express, keep their package set in a
committed manifest and lockfile. The action reads that project input and stamps
a runtime instead of carrying a copy of the generic builder.

Pin the action to a conda-ship release tag. The action downloads the matching
`cs` and `cs-runtime-template` release assets, verifies their GitHub
artifact attestations and release `SHA256SUMS`, and stamps the generated
runtime. It runs `cs build --dry-run` before the real build so manifest,
lockfile, naming, template, install scheme, and bundle metadata issues fail
before artifact files are written.

GitHub-hosted runners already include the GitHub CLI used for attestation
verification. Self-hosted runners must provide `gh`.

## Single-Platform Example

The checked-out repository must contain `conda.toml` plus `conda.lock`,
`pyproject.toml` with `[tool.conda]` plus `conda.lock`, `pixi.toml` plus
`pixi.lock`, or `pyproject.toml` with `[tool.pixi]` plus `pixi.lock`. These
examples assume the manifest contains `[tool.conda-ship].runtime` and
`[tool.conda-ship].delegate`; pass `runtime` or `delegate` only when CI should
override those values.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: jezdez/conda-ship@v0.1.0
        id: cs

      - uses: actions/upload-artifact@v4
        with:
          name: ${{ steps.cs.outputs.asset-name }}
          path: ${{ steps.cs.outputs.dist-path }}
```

Use a tag for release builds. Branch refs do not have matching release assets.

## Project Root Example

When the downstream manifest lives below the repository root, point the action
at that directory:

```yaml
steps:
  - uses: actions/checkout@v4

  - uses: jezdez/conda-ship@v0.1.0
    id: cs
    with:
      root: dist/demo
```

The action does not run a solve, generate a manifest, or refresh a lockfile.
Update and commit the lockfile before running release builds.

Use `install-scheme` for a named install policy and `install-name` for the name inside
that install scheme. When neither is set, the action leaves those values to
`[tool.conda-ship]` and the runtime defaults. With the default `conda-home`
install scheme, a runtime named `demo` installs below `~/.conda/demo`.

## External Bundle Example

Set `layout` to `external` when you want to distribute the runtime and package
bundle as separate files:

```yaml
- uses: jezdez/conda-ship@v0.1.0
  id: cs
  with:
    layout: external

- uses: actions/upload-artifact@v4
  with:
    name: ${{ steps.cs.outputs.asset-name }}
    path: ${{ steps.cs.outputs.dist-path }}
```

## Embedded Bundle Example

Set `layout` to `embedded` when the runtime must bootstrap without network
access:

```yaml
- uses: jezdez/conda-ship@v0.1.0
  id: cs
  with:
    layout: embedded
```

The output runtime uses the `z` suffix, for example `demoz` on Unix or
`demoz.exe` on Windows.

## Matrix Builds

Run the action across operating systems to produce platform-specific
runtimes:

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]

runs-on: ${{ matrix.os }}

steps:
  - uses: actions/checkout@v4

  - uses: jezdez/conda-ship@v0.1.0
    id: cs
```

Each job emits an asset name qualified with the runner target triple.

## Downstream Release Preparation

Use `dist-path` as the source of truth for artifact uploads. It contains the
runtime, optional external bundle, `.info.json`, `.runtime.lock`,
`.packages.txt`, and `.sha256` files for that build. The individual path
outputs are still available when release tooling or package-manager wrappers
need to address one file directly.
