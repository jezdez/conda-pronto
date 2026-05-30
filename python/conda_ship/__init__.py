"""Conda plugin adapter for conda-ship."""

from __future__ import annotations

try:
    from importlib.metadata import version
except ImportError:  # pragma: no cover
    from importlib_metadata import version


try:
    __version__ = version("conda-ship")
except Exception:  # pragma: no cover
    __version__ = "0+unknown"
