# Concepts

conda-ship separates three concerns:

- resolving and recording a conda runtime package set
- stamping a generic runtime template into a distribution-specific runtime
- staging release artifacts that downstream projects can distribute

The split from conda-express makes that separation explicit. conda-ship owns these
generic concerns; conda-express owns the `cx` and `cxz` distribution built with
them.

## Builder

The `cs` CLI is the builder. It reads `conda.toml`/`conda.lock`,
`pyproject.toml` with `[tool.conda]` plus `conda.lock`, the compatible
`pixi.toml`/`pixi.lock` pair, or `pyproject.toml` with `[tool.pixi]` plus
`pixi.lock`, applies `[tool.conda-ship]`, then derives a runtime lock, bundle files,
runtimes, and artifact metadata.

The selected source lockfile is the source of the concrete conda package
records. conda-ship is not a replacement for
{external+conda-workspaces:doc}`conda-workspaces <index>`, Pixi, or any other
workspace solver; it consumes a solved environment and turns it into
runtime artifacts.

## Runtime

A runtime is the executable that users run after conda-ship finishes.
Examples include `demo`, `demoz`, `cx`, and `cxz`.

The command name is the base command name for that runtime. It can come from
`[tool.conda-ship].command` or `--command`, and it is not a conda environment
name. The `embedded` layout adds the `z` suffix to the staged executable name
because that variant contains compressed package archives.

Use "runtime" for the thing conda-ship produces, "command name" for the
resolved executable name, and "artifact" for the release files written to
`dist/`.

## Runtime Template

`conda-ship-runtime` is an internal generic binary target. It is not a first-party
distribution. During `cs build`, the builder copies a generic runtime
template under the resolved command name and stamps the copy with the
downstream command name, install scheme and install name, metadata filename, environment variable
names, runtime lock, and optional bundle. The stamped copy is the runtime.
Released builds use prebuilt template assets; source checkouts can build the
template locally as a development fallback.

## Runtime Lock

The runtime lock is derived from the configured source environment, then filtered
through `[tool.conda-ship].exclude`. conda-ship stamps the derived lock into every
runtime artifact and stages a copy next to the output binary. It is not a second
checked-in project lockfile.

`cs inspect` derives the same runtime lock without writing files, so it is
the local preflight command. `cs build`, `cs bundle`, and `cs run`
derive the lock as part of their normal work.

The generated runtime can install from:

- the stamped lockfile and network package downloads
- an external lockfile passed with `--lockfile`

## Bundles

Bundles contain downloaded conda package archives.

The `external` layout pairs a runtime with `COMMAND.bundle.tar.zst`. The
`embedded` layout appends `z` to the command name and includes the compressed
bundle inside the runtime.

An embedded runtime automatically uses its bundled archives during
bootstrap. An explicit `--bundle` can still override that bundle.
