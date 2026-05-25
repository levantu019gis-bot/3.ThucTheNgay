"""Export summary and log models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from thucthengay.models.issue import Issue


class ExportedComposition(BaseModel):
    """Composition successfully written to report outputs."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    slide_number: int = Field(ge=1)
    render_path: str


class SkippedComposition(BaseModel):
    """Composition omitted from export."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    reason: str


class ExportLog(BaseModel):
    """Traceable export result for PPTX/TXT output."""

    model_config = ConfigDict(extra="forbid")

    pptx_path: str | None = None
    txt_path: str | None = None
    slide_count: int = Field(default=0, ge=0)
    target_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    exported: list[ExportedComposition] = Field(default_factory=list)
    skipped: list[SkippedComposition] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
