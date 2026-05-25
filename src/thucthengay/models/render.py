"""Render result models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from thucthengay.models.issue import Issue


class RenderResult(BaseModel):
    """Metadata recorded after preview or final render."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    output_path: str
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    center: list[float]
    scale: int = Field(gt=0)
    layer_ids: list[str] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)

    @field_validator("center")
    @classmethod
    def center_must_be_lon_lat(cls, value: list[float]) -> list[float]:
        if len(value) != 2:
            msg = "center must contain exactly [lon, lat]"
            raise ValueError(msg)
        lon, lat = value
        if not -180 <= lon <= 180:
            msg = "center longitude must be between -180 and 180"
            raise ValueError(msg)
        if not -90 <= lat <= 90:
            msg = "center latitude must be between -90 and 90"
            raise ValueError(msg)
        return value
