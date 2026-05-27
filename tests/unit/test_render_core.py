"""Tests for Story 5.3 composed map rendering."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import numpy as np
import pytest
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds

from thucthengay.gis.crs import GEOGRAPHIC_CRS
from thucthengay.models.config import GridConfig, GridInterval
from thucthengay.models.template import MapFrame
from thucthengay.render import (
    GeoWindow,
    RenderBackground,
    RenderError,
    RenderLayerRef,
    RenderSpec,
    draw_coordinate_frame,
    render_map,
)


def _spec(
    *,
    layers: list[RenderLayerRef],
    bg_color: str = "#112233",
    interval: GridInterval | None = None,
) -> RenderSpec:
    return RenderSpec(
        composition_id="tgt__20260525",
        target_id="tgt",
        output_width=64,
        output_height=48,
        view_center=[106.5, 10.5],
        view_scale=50000,
        map_frame=MapFrame(x=0, y=0, width=640, height=360),
        map_frame_aspect=640 / 360,
        geo_window=GeoWindow(min_lon=106.0, min_lat=10.0, max_lon=107.0, max_lat=11.0),
        visible_layers=layers,
        grid=GridConfig(interval=interval or GridInterval(minutes=30), label_format="dms_full"),
        background=RenderBackground(color=bg_color),
        template_metadata_file="t.json",
        template_pptx="t.pptx",
        slide_index=0,
    )


def _make_memfile(
    *,
    bounds: tuple[float, float, float, float],
    rgb: tuple[int, int, int],
    width: int = 32,
    height: int = 32,
) -> MemoryFile:
    data = np.zeros((3, height, width), dtype=np.uint8)
    data[0, :, :] = rgb[0]
    data[1, :, :] = rgb[1]
    data[2, :, :] = rgb[2]
    memfile = MemoryFile()
    with memfile.open(
        driver="GTiff",
        width=width,
        height=height,
        count=3,
        dtype="uint8",
        crs=GEOGRAPHIC_CRS,
        transform=from_bounds(*bounds, width, height),
    ) as ds:
        ds.write(data)
    return memfile


@contextmanager
def _opener_for(
    mapping: dict[str, MemoryFile],
    *,
    unreadable_paths: set[str] | None = None,
) -> Iterator[callable]:
    unreadable_paths = unreadable_paths or set()
    handles: list = []

    def opener(path: str) -> rasterio.DatasetReader:
        if path in unreadable_paths:
            raise rasterio.RasterioIOError(f"Synthetic open failure for {path!r}")
        ds = mapping[path].open()
        handles.append(ds)
        return ds

    try:
        yield opener
    finally:
        for ds in handles:
            ds.close()
        for memfile in mapping.values():
            memfile.close()


class TestRenderMap:
    def test_background_survives_uncovered_raster_area_and_frame_is_drawn(self) -> None:
        memfile = _make_memfile(bounds=(106.0, 10.0, 106.5, 11.0), rgb=(80, 90, 100))
        layer = RenderLayerRef(layer_id="L1", source_path="L1.tif", cache_path="L1.tif", order=0)

        with _opener_for({"L1.tif": memfile}) as opener:
            result = render_map(_spec(layers=[layer]), dataset_opener=opener)

        assert tuple(result.canvas[24, 8].tolist()) == (80, 90, 100)
        assert tuple(result.canvas[24, 56].tolist()) == (17, 34, 51)
        assert tuple(result.canvas[0, 32].tolist()) != (17, 34, 51)

    def test_preserves_non_fatal_raster_issues(self) -> None:
        good = _make_memfile(bounds=(106.0, 10.0, 107.0, 11.0), rgb=(40, 50, 60))
        layers = [
            RenderLayerRef(layer_id="BAD", source_path="bad.tif", cache_path="bad.tif", order=0),
            RenderLayerRef(layer_id="OK", source_path="ok.tif", cache_path="ok.tif", order=1),
        ]

        with _opener_for({"ok.tif": good}, unreadable_paths={"bad.tif"}) as opener:
            result = render_map(_spec(layers=layers), dataset_opener=opener)

        assert result.painted_layer_ids == ("OK",)
        assert [issue.issue_id for issue in result.issues] == ["render.raster.unreadable"]

    def test_mvp_does_not_draw_boundary_north_arrow_or_scale_bar(self) -> None:
        spec = _spec(layers=[], bg_color="#112233", interval=GridInterval(degrees=1))
        result = render_map(spec)

        expected = np.zeros_like(result.canvas)
        expected[:, :] = (17, 34, 51)
        draw_coordinate_frame(expected, spec)

        assert np.array_equal(result.canvas, expected)

    def test_frame_error_preserves_prior_raster_issues(self) -> None:
        good = _make_memfile(bounds=(106.0, 10.0, 107.0, 11.0), rgb=(40, 50, 60))
        layers = [
            RenderLayerRef(layer_id="BAD", source_path="bad.tif", cache_path="bad.tif", order=0),
            RenderLayerRef(layer_id="OK", source_path="ok.tif", cache_path="ok.tif", order=1),
        ]
        spec = _spec(layers=layers)
        spec.grid.label_format = "unsupported"

        with _opener_for({"ok.tif": good}, unreadable_paths={"bad.tif"}) as opener:
            with pytest.raises(RenderError) as exc:
                render_map(spec, dataset_opener=opener)

        assert [issue.issue_id for issue in exc.value.issues] == [
            "render.raster.unreadable",
            "render.frame.label_format_invalid",
        ]

    def test_cancellation_after_raster_before_frame_raises_structured_issue(self) -> None:
        with pytest.raises(RenderError) as exc:
            render_map(
                _spec(layers=[], bg_color="#112233", interval=GridInterval(degrees=1)),
                is_cancelled=lambda: True,
            )

        assert [issue.issue_id for issue in exc.value.issues] == ["render.cancelled"]
