"""Shared render specification built from composition state.

Story 5.1: produce a normalized, immutable spec object that both preview and
final rendering paths can consume. The spec is derived (not persisted) and is
free of Qt dependencies.
"""

from __future__ import annotations

import math

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from thucthengay.models.composition import Composition
from thucthengay.models.config import GridConfig, TargetConfig
from thucthengay.models.issue import Issue, IssueScope, IssueSeverity
from thucthengay.models.template import MapFrame, TemplateMetadata

POINT_TO_INCH: float = 1.0 / 72.0
INCH_TO_METER: float = 0.0254
METERS_PER_DEGREE_LAT: float = 111_320.0


class RenderSpecError(Exception):
    """Raised when render spec inputs are invalid; carries structured issues."""

    def __init__(self, issues: list[Issue]) -> None:
        self.issues = issues
        super().__init__("; ".join(issue.message for issue in issues))


class GeoWindow(BaseModel):
    """Geographic bounding window in WGS84 lon/lat degrees."""

    model_config = ConfigDict(extra="forbid")

    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

    @model_validator(mode="after")
    def bounds_must_be_ordered(self) -> GeoWindow:
        if self.min_lon >= self.max_lon:
            msg = "min_lon must be < max_lon"
            raise ValueError(msg)
        if self.min_lat >= self.max_lat:
            msg = "min_lat must be < max_lat"
            raise ValueError(msg)
        return self


class RenderLayerRef(BaseModel):
    """Lightweight pointer to a visible layer in draw order."""

    model_config = ConfigDict(extra="forbid")

    layer_id: str
    source_path: str
    cache_path: str | None = None
    order: int = Field(ge=0)


class RenderBackground(BaseModel):
    """Background settings drawn beneath raster coverage."""

    model_config = ConfigDict(extra="forbid")

    color: str = "#FFFFFF"


class RenderSpec(BaseModel):
    """Normalized render specification consumed by preview and final renderers."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    output_width: int = Field(gt=0)
    output_height: int = Field(gt=0)
    view_center: list[float]
    view_scale: int = Field(gt=0)
    map_frame: MapFrame
    map_frame_aspect: float = Field(gt=0)
    geo_window: GeoWindow
    visible_layers: list[RenderLayerRef] = Field(default_factory=list)
    grid: GridConfig
    background: RenderBackground = Field(default_factory=RenderBackground)
    template_metadata_file: str
    template_pptx: str
    slide_index: int = Field(ge=0)

    @field_validator("view_center")
    @classmethod
    def view_center_must_be_lon_lat(cls, value: list[float]) -> list[float]:
        if len(value) != 2:
            msg = "view_center must contain exactly [lon, lat]"
            raise ValueError(msg)
        lon, lat = value
        if not -180 <= lon <= 180:
            msg = "view_center longitude must be between -180 and 180"
            raise ValueError(msg)
        if not -90 <= lat <= 90:
            msg = "view_center latitude must be between -90 and 90"
            raise ValueError(msg)
        return value


def _issue(
    issue_id: str,
    message: str,
    remediation: str,
    *,
    scope: IssueScope = IssueScope.RENDER,
    target_id: str | None = None,
    composition_id: str | None = None,
) -> Issue:
    return Issue(
        issue_id=issue_id,
        severity=IssueSeverity.ERROR,
        scope=scope,
        target_id=target_id,
        composition_id=composition_id,
        message=message,
        remediation=remediation,
    )


def _compute_geo_window(
    *, center_lon: float, center_lat: float, scale_denom: int, map_frame: MapFrame
) -> GeoWindow:
    """MVP geo window from scale + map frame physical size.

    Treats ``map_frame.width``/``height`` as PowerPoint points. Story 5.2 will
    refine with proper CRS transforms; this approximation keeps preview/final
    parity at this stage.
    """
    paper_width_m = map_frame.width * POINT_TO_INCH * INCH_TO_METER
    paper_height_m = map_frame.height * POINT_TO_INCH * INCH_TO_METER
    ground_width_m = paper_width_m * scale_denom
    ground_height_m = paper_height_m * scale_denom

    cos_lat = math.cos(math.radians(center_lat))
    meters_per_degree_lon = METERS_PER_DEGREE_LAT * max(cos_lat, 1e-6)

    half_w_deg = (ground_width_m / 2.0) / meters_per_degree_lon
    half_h_deg = (ground_height_m / 2.0) / METERS_PER_DEGREE_LAT

    return GeoWindow(
        min_lon=center_lon - half_w_deg,
        max_lon=center_lon + half_w_deg,
        min_lat=center_lat - half_h_deg,
        max_lat=center_lat + half_h_deg,
    )


def build_render_spec(
    *,
    composition: Composition,
    target: TargetConfig,
    template: TemplateMetadata,
    template_metadata_file: str,
    output_width: int,
    output_height: int,
) -> RenderSpec:
    """Build a :class:`RenderSpec` from composition + target + template + output size."""
    issues: list[Issue] = []

    if composition.target_id != target.id:
        issues.append(
            _issue(
                "render.spec.target_mismatch",
                "Composition và target không khớp.",
                (
                    f"Target id '{target.id}' không trùng với composition.target_id "
                    f"'{composition.target_id}'. Hãy chọn đúng target cho composition."
                ),
                target_id=target.id,
                composition_id=composition.composition_id,
            )
        )

    if output_width <= 0 or output_height <= 0:
        issues.append(
            _issue(
                "render.spec.output_size_invalid",
                "Kích thước output phải dương.",
                "Cung cấp output_width và output_height lớn hơn 0.",
                target_id=target.id,
                composition_id=composition.composition_id,
            )
        )

    if template.map_frame.width <= 0 or template.map_frame.height <= 0:
        issues.append(
            _issue(
                "render.spec.map_frame_invalid",
                "Kích thước map frame của template không hợp lệ.",
                "Kiểm tra template metadata: map_frame width/height phải > 0.",
                scope=IssueScope.TEMPLATE,
                target_id=target.id,
                composition_id=composition.composition_id,
            )
        )

    if issues:
        raise RenderSpecError(issues)

    visible_layers = sorted(
        (layer for layer in composition.layers if layer.visible),
        key=lambda layer: layer.order,
    )
    visible_refs = [
        RenderLayerRef(
            layer_id=layer.layer_id,
            source_path=layer.source_path,
            cache_path=layer.cache_path,
            order=layer.order,
        )
        for layer in visible_layers
    ]

    grid = composition.grid_override if composition.grid_override is not None else target.grid

    center_lon, center_lat = composition.view.center
    geo_window = _compute_geo_window(
        center_lon=center_lon,
        center_lat=center_lat,
        scale_denom=composition.view.scale,
        map_frame=template.map_frame,
    )

    map_frame_aspect = template.map_frame.width / template.map_frame.height

    return RenderSpec(
        composition_id=composition.composition_id,
        target_id=target.id,
        output_width=output_width,
        output_height=output_height,
        view_center=list(composition.view.center),
        view_scale=composition.view.scale,
        map_frame=template.map_frame,
        map_frame_aspect=map_frame_aspect,
        geo_window=geo_window,
        visible_layers=visible_refs,
        grid=grid,
        background=RenderBackground(),
        template_metadata_file=template_metadata_file,
        template_pptx=template.template_pptx,
        slide_index=template.slide_index,
    )
