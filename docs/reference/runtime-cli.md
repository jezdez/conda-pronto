# Runtime CLI Reference

Every conda-ship artifact includes a generated runtime. In this page,
`COMMAND` stands for the command name resolved by `cs build` from
`[tool.conda-ship].command` or `--command`.

For conda-express, `COMMAND` is `cx`. For an embedded conda-express artifact,
the staged runtime is `cxz`.

## Global Options

`-v, --verbose`
: Increase output detail.

`-q, --quiet`
: Suppress non-essential output.

`--path PATH`
: Use a custom install path instead of the distribution default. This applies to
  `bootstrap`, `status`, `shell`, `uninstall`, and pass-through conda commands.
  Put it before pass-through commands so conda does not interpret it as one of
  its own options, for example `COMMAND --path /tmp/demo install numpy`.

`-h, --help`
: Show runtime help.

`-V, --version`
: Show the runtime version.

## `COMMAND bootstrap`

Install conda into the runtime's install path.

```bash
COMMAND bootstrap [OPTIONS]
```

Options:

`--force`
: Remove an existing install path before bootstrapping again.

`--scheme SCHEME`
: Install with a named scheme instead of the stamped default. Currently
  supported: `conda`, which installs below `~/.conda/INSTALL_NAME`, and
  `data`, which installs below the platform user data directory. This is
  mutually exclusive with the global `--path` option.

`--lockfile PATH`
: Use an external rattler-lock file instead of the stamped runtime lock.

`--bundle DIR`
: Pre-populate the package cache from a directory containing `.conda` or
  `.tar.bz2` archives.

`--offline`
: Disable network access. Packages must be available from the local cache, an
  explicit `--bundle`, or an embedded bundle.

Examples:

```bash
# Standard network bootstrap from the stamped lockfile
COMMAND bootstrap

# Re-bootstrap into the default install path
COMMAND bootstrap --force

# Bootstrap into a custom install path
COMMAND --path /opt/name bootstrap

# Bootstrap from an external bundle directory
COMMAND bootstrap --bundle ./packages --offline
```

For an embedded runtime, conda-ship detects the built-in bundle
automatically:

```bash
COMMANDz bootstrap
```

An explicit `--bundle` still takes priority over the embedded bundle.

## `COMMAND status`

Show runtime and install details.

```bash
COMMAND [--path PATH] status [--scheme SCHEME]
```

The output includes the command name, runtime version, install path, configured
channels, configured package specs, installed package count, and conda
executable path.

## `COMMAND shell`

Start a conda-spawn subshell for an environment.

```bash
COMMAND shell [ENV]
```

Examples:

```bash
COMMAND shell myenv
exit
```

This command delegates to `conda spawn`. It uses the runtime's default install
path.

## `COMMAND uninstall`

Remove the install path and named environments.

```bash
COMMAND uninstall [OPTIONS]
```

Options:

`--scheme SCHEME`
: Remove the install path for a named scheme instead of the stamped default.
  Currently supported: `conda` and `data`. This is mutually exclusive with the
  global `--path` option.

`-y, --yes`
: Skip the interactive confirmation prompt.

The command removes the install path, attempts to remove named environments
cleanly, cleans PATH entries from common shell profiles, and prints a hint for
removing the runtime through the package manager or install method that
provided it.

## `COMMAND help`

Show the runtime help text.

```bash
COMMAND help
```

## Pass-Through Commands

Any command not listed above is passed through to the installed conda
executable after bootstrap:

```bash
COMMAND create -n myenv python=3.12 numpy
COMMAND install -n myenv pandas
COMMAND list -n myenv
COMMAND env list
COMMAND info

# Use a custom runtime install path for pass-through commands
COMMAND --path /tmp/name install -n myenv pandas
```

If the install path does not exist, pass-through commands automatically
bootstrap first.

## Disabled Shell Commands

Generated runtimes use conda-spawn for activation. These commands are
intercepted with runtime-specific guidance instead of being passed through:

- `COMMAND activate`
- `COMMAND deactivate`
- `COMMAND init`

Use `COMMAND shell ENV` instead of `conda activate ENV`.
