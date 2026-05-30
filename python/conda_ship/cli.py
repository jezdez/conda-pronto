"""CLI adapter used by the ``conda ship`` plugin command."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def configure_parser(parser: argparse.ArgumentParser) -> None:
    """Configure the parser for ``conda ship``."""
    parser.add_argument(
        "ship_args",
        nargs=argparse.REMAINDER,
        metavar="ARGS",
        help="Arguments passed through to the cs executable.",
    )


def execute(args: argparse.Namespace) -> int:
    """Run ``cs`` and return its status code."""
    return run_cs(args.ship_args)


def main(argv: Sequence[str] | None = None) -> None:
    """Standalone debugging entry point for the plugin adapter."""
    raise SystemExit(run_cs(sys.argv[1:] if argv is None else argv))


def run_cs(argv: Sequence[str], *, executable: str | None = None) -> int:
    """Delegate to the canonical ``cs`` executable."""
    cs = executable or os.environ.get("CONDA_SHIP_EXECUTABLE") or installed_cs()
    if cs is None:
        print(
            "conda-ship could not find the `cs` executable on PATH.",
            file=sys.stderr,
        )
        return 127

    ship_args = list(argv)
    if ship_args[:1] == ["--"]:
        ship_args = ship_args[1:]
    if not ship_args:
        ship_args = ["--help"]

    try:
        return subprocess.run([cs, *ship_args]).returncode
    except FileNotFoundError:
        print(f"conda-ship could not execute {cs!r}.", file=sys.stderr)
        return 127


def installed_cs() -> str | None:
    """Find the ``cs`` executable installed with the current Python env."""
    binary = "cs.exe" if os.name == "nt" else "cs"
    env_binary = Path(sys.executable).with_name(binary)
    if env_binary.is_file():
        return str(env_binary)
    return shutil.which("cs")


if __name__ == "__main__":
    main()
