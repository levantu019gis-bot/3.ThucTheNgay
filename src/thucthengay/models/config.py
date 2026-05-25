"""Project configuration models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class GridInterval(BaseModel):
    """DMS-compatible grid interval."""

    model_config = ConfigDict(extra="forbid")

    degrees: int = Field(default=0, ge=0)
    minutes: int = Field(default=0, ge=0, lt=60)
    seconds: float = Field(default=0, ge=0, lt=60)

    @model_validator(mode="after")
    def interval_must_be_positive(self) -> GridInterval:
        if self.degrees == 0 and self.minutes == 0 and self.seconds == 0:
            msg = "grid interval must be greater than zero"
            raise ValueError(msg)
        return self


class GridConfig(BaseModel):
    """Target-level grid settings."""

    model_config = ConfigDict(extra="forbid")

    interval: GridInterval
    label_format: str = "dms_full"
    style: dict[str, Any] = Field(default_factory=dict)


class TargetExportConfig(BaseModel):
    """Target-specific export references."""

    model_config = ConfigDict(extra="forbid")

    template_metadata_file: str
    txt_line_template: str | None = None


class TargetConfig(BaseModel):
    """Configured reporting target."""

    model_config = ConfigDict(extra="forbid")

    id: str
    enabled: bool = True
    sort_order: int = 0
    name: str
    alias: str | None = None
    title: str | None = None
    geojson_file: str
    coordinate: list[float]
    scale: int = Field(gt=0)
    grid: GridConfig
    export: TargetExportConfig
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("coordinate")
    @classmethod
    def coordinate_must_be_lon_lat(cls, value: list[float]) -> list[float]:
        if len(value) != 2:
            msg = "coordinate must contain exactly [lon, lat]"
            raise ValueError(msg)
        lon, lat = value
        if not -180 <= lon <= 180:
            msg = "longitude must be between -180 and 180"
            raise ValueError(msg)
        if not -90 <= lat <= 90:
            msg = "latitude must be between -90 and 90"
            raise ValueError(msg)
        return value


class ProjectConfig(BaseModel):
    """Root project configuration."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    targets: list[TargetConfig]
