# How Generated Runtimes Work

When you run `cs build`, conda-ship does not invent a new program from scratch.
It starts with a small generic runtime template, copies it to the resolved
command name, and writes your build data into that copy. The command name can
come from `[tool.conda-ship].command` or from `--command`.

Users rarely need to think about the template. They run the
finished runtime, such as `demo`, `demoz`, `cx`, or `cxz`.

## What `cs build` Writes

During a runtime build, conda-ship writes these details into the copied
binary:

- command and display name
- install scheme and install name
- runtime lock
- optional compressed package bundle
- documentation URL
- metadata filename
- bundle and offline environment variable names

That is what turns the same generic bootstrap code into a specific runtime
with its own command name, package set, help links, and install location.

## Where The Template Comes From

For packaged builds, the template is downloaded from conda-ship's GitHub
Release assets. The asset name includes the platform it runs on, for example:

```text
cs-runtime-template-x86_64-unknown-linux-gnu
cs-runtime-template-aarch64-apple-darwin
cs-runtime-template-x86_64-pc-windows-msvc.exe
```

You usually only see those names when wiring a packaging job. The GitHub Action
downloads the matching template automatically. A packaged `cs` CLI looks for
an installed `cs-runtime-template` automatically; `--template PATH` is an
override for custom packaging or cross-builds.

The template is not a runtime. Running it directly fails with a message that
points back to `cs build`; only the stamped copy has a command name,
lockfile, package metadata, and install policy.

When developing conda-ship itself from a source checkout, `--template` is
optional. In that mode, `cs build` compiles the local generic runtime before
writing the runtime.

## What Users See

The finished runtime has a small command surface:

- `bootstrap`: install conda into the runtime's install path
- `status`: report runtime and install details
- `shell`: start a conda-spawn subshell
- `uninstall`: remove the install path

All other commands are passed through to the installed conda executable after
bootstrap.

The base prefix is protected with a CEP 22 frozen marker. Users create named
environments for regular package work.

## What Each Project Chooses

Some runtime behavior is visible to users:

- conda-spawn based activation through `COMMAND shell`
- disabled `activate`, `deactivate`, and `init` commands with guidance
- automatic bootstrap before pass-through conda commands
- uninstall that removes the install path and prints a runtime-removal hint

The package set, command name, documentation URL, and release channel belong to
the project using conda-ship.
