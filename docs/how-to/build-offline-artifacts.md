# Build Offline Artifacts

Offline artifacts let the generated runtime install from package archives that
were downloaded during the build.

Use them when a downstream distribution needs air-gapped installs, native
installer integration, or a single self-contained runtime.

## Choose A Layout

::::{tab-set}

:::{tab-item} External
Use `external` when you want the runtime and compressed bundle as separate
files. This is useful when an installer or package manager already knows how to
place supporting files next to the binary.

```bash
pronto build \
  --layout external \
  --command demo \
  --template ./pronto-runtime-template
```
:::

:::{tab-item} Embedded
Use `embedded` when you want one larger runtime that can bootstrap without a
separate bundle file.

```bash
pronto build \
  --layout embedded \
  --command demo \
  --template ./pronto-runtime-template
```
:::

::::

## Bootstrap From An External Bundle

For an `external` build, distribute these files together:

- `demo`
- `demo.bundle.tar.zst`
- `demo.runtime.lock`
- `demo.info.json`
- `demo.packages.txt`
- `demo.sha256`

Point the runtime at an extracted bundle directory:

```bash
mkdir -p /opt/demo-bundle
tar -I zstd -xf demo.bundle.tar.zst -C /opt/demo-bundle
demo --path /opt/demo bootstrap --bundle /opt/demo-bundle --offline
```

conda-pronto also stamps a command-specific bundle environment variable into the
runtime. For a command named `demo`, that variable is
`DEMO_BUNDLE`.

## Bootstrap From An Embedded Bundle

An embedded runtime carries the bundle inside the binary:

```bash
demoz --path /opt/demo bootstrap
```

The runtime extracts the compressed package archives to a temporary directory
during bootstrap and installs from that extracted bundle without network
access.

An explicit `--bundle` still takes priority over the embedded bundle. Use that
override to test a replacement package set without rebuilding the binary.
