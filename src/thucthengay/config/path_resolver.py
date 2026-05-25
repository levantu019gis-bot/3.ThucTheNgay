"""Path resolution helpers for config and template metadata files."""

from __future__ import annotations

from pathlib import Path


def resolve_relative_to_file(owner_file: str | Path, value: str) -> Path:
    """Resolve a string path relative to the file that declares it."""
    path = Path(value)
    if path.is_absolute():
        return path
    return (Path(owner_file).resolve().parent / path).resolve()
