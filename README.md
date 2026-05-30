# conda-pronto

Build ready-to-run conda bootstrap binaries.

`conda-pronto` is a generic builder and runtime for single-binary conda
distributions. It installs the `pronto` CLI.

`conda-express` is a downstream distribution that uses conda-pronto to publish the
official `cx` and `cxz` binaries. conda-pronto owns the generic builder/runtime; a
downstream distribution owns its package set, binary names, release channels,
and installer wrappers.

Artifact layouts:

- `online`: `<name>` with stamped lock/metadata; packages are downloaded during bootstrap.
- `external`: `<name>` plus `<name>.bundle.tar.zst`.
- `embedded`: `<name>z`, the runtime plus compressed bundle embedded in one binary.

The CLI builds from a solved downstream project. Installed builds should pass a
released runtime template; source checkouts can omit `--template` while
developing conda-pronto itself:

```bash
pronto lock
pronto inspect
pronto build --layout online --name serpe --template ./pronto-runtime-template
pronto build --layout embedded --name serpe --template ./pronto-runtime-template
pronto run --name serpe -- bootstrap --prefix /tmp/serpe-smoke
```

Every `pronto build` writes the staged binary plus artifact metadata: the
runtime lock, a tab-separated package list, an info JSON document, and SHA256
checksums. The staged binary is stamped with the runtime lock, distribution
metadata, and optional embedded bundle before checksums are written. The GitHub
Action downloads tagged `pronto` and runtime-template release assets, verifies
their GitHub attestations and `SHA256SUMS`, and then uses the same stamping
path against a committed downstream manifest and lockfile.

Most users run the builder as `pronto`. The Python package can also make
`conda pronto` available inside a conda environment; that command is a shortcut
for the same `pronto` executable. Conda packages install the Rust binary and
the small Python adapter together.

Generic runtime behavior stays here; opinionated package sets and distribution
defaults belong in downstream distributions.

`conda.toml` plus `conda.lock` is the preferred manifest/lockfile pair for new
conda-pronto project metadata. `pixi.toml` plus `pixi.lock` and Pixi's
`pyproject.toml` plus `pixi.lock` remain supported for Pixi-compatible
workflows.

`pronto` is not an OS installer generator and does not target `.sh`, `.pkg`, or
`.msi` output. It produces bootstrap binaries that can be distributed directly
or wrapped by Homebrew, constructor, Docker, enterprise packaging systems, and
other release tooling.
