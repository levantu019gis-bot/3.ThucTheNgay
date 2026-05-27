"""Composed map rendering pipeline."""

from __future__ import annotations

import rasterio

from thucthengay.models.issue import Issue, IssueScope, IssueSeverity
from thucthengay.render.frame import draw_coordinate_frame
from thucthengay.render.raster import (
    CancelCallback,
    DatasetOpener,
    RasterRenderResult,
    RenderError,
    render_raster_layers,
)
from thucthengay.render.spec import RenderSpec


def _cancelled_issue(spec: RenderSpec) -> Issue:
    return Issue(
        issue_id="render.cancelled",
        severity=IssueSeverity.ERROR,
        scope=IssueScope.RENDER,
        target_id=spec.target_id,
        composition_id=spec.composition_id,
        message="Render da bi huy.",
        remediation="Thuc hien lai render khi khong con thao tac moi hon dang cho.",
    )


def render_map(
    spec: RenderSpec,
    *,
    dataset_opener: DatasetOpener = rasterio.open,
    is_cancelled: CancelCallback | None = None,
) -> RasterRenderResult:
    """Render raster/background and overlay the MVP coordinate frame."""
    result = render_raster_layers(
        spec,
        dataset_opener=dataset_opener,
        is_cancelled=is_cancelled,
    )
    if is_cancelled is not None and is_cancelled():
        raise RenderError([*result.issues, _cancelled_issue(spec)])

    try:
        draw_coordinate_frame(result.canvas, spec)
    except RenderError as exc:
        raise RenderError([*result.issues, *exc.issues]) from exc
    return result
