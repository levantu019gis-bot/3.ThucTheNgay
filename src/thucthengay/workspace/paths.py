"""Workspace path layout helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

APP_OWNED_DIRS = ("cache", "compositions", "renders", "exports")
MANIFEST_FILENAME = "manifest.json"


@dataclass(frozen=True)
class WorkspacePaths:
    """Canonical filesystem paths inside one workspace root."""

    root: Path

    @property
    def manifest(self) -> Path:
        return self.root / MANIFEST_FILENAME

    @property
    def cache(self) -> Path:
        return self.root / "cache"

    @property
    def compositions(self) -> Path:
        return self.root / "compositions"

    @property
    def renders(self) -> Path:
        return self.root / "renders"

    @property
    def exports(self) -> Path:
        return self.root / "exports"

    @property
    def app_owned_dirs(self) -> tuple[Path, ...]:
        return (self.cache, self.compositions, self.renders, self.exports)

    def composition_file(self, composition_id: str) -> Path:
        if "/" in composition_id or "\\" in composition_id or composition_id in {"", ".", ".."}:
            msg = f"Invalid composition id for workspace path: {composition_id!r}"
            raise ValueError(msg)
        return self.compositions / f"{composition_id}.json"
