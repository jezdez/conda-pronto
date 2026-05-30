# Builder CLI Reference

The `pronto` CLI builds and stages conda runtimes.

This page covers the builder CLI. For the command surface exposed by generated
runtimes, see {doc}`runtime-cli`.

The `conda-pronto` package can also make `conda pronto` available as a
conda-style shortcut for this CLI. See {doc}`conda-plugin`.

Installed `pronto` builds use a prebuilt runtime template passed with
`--template`. Source checkouts can omit that option while developing
conda-pronto itself; in that mode `pronto build` compiles the internal
`pronto-runtime` target before stamping the staged artifact.

## `pronto lock`

Derive the runtime lock from the selected project lockfile environment and
write it to `target/pronto/runtime.lock`.

```bash
pronto lock [--check] [--root PATH]
```

Options:

- `--check`: verify that the runtime lock can be derived; do not write it.
- `--root PATH`: use a build root instead of auto-detecting one.

## `pronto inspect`

Summarize the derived runtime lock.

```bash
pronto inspect [--platform PLATFORM] [--json] [--root PATH]
```

Options:

- `--platform PLATFORM`: inspect a conda platform such as `linux-64`.
- `--json`: emit machine-readable JSON.
- `--root PATH`: use a build root instead of auto-detecting one.

## `pronto bundle`

Download package archives from the derived runtime lock into
`target/pronto/bundle/` and compress them as `target/pronto/bundle.tar.zst`.

```bash
pronto bundle [--platform PLATFORM] [--root PATH]
```

Options:

- `--platform PLATFORM`: choose the conda platform to download.
- `--root PATH`: use a build root instead of auto-detecting one.

## `pronto build`

Build and stage a runtime artifact.

```bash
pronto build --command COMMAND [--layout LAYOUT] [--target-label LABEL] \
  [--platform PLATFORM] [--target TRIPLE] [--template PATH] \
  [--docs-url URL] [--scheme SCHEME] [--install-name NAME] \
  [--out-dir PATH] [--root PATH]
```

`COMMAND`, `LABEL`, and `TRIPLE` are used in artifact filenames. They must
start with an ASCII letter or digit and may only contain ASCII letters, digits,
`.`, `_`, and `-`. `COMMAND` names the generated runtime; it is not a conda
environment name.

Options:

- `--command COMMAND`: required command name for the generated runtime.
- `--layout online`: stage a runtime that downloads packages during bootstrap.
- `--layout external`: stage a runtime plus compressed bundle.
- `--layout embedded`: stage a runtime with the compressed bundle embedded.
- `--target-label LABEL`: append a platform or target label to artifact names.
- `--platform PLATFORM`: choose the conda platform for metadata and bundles.
- `--target TRIPLE`: Rust target triple for source-checkout builds; also selects
  the staged `.exe` suffix for Windows artifacts when a template is supplied.
  Path-like custom target specifications are not supported here.
- `--template PATH`: prebuilt generic runtime template binary to copy and
  stamp. When omitted, `pronto build` compiles `pronto-runtime` from `--root`.
- `--docs-url URL`: documentation URL stamped into runtime help output.
- `--scheme SCHEME`: install scheme stamped into the runtime. Currently
  supported: `conda`, which installs below `~/.conda/INSTALL_NAME`, and
  `data`, which installs below the platform user data directory.
- `--install-name NAME`: name used inside the install scheme. Defaults to
  `COMMAND`.
- `--out-dir PATH`: write staged artifacts somewhere other than `dist/`.
- `--root PATH`: use a project root instead of auto-detecting one.

## `pronto run`

Build a runtime artifact and execute it immediately.

```bash
pronto run --command COMMAND [--layout LAYOUT] [--platform PLATFORM] \
  [--template PATH] [--docs-url URL] [--scheme SCHEME] [--install-name NAME] \
  [--out-dir PATH] [--root PATH] \
  -- RUNTIME_ARGS...
```

Everything after `--` is passed to the staged runtime.

Options:

- `--command COMMAND`: required command name for the generated runtime.
- `--layout online`: stage a runtime that downloads packages during bootstrap.
- `--layout external`: stage a runtime plus compressed bundle.
- `--layout embedded`: stage a runtime with the compressed bundle embedded.
- `--platform PLATFORM`: choose the conda platform for metadata and bundles.
- `--template PATH`: prebuilt generic runtime template binary to copy and
  stamp. When omitted, `pronto run` compiles `pronto-runtime` from `--root`.
- `--docs-url URL`: documentation URL stamped into runtime help output.
- `--scheme SCHEME`: install scheme stamped into the runtime. Currently
  supported: `conda` and `data`.
- `--install-name NAME`: name used inside the install scheme. Defaults to
  `COMMAND`.
- `--out-dir PATH`: write staged artifacts somewhere other than `dist/`.
- `--root PATH`: use a project root instead of auto-detecting one.
- `RUNTIME_ARGS`: arguments passed to the staged runtime after it is built.

## `pronto configure`

Patch runtime packages, channels, or excludes in the selected project manifest.

```bash
pronto configure [--package SPEC]... [--channel CHANNEL]... [--exclude NAME]... \
  [--root PATH]
```

Repeat list options for each value. Package specs are conda matchspecs, so
version constraints may contain commas. After configuration changes, refresh
the source lockfile with the tool that owns the manifest, then run
`pronto lock`.

Options:

- `--package SPEC`: conda package matchspec to include; repeat for multiple packages.
- `--channel CHANNEL`: conda channel name or URL to use; repeat for multiple channels.
- `--exclude NAME`: package name to prune after solving; repeat for multiple packages.
- `--root PATH`: use a build root instead of auto-detecting one.
