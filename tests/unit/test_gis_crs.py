"""Tests for Story 5.2: CRS/window helpers in thucthengay.gis.crs."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import numpy as np
import pytest
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds

from thucthengay.gis.crs import (
    GEOGRAPHIC_CRS,
    dataset_geographic_bbox,
    geographic_window_to_raster_window,
    get_transformer,
    normalize_crs_key,
)


@contextmanager
def _synthetic_dataset(
    *,
    bounds: tuple[float, float, float, float],
    crs: str,
    width: int = 64,
    height: int = 64,
    fill: int = 200,
) -> Iterator[rasterio.DatasetReader]:
    """Yield a tiny in-memory GeoTIFF dataset for testing."""
    left, bottom, right, top = bounds
    transform = from_bounds(left, bottom, right, top, width, height)
    data = np.full((3, height, width), fill, dtype=np.uint8)
    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": 3,
        "dtype": "uint8",
        "crs": crs,
        "transform": transform,
    }
    with MemoryFile() as memfile:
        with memfile.open(**profile) as dataset:
            dataset.write(data)
        with memfile.open() as dataset:
            yield dataset


class TestNormalizeCrsKey:
    def test_returns_canonical_string(self) -> None:
        assert normalize_crs_key("EPSG:4326").startswith("EPSG:4326")

    def test_raises_when_crs_missing(self) -> None:
        with pytest.raises(ValueError, match="CRS"):
            normalize_crs_key(None)


class TestTransformerCache:
    def test_returns_cached_instance(self) -> None:
        a = get_transformer("EPSG:4326", "EPSG:3857")
        b = get_transformer("EPSG:4326", "EPSG:3857")
        assert a is b


class TestDatasetGeographicBbox:
    def test_returns_bounds_for_geographic_dataset(self) -> None:
        with _synthetic_dataset(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS
        ) as ds:
            assert dataset_geographic_bbox(ds) == pytest.approx((106.0, 10.0, 107.0, 11.0))

    def test_reprojects_projected_bounds_to_wgs84(self) -> None:
        forward = get_transformer(GEOGRAPHIC_CRS, "EPSG:3857")
        x0, y0 = forward.transform(106.0, 10.0)
        x1, y1 = forward.transform(107.0, 11.0)
        with _synthetic_dataset(
            bounds=(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)),
            crs="EPSG:3857",
        ) as ds:
            bbox = dataset_geographic_bbox(ds)

        assert bbox == pytest.approx((106.0, 10.0, 107.0, 11.0), abs=0.01)


class TestGeographicWindowToRasterWindowSameCrs:
    def test_full_overlap_returns_window_and_bbox(self) -> None:
        with _synthetic_dataset(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS
        ) as ds:
            geo = (106.25, 10.25, 106.75, 10.75)
            res = geographic_window_to_raster_window(geo, ds)

        assert res is not None
        assert res.covered_bbox == pytest.approx(geo)
        assert res.window.width > 0
        assert res.window.height > 0

    def test_partial_overlap_clips_to_raster_bounds(self) -> None:
        with _synthetic_dataset(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS
        ) as ds:
            geo = (106.5, 10.5, 107.5, 11.5)  # half outside
            res = geographic_window_to_raster_window(geo, ds)

        assert res is not None
        assert res.covered_bbox == pytest.approx((106.5, 10.5, 107.0, 11.0))

    def test_no_overlap_returns_none(self) -> None:
        with _synthetic_dataset(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS
        ) as ds:
            geo = (110.0, 20.0, 111.0, 21.0)
            res = geographic_window_to_raster_window(geo, ds)

        assert res is None


class TestGeographicWindowToRasterWindowCrossCrs:
    def test_projected_crs_window_resolves(self) -> None:
        # Web Mercator bounds roughly equivalent to lon 106..107, lat 10..11
        forward = get_transformer(GEOGRAPHIC_CRS, "EPSG:3857")
        x0, y0 = forward.transform(106.0, 10.0)
        x1, y1 = forward.transform(107.0, 11.0)
        with _synthetic_dataset(
            bounds=(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)),
            crs="EPSG:3857",
        ) as ds:
            geo = (106.25, 10.25, 106.75, 10.75)
            res = geographic_window_to_raster_window(geo, ds)

        assert res is not None
        # Covered bbox should still be roughly inside the requested geo window
        cmin_lon, cmin_lat, cmax_lon, cmax_lat = res.covered_bbox
        assert 106.2 <= cmin_lon <= 106.3
        assert 106.7 <= cmax_lon <= 106.8
        assert 10.2 <= cmin_lat <= 10.3
        assert 10.7 <= cmax_lat <= 10.8
