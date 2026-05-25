"""CRS and raster-window helpers for the rendering pipeline.

Story 5.2: convert a geographic map window (WGS84) into raster pixel windows,
handling on-the-fly reprojection when the source raster CRS differs.

Performance notes:
- ``get_transformer`` is LRU-cached because pyproj Transformer construction is
  comparatively expensive and we may hit it once per layer per render call.
- ``geographic_window_to_raster_window`` densifies the four edges of the
  geographic bbox before reprojection (avoiding projection-curvature error
  from a 4-corner sample), but it does NOT iterate over pixels.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import numpy as np
import rasterio
from pyproj import CRS, Transformer
from rasterio.windows import Window, from_bounds

GEOGRAPHIC_CRS = "EPSG:4326"

Bbox = tuple[float, float, float, float]


@dataclass(frozen=True)
class WindowResolution:
    """Resolved read window plus the geographic extent actually covered."""

    window: Window
    covered_bbox: Bbox


@lru_cache(maxsize=64)
def get_transformer(src_crs: str, dst_crs: str) -> Transformer:
    """Return a cached pyproj ``Transformer`` for ``(src_crs, dst_crs)``."""
    return Transformer.from_crs(src_crs, dst_crs, always_xy=True)


def normalize_crs_key(crs: Any) -> str:
    """Normalize various CRS spellings to a hashable string usable as cache key."""
    if crs is None:
        msg = "Raster CRS is missing."
        raise ValueError(msg)
    return CRS.from_user_input(crs).to_string()


def _reproject_bbox(
    bbox: Bbox, transformer: Transformer, *, densify: int = 21
) -> Bbox:
    """Project a bbox edge-densified to target CRS."""
    min_x, min_y, max_x, max_y = bbox
    xs_lin = np.linspace(min_x, max_x, densify)
    ys_lin = np.linspace(min_y, max_y, densify)
    edge_x = np.concatenate(
        [xs_lin, np.full_like(ys_lin, max_x), xs_lin[::-1], np.full_like(ys_lin, min_x)]
    )
    edge_y = np.concatenate(
        [np.full_like(xs_lin, min_y), ys_lin, np.full_like(xs_lin, max_y), ys_lin[::-1]]
    )
    out_x, out_y = transformer.transform(edge_x, edge_y)
    return float(out_x.min()), float(out_y.min()), float(out_x.max()), float(out_y.max())


def geographic_window_to_raster_window(
    geo_bbox: Bbox,
    dataset: rasterio.io.DatasetReader,
) -> WindowResolution | None:
    """Resolve a WGS84 ``geo_bbox`` (min_lon, min_lat, max_lon, max_lat) on ``dataset``.

    Returns ``None`` if the geographic window does not overlap the raster.
    ``covered_bbox`` is clipped to the raster's bounds in WGS84 lon/lat.
    """
    raster_crs = normalize_crs_key(dataset.crs)

    if raster_crs == GEOGRAPHIC_CRS:
        bbox_in_raster: Bbox = geo_bbox
    else:
        forward = get_transformer(GEOGRAPHIC_CRS, raster_crs)
        bbox_in_raster = _reproject_bbox(geo_bbox, forward)

    ds_bounds = dataset.bounds
    inter_left = max(bbox_in_raster[0], ds_bounds.left)
    inter_bottom = max(bbox_in_raster[1], ds_bounds.bottom)
    inter_right = min(bbox_in_raster[2], ds_bounds.right)
    inter_top = min(bbox_in_raster[3], ds_bounds.top)
    if inter_left >= inter_right or inter_bottom >= inter_top:
        return None

    window = from_bounds(
        inter_left, inter_bottom, inter_right, inter_top, transform=dataset.transform
    )

    if raster_crs == GEOGRAPHIC_CRS:
        covered: Bbox = (inter_left, inter_bottom, inter_right, inter_top)
    else:
        inverse = get_transformer(raster_crs, GEOGRAPHIC_CRS)
        lon_min, lat_min, lon_max, lat_max = _reproject_bbox(
            (inter_left, inter_bottom, inter_right, inter_top), inverse
        )
        lon_min = max(lon_min, geo_bbox[0])
        lat_min = max(lat_min, geo_bbox[1])
        lon_max = min(lon_max, geo_bbox[2])
        lat_max = min(lat_max, geo_bbox[3])
        if lon_min >= lon_max or lat_min >= lat_max:
            return None
        covered = (lon_min, lat_min, lon_max, lat_max)

    return WindowResolution(window=window, covered_bbox=covered)
