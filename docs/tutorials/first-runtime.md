# Build Your First Runtime

This tutorial builds a local conda bootstrap binary named `demo` and runs it
against a temporary prefix.

`demo` is the example binary name. conda-pronto itself provides the builder and
generic runtime; it does not publish a default runtime binary.

## Prerequisites

Run this tutorial from a project root with a manifest, a lockfile, a solved
`runtime` environment, and a `[tool.pronto]` section. A conda-pronto source
checkout works for that purpose because it carries a Pixi-compatible example
configuration.

Installed `pronto` builds need a prebuilt runtime template passed with
`--template`. In a conda-pronto source checkout you can omit that option;
the builder will compile the local `pronto-runtime` target before stamping it.

Make sure the `pronto` CLI is available on your `PATH`, then derive the runtime
lock:

```bash
pronto lock
```

`pronto lock` derives the runtime lock from the selected solved environment and
the conda-pronto runtime configuration, then writes it to `target/pronto/runtime.lock`.

## Inspect The Runtime Package Set

Check the package set that will be stamped into the runtime artifact:

```bash
pronto inspect
```

The output lists every platform in the derived runtime lock, then prints the
packages for the current platform.

## Build A Network Bootstrap Binary

Build a binary that contains lockfile metadata but downloads package archives
during bootstrap:

```bash
pronto build --layout online --name demo
```

The staged files are written to `dist/`. The binary is named `demo` on Unix
and `demo.exe` on Windows.

## Smoke Test The Runtime

Run the staged binary through conda-pronto:

```bash
pronto run --name demo -- bootstrap --prefix /tmp/demo
```

Then ask the generated runtime for status:

```bash
dist/demo status --prefix /tmp/demo
```

The status output reports the binary name, prefix, configured channels,
configured package specs, installed package count, and conda executable path.

## Build An Embedded Artifact

Build an artifact that carries compressed package archives inside the binary:

```bash
pronto build --layout embedded --name demo
```

The embedded artifact uses the `z` suffix, so the binary is staged as
`dist/demoz` on Unix and `dist/demoz.exe` on Windows.

Run the embedded artifact the same way:

```bash
dist/demoz bootstrap --prefix /tmp/demoz
```

The embedded bundle is detected automatically. No `--bundle` or `--offline`
flag is required.
