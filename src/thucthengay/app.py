"""Minimal command-line entrypoint for the application scaffold."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    """Run the placeholder app shell without requiring GUI or project data."""
    _ = sys.argv[1:] if argv is None else argv
    print("3.ThucTheNgay scaffold ready.")
    return 0
