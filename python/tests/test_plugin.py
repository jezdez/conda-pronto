from __future__ import annotations

import argparse

from conda_ship.plugin import conda_subcommands


def test_registers_ship_subcommand() -> None:
    subcommands = list(conda_subcommands())

    assert [subcommand.name for subcommand in subcommands] == ["ship"]


def test_subcommand_has_summary_and_actions() -> None:
    (subcommand,) = conda_subcommands()

    assert "conda runtimes" in subcommand.summary
    assert callable(subcommand.action)
    assert callable(subcommand.configure_parser)


def test_subcommand_configures_parser() -> None:
    (subcommand,) = conda_subcommands()
    parser = argparse.ArgumentParser(prog="conda ship")

    subcommand.configure_parser(parser)

    args = parser.parse_args(["lock", "--check"])
    assert args.ship_args == ["lock", "--check"]
