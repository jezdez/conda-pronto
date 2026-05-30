# Configuration Reference

conda-pronto reads project intent from a conda-compatible manifest and concrete
package records from the matching lockfile.

The preferred manifest is `conda.toml` with `conda.lock`. `pixi.toml` with
`pixi.lock` and Pixi's `pyproject.toml` with `pixi.lock` remain supported for
Pixi-compatible workflows.

Downstream distributions maintain these values in their own project manifest.
conda-pronto treats the values as build input; it does not define a universal
conda distribution.

`pronto lock`, `pronto inspect`, `pronto build`, and `pronto run` can read either
manifest/lockfile pair. Installed builds pass `--template` so conda-pronto
can stamp a prebuilt generic runtime without needing the conda-pronto source
checkout.

## Manifest Discovery

conda-pronto looks in the build root for:

1. `conda.toml`
2. `pixi.toml`
3. `pyproject.toml` when it contains `[tool.pixi]` or `[tool.pronto]`

The selected manifest determines the lockfile:

| Manifest | Lockfile |
| --- | --- |
| `conda.toml` | `conda.lock` |
| `pixi.toml` | `pixi.lock` |
| `pyproject.toml` with Pixi config | `pixi.lock` |

`conda.lock` and `pixi.lock` are source lockfiles owned by their respective
workspace tools. `target/pronto/runtime.lock` is generated build output owned
by conda-pronto.

## Runtime Environment

The selected environment determines the conda packages available to the
generated bootstrap runtime. In `conda.toml` or `pixi.toml`, this is commonly a
dedicated `runtime` environment:

```toml
[feature.runtime.dependencies]
python = ">=3.12"
conda = ">=25.1"
conda-rattler-solver = "*"
conda-spawn = ">=0.1.0"

[environments]
runtime = { features = ["runtime"], no-default-feature = true }
```

In Pixi's `pyproject.toml` layout, the same Pixi sections live below
`[tool.pixi]`, for example `[tool.pixi.feature.runtime.dependencies]`.

## `[tool.pronto]`

`[tool.pronto]` records conda-pronto-specific build policy:

```toml
[tool.pronto]
environment = "runtime"
exclude = ["conda-libmamba-solver"]
docs-url = "https://example.com/demo/"
```

`environment`
: Name of the solved environment to turn into the runtime lock. When omitted,
  conda-pronto first tries `runtime`, then falls back to the default environment.

`exclude`
: Package names removed from the derived runtime lock, including dependencies
  used only by excluded packages.

`docs-url`
: Documentation URL stamped into generated runtime help output. The GitHub
  Action also exposes this as the `docs-url` input.

The older compatibility metadata fields are still accepted:

```toml
[tool.pronto]
channels = ["conda-forge"]
packages = [
  "python >=3.12",
  "conda >=25.1",
  "conda-rattler-solver",
  "conda-spawn >=0.1.0",
]
```

`packages`
: Specs shown in runtime metadata and used for live solves with `--no-lock`.
  Prefer conda workspace dependency sections for `conda.toml` projects.

`channels`
: Channels written into runtime metadata and the installed `.condarc` when the
  lockfile environment does not provide channels. Prefer `[workspace].channels`
  for `conda.toml` and `pixi.toml` projects, or `[tool.pixi.workspace].channels`
  for Pixi `pyproject.toml` projects.

## Stamped Runtime Metadata

`pronto build --name NAME` stamps these runtime values onto the staged binary:

- command name: `NAME` for `online` and `external`, `NAME` plus `z` for
  `embedded`
- display name: `NAME`
- default prefix: `~/.NAME`
- metadata file: `.NAME.json`
- bundle environment variable: uppercased `NAME` plus `_BUNDLE`
- offline environment variable: uppercased `NAME` plus `_OFFLINE`

Non-alphanumeric characters in environment variable names become underscores.

## Downstream Defaults

conda-pronto's repository default package set exists so the builder and runtime can be
tested. A downstream distribution makes its own package choices and passes them
through `pronto configure` or direct manifest edits before committing the
matching lockfile.

For example, conda-express owns the package set used when building `cx` and
`cxz`; those package choices are conda-express policy, not conda-pronto policy.
