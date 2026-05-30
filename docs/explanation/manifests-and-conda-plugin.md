# Manifests And Plugin Entry Points

conda-pronto supports conda-native manifests and Pixi manifests.

conda-pronto is not an environment manager. It consumes a solved conda environment
and turns it into runtimes.

## Manifest Priority

conda-pronto treats {external+conda-workspaces:doc}`conda.toml <reference/conda-toml-spec>`
as the preferred project manifest. `pixi.toml` and Pixi's `pyproject.toml`
layout are supported when a downstream project already keeps its conda solve in
Pixi.

Inside a build root, conda-pronto looks for manifests in this order:

1. `conda.toml`
2. `pixi.toml`
3. `pyproject.toml` when it contains `[tool.pixi]`

When `conda.toml` is selected, conda-pronto reads package records from `conda.lock`.
When `pixi.toml` or Pixi's `pyproject.toml` is selected, it reads package
records from `pixi.lock`.

The lockfile remains the source of concrete package records. If the selected
lockfile is missing, create it with the tool that owns the manifest, then run
`pronto lock` again.

## Runtime Environment Selection

The solved environment used for the runtime is selected by
`[tool.pronto].source-environment`:

```toml
[tool.pronto]
source-environment = "runtime"
exclude = ["conda-libmamba-solver"]
docs-url = "https://example.com/demo/"
```

If `source-environment` is omitted, conda-pronto first looks for a solved
environment named `runtime`. If that is not present, it uses the lockfile's
default environment.

conda-pronto writes a new generated lock at `target/pronto/runtime.lock`. That lock
contains only the selected runtime environment, renamed to `default` for the
generated runtime. It is build output, not another source project
lockfile.

## Conda Workspace Shape

A conda-native conda-pronto project puts conda intent in the
{external+conda-workspaces:doc}`conda-workspaces schema <reference/conda-toml-spec>`
and conda-pronto-specific build policy in `[tool.pronto]`:

```toml
[workspace]
name = "demo"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]

[feature.runtime.dependencies]
python = ">=3.12"
conda = ">=25.1"
conda-rattler-solver = "*"
conda-spawn = ">=0.1.0"

[environments]
runtime = { features = ["runtime"], no-default-feature = true }

[tool.pronto]
source-environment = "runtime"
exclude = ["conda-libmamba-solver"]
```

`[tool.pronto]` is for conda-pronto build behavior: which source environment to
turn into a runtime, which packages to prune after the solve, artifact naming
policy, bundle policy, and runtime documentation links.

Package and channel intent belongs in the
{external+conda-workspaces:doc}`conda workspace sections <reference/conda-toml-spec>`
when that manifest is available. conda-pronto reads the selected lockfile
environment and stamps the resolved package names and channel URLs into runtime
metadata for status output and live-solve defaults.

For Pixi projects that keep Pixi config in `pyproject.toml`, use Pixi's
`[tool.pixi.*]` table names, such as `[tool.pixi.workspace]` and
`[tool.pixi.feature.runtime.dependencies]`. `[tool.pronto]` remains a separate
tool table because it configures conda-pronto, not Pixi.

## CLI Entry Points

`pronto ...` is the primary command. When `conda-pronto` is installed in a
conda environment, `conda pronto ...` can also be available as a conda-style
shortcut for the same builder:

- `pronto ...` remains the primary CLI.
- `conda pronto ...` runs the installed `pronto` executable.
- conda-pronto does not require this shortcut to work.
- the shortcut does not make conda-pronto part of conda itself.

The builder identity remains `pronto`, and downstream distributions still own
the runtimes they publish.

The Python adapter first looks for the `pronto` executable next to the current
Python interpreter, then falls back to `PATH`. Conda recipes for
`conda-pronto` package the Rust-built `pronto` binary and the adapter in the
same environment. For adapter tests or custom packaging,
`CONDA_PRONTO_EXECUTABLE` points at a specific executable.

## Runtime Template Boundary

The downstream project manifest lives in the downstream repository. The
conda-pronto builder and generic runtime template come from the conda-pronto
release or package installation.

`pronto build --template PATH` copies the prebuilt template, stamps the
copy with the command name, install scheme and install name, runtime lock, metadata, and optional embedded
bundle. That stamped copy is the runtime. conda-pronto then writes the
staged artifacts to the downstream project's output
directory. Source checkouts can omit `--template` while changing
conda-pronto itself; that fallback builds `pronto-runtime` locally with Cargo.
