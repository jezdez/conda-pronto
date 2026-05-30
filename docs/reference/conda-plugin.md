# `conda pronto` Reference

Most users run conda-pronto as `pronto`.

When `conda-pronto` is installed in a conda environment, it can also add a
`conda pronto` command. This is only a conda-style shortcut for the same
builder:

```bash
conda pronto lock
conda pronto inspect
conda pronto build --layout online --command demo --template ./pronto-runtime-template
```

`conda pronto ...` runs the installed `pronto` executable with the same
arguments. It is not a separate builder and it does not make conda-pronto part
of conda itself.

Installed builds pass `--template` to stamp a prebuilt generic runtime
template; source checkouts can omit that option while developing conda-pronto
itself.

## Packaging Details

`conda-pronto` first looks for a `pronto` executable next to the current Python
interpreter, then falls back to `PATH`.

A conda package must install both pieces into the same environment:

- the Rust-built `pronto` executable
- the Python `conda_pronto` adapter package

For custom packaging or tests, set `CONDA_PRONTO_EXECUTABLE` to an explicit
executable path.

## Argument Forwarding

Arguments after `conda pronto` are passed to `pronto`:

```bash
conda pronto build \
  --layout embedded \
  --command demo \
  --template ./pronto-runtime-template
```

When you need to pass an argument that conda's own parser would consume, insert
`--` before the conda-pronto arguments:

```bash
conda pronto -- --help
```

Running `conda pronto` without arguments shows `pronto --help`.
