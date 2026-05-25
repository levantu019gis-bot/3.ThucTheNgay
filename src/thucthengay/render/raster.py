"""Raster compositing core for the rendering pipeline.

Story 5.2: read each visible raster layer through a windowed/decimated path,
reproject on-the-fly with ``WarpedVRT`` when needed, and composite into a
single uint8 RGB canvas sized ``(spec.output_height, spec.output_width, 3)``.

Performance:
- ``rasterio.windows.from_bounds`` + ``out_shape=`` ensures GDAL reads the
  smallest possible window at the target decimation; no full-raster loads.
- ``WarpedVRT`` performs CRS reprojection during the read call without writing
  intermediate files. We instantiate it only when CRS differs from WGS84.
- One preallocated canvas, in-place paste, ``uint8`` dtype throughout.
- ``dataset_opener`` injection lets tests pass synthetic ``MemoryFile`` datasets
  without touching disk and keeps the module Qt-free.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.io import DatasetReader
from rasterio.vrt import WarpedVRT

from thucthengay.gis.crs import (
    GEOGRAPHIC_CRS,
    geographic_window_to_raster_window,
    normalize_crs_key,
)
from thucthengay.models.issue import Issue, IssueScope, IssueSeverity
from thucthengay.render.spec import RenderLayerRef, RenderSpec

DatasetOpener = Callable[[str], "rasterio.DatasetReader"]


class RenderError(Exception):
    """Raised when rendering cannot produce any output; carries structured issues."""

    def __init__(self, issues: list[Issue]) -> None:
        self.issues = issues
        super().__init__("; ".join(issue.message for issue in issues))


def _parse_hex_color(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    if len(text) != 6:
        msg = f"Background color must be #RRGGBB, got {value!r}"
        raise ValueError(msg)
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def _issue(
    issue_id: str,
    message: str,
    remediation: str,
    *,
    layer_id: str | None,
    composition_id: str | None,
    target_id: str | None,
) -> Issue:
    return Issue(
        issue_id=issue_id,
        severity=IssueSeverity.ERROR,
        scope=IssueScope.RENDER,
        target_id=target_id,
        composition_id=composition_id,
        layer_id=layer_id,
        message=message,
        remediation=remediation,
    )


@contextmanager
def _open_layer(
    layer: RenderLayerRef, opener: DatasetOpener
) -> Iterator[DatasetReader]:
    path = layer.cache_path or layer.source_path
    ds = opener(path)
    try:
        yield ds
    finally:
        ds.close()


def _geo_to_pixel(
    canvas_w: int,
    canvas_h: int,
    geo_bbox: tuple[float, float, float, float],
    target_bbox: tuple[float, float, float, float],
) -> tuple[int, int, int, int]:
    """Map ``target_bbox`` (WGS84) into integer pixel coords on the canvas."""
    min_lon, min_lat, max_lon, max_lat = geo_bbox
    tlon0, tlat0, tlon1, tlat1 = target_bbox
    w_lon = max_lon - min_lon
    h_lat = max_lat - min_lat
    col0 = int(round((tlon0 - min_lon) / w_lon * canvas_w))
    col1 = int(round((tlon1 - min_lon) / w_lon * canvas_w))
    row0 = int(round((max_lat - tlat1) / h_lat * canvas_h))
    row1 = int(round((max_lat - tlat0) / h_lat * canvas_h))
    col0 = max(0, min(canvas_w, col0))
    col1 = max(0, min(canvas_w, col1))
    row0 = max(0, min(canvas_h, row0))
    row1 = max(0, min(canvas_h, row1))
    return row0, row1, col0, col1


def _read_layer_into(
    *,
    dataset: DatasetReader,
    geo_bbox: tuple[float, float, float, float],
    canvas: np.ndarray,
) -> bool:
    """Read ``dataset`` into the ``canvas`` region corresponding to its overlap.

    Returns ``True`` if pixels were written, ``False`` if no overlap.
    """
    raster_crs = normalize_crs_key(dataset.crs)
    use_vrt = raster_crs != GEOGRAPHIC_CRS

    src: DatasetReader
    if use_vrt:
        src = WarpedVRT(dataset, crs=GEOGRAPHIC_CRS, resampling=Resampling.bilinear)
    else:
        src = dataset

    try:
        resolution = geographic_window_to_raster_window(geo_bbox, src)
        if resolution is None:
            return False

        canvas_h, canvas_w = canvas.shape[:2]
        row0, row1, col0, col1 = _geo_to_pixel(
            canvas_w, canvas_h, geo_bbox, resolution.covered_bbox
        )
        out_h = row1 - row0
        out_w = col1 - col0
        if out_h <= 0 or out_w <= 0:
            return False

        band_count = src.count
        read_bands = (1, 2, 3) if band_count >= 3 else (1,)
        data = src.read(
            indexes=read_bands,
            window=resolution.window,
            out_shape=(len(read_bands), out_h, out_w),
            resampling=Resampling.bilinear,
        )
        if data.dtype != np.uint8:
            data = np.clip(data, 0, 255).astype(np.uint8)

        if len(read_bands) == 1:
            rgb = np.repeat(data, 3, axis=0)
        else:
            rgb = data

        canvas[row0:row1, col0:col1, :] = np.transpose(rgb, (1, 2, 0))
        return True
    finally:
        if use_vrt:
            src.close()


def render_raster_layers(
    spec: RenderSpec,
    *,
    dataset_opener: DatasetOpener = rasterio.open,
) -> np.ndarray:
    """Composite visible raster layers into a single uint8 RGB canvas.

    Layers are drawn in ``spec.visible_layers`` order (lower ``order`` first);
    later layers overwrite earlier pixels where they cover.
    Per-layer IO/CRS failures are collected as ``Issue``s; rendering proceeds
    on remaining layers. If *no* layer is successfully drawn AND at least one
    issue was recorded, ``RenderError`` is raised.
    """
    geo_bbox = (
        spec.geo_window.min_lon,
        spec.geo_window.min_lat,
        spec.geo_window.max_lon,
        spec.geo_window.max_lat,
    )

    bg = _parse_hex_color(spec.background.color)
    canvas = np.empty((spec.output_height, spec.output_width, 3), dtype=np.uint8)
    canvas[..., 0] = bg[0]
    canvas[..., 1] = bg[1]
    canvas[..., 2] = bg[2]

    issues: list[Issue] = []
    painted = 0

    for layer in spec.visible_layers:
        try:
            with _open_layer(layer, dataset_opener) as dataset:
                if dataset.crs is None:
                    issues.append(
                        _issue(
                            "render.raster.crs_missing",
                            f"Layer '{layer.layer_id}' không có CRS.",
                            "Kiểm tra GeoTIFF có gắn CRS hợp lệ (ví dụ EPSG:4326).",
                            layer_id=layer.layer_id,
                            composition_id=spec.composition_id,
                            target_id=spec.target_id,
                        )
                    )
                    continue
                if _read_layer_into(dataset=dataset, geo_bbox=geo_bbox, canvas=canvas):
                    painted += 1
        except (rasterio.RasterioIOError, OSError, ValueError) as exc:
            issues.append(
                _issue(
                    "render.raster.unreadable",
                    f"Không đọc được layer '{layer.layer_id}': {exc}",
                    "Kiểm tra đường dẫn file và quyền đọc; thử mở lại bằng QGIS để xác minh.",
                    layer_id=layer.layer_id,
                    composition_id=spec.composition_id,
                    target_id=spec.target_id,
                )
            )

    if painted == 0 and issues:
        raise RenderError(issues)

    return canvas
