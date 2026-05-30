# Manifests And Plugin Entry Points

conda-ship supports conda-workspaces manifests and Pixi manifests.

conda-ship is not an environment manager. It consumes a solved conda environment
and turns it into runtimes.

## Manifest Priority

conda-ship treats {external+conda-workspaces:doc}`conda.toml <reference/conda-toml-spec>`
as the preferred project manifest. The conda-workspaces `pyproject.toml`
embedded form with `[tool.conda]` is also supported. `pixi.toml` and
`pyproject.toml` with `[tool.pixi]` are supported when a downstream project
already keeps its conda solve in Pixi.

Inside a build root, conda-ship looks for manifests in this order:

1. `conda.toml`
2. `pixi.toml`
3. `pyproject.toml` when it contains `[tool.conda]` or `[tool.pixi]`

When `conda.toml` is selected, conda-ship reads package records from `conda.lock`.
When `pyproject.toml` with `[tool.conda]` is selected, it also reads package
records from `conda.lock`. When `pixi.toml` or `pyproject.toml` with
`[tool.pixi]` is selected, it reads package records from `pixi.lock`.
If a `pyproject.toml` contains both `[tool.conda]` and `[tool.pixi]`,
`[tool.conda]` wins.

The lockfile remains the source of concrete package records. If the selected
lockfile is missing, create it with the tool that owns the manifest, then run
`cs inspect` or `cs build --dry-run` again.

## Runtime Environment Selection

The solved environment used for the runtime is selected by
`[tool.conda-ship].source-environment`:

```toml
[tool.conda-ship]
command = "demo"
layout = "online"
source-environment = "runtime"
exclude = ["conda-libmamba-solver"]
docs-url = "https://example.com/demo/"
```

If `source-environment` is omitted, conda-ship first looks for a solved
environment named `runtime`. If that is not present, it uses the lockfile's
default environment.

conda-ship derives a runtime lock that contains only the selected runtime
environment, renamed to `default` for the generated runtime. The derived lock is
stamped into staged runtimes and copied into the staged artifact directory. It
is build output, not another source project lockfile.

## Conda Workspace Shape

A conda-workspaces project puts conda intent in the
{external+conda-workspaces:doc}`conda-workspaces schema <reference/conda-toml-spec>`
and conda-ship-specific build policy in `[tool.conda-ship]`:

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

[tool.conda-ship]
command = "demo"
layout = "online"
source-environment = "runtime"
exclude = ["conda-libmamba-solver"]
```

`[tool.conda-ship]` is for conda-ship build behavior: which source environment to
turn into a runtime, which packages to prune after the solve, artifact naming
policy, bundle policy, and runtime documentation links.

Package and channel intent belongs in the
{external+conda-workspaces:doc}`conda workspace sections <reference/conda-toml-spec>`
when that manifest is available. conda-ship reads the selected lockfile
environment and stamps the resolved package names and channel URLs into runtime
metadata for status output.

For conda-workspaces projects that keep conda config in `pyproject.toml`, use
`[tool.conda.*]` table names, such as `[tool.conda.workspace]` and
`[tool.conda.feature.runtime.dependencies]`. For Pixi projects, use Pixi's
`[tool.pixi.*]` table names, such as `[tool.pixi.workspace]` and
`[tool.pixi.feature.runtime.dependencies]`. `[tool.conda-ship]` remains a separate
tool table because it configures conda-ship, not the workspace solver.

## CLI Entry Points

`cs ...` is the primary command. When `conda-ship` is installed in a
conda environment, `conda ship ...` can also be available as a conda-style
shortcut for the same builder:

- `cs ...` remains the primary CLI.
- `conda ship ...` runs the installed `cs` executable.
- conda-ship does not require this shortcut to work.
- the shortcut does not make conda-ship part of conda itself.

The builder identity remains `cs`, and downstream distributions still own
the runtimes they publish.

The Python adapter first looks for the `cs` executable next to the current
Python interpreter, then falls back to `PATH`. Conda recipes for
`conda-ship` package the Rust-built `cs` binary and the adapter in the
same environment. For adapter tests or custom packaging,
`CONDA_SHIP_EXECUTABLE` points at a specific executable.

## Runtime Template Boundary

The downstream project manifest lives in the downstream repository. The
conda-ship builder and generic runtime template come from the conda-ship
release or package installation.

`cs build` copies the selected template, stamps the copy with the command
name, install scheme and install name, runtime lock, metadata, and optional
embedded bundle. That stamped copy is the runtime. conda-ship then writes the
staged artifacts to the downstream project's output directory. Source checkouts
can omit `--template` while changing conda-ship itself; that fallback builds
`conda-ship-runtime` locally with Cargo.
