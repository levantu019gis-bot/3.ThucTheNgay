"""PowerPoint template metadata models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PlaceholderType(StrEnum):
    """Supported template placeholder roles."""

    MAP_IMAGE = "map_image"
    TEXT = "text"


class MapFrame(BaseModel):
    """Map image rectangle in template coordinate units."""

    model_config = ConfigDict(extra="forbid")

    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)


class TemplatePlaceholder(BaseModel):
    """Named shape placeholder in a target-specific PPTX template."""

    model_config = ConfigDict(extra="forbid")

    name: str
    kind: PlaceholderType
    fallback_id: str | None = None
    required: bool = True


class TemplateMetadata(BaseModel):
    """Metadata file consumed by export and validation services."""

    model_config = ConfigDict(extra="forbid")

    template_pptx: str
    slide_index: int = Field(ge=0)
    map_frame: MapFrame
    placeholders: list[TemplatePlaceholder] = Field(default_factory=list)
