"""Workspace manifest models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceManifest(BaseModel):
    """Top-level workspace manifest."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    config_path: str
    imagery_input_path: str | None = None
    composition_ids: list[str] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
