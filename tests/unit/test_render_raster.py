"""Tests for Story 5.2: render_raster_layers compositing."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import numpy as np
import pytest
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds

from thucthengay.gis.crs import GEOGRAPHIC_CRS, get_transformer
from thucthengay.models.config import GridConfig, GridInterval
from thucthengay.models.template import MapFrame
from thucthengay.render import (
    GeoWindow,
    RenderBackground,
    RenderError,
    RenderLayerRef,
    RenderSpec,
    render_raster_layers,
)


def _spec(
    *,
    layers: list[RenderLayerRef],
    geo: tuple[float, float, float, float] = (106.0, 10.0, 107.0, 11.0),
    width: int = 32,
    height: int = 32,
    bg_color: str = "#FFFFFF",
) -> RenderSpec:
    return RenderSpec(
        composition_id="tgt__20260525",
        target_id="tgt",
        output_width=width,
        output_height=height,
        view_center=[(geo[0] + geo[2]) / 2, (geo[1] + geo[3]) / 2],
        view_scale=50000,
        map_frame=MapFrame(x=0, y=0, width=640, height=360),
        map_frame_aspect=640 / 360,
        geo_window=GeoWindow(
            min_lon=geo[0], min_lat=geo[1], max_lon=geo[2], max_lat=geo[3]
        ),
        visible_layers=layers,
        grid=GridConfig(interval=GridInterval(minutes=1)),
        background=RenderBackground(color=bg_color),
        template_metadata_file="t.json",
        template_pptx="t.pptx",
        slide_index=0,
    )


def _make_memfile(
    *,
    bounds: tuple[float, float, float, float],
    crs: str,
    rgb: tuple[int, int, int],
    width: int = 32,
    height: int = 32,
) -> MemoryFile:
    """Return an open MemoryFile holding a tiny GeoTIFF; caller closes it."""
    left, bottom, right, top = bounds
    transform = from_bounds(left, bottom, right, top, width, height)
    data = np.zeros((3, height, width), dtype=np.uint8)
    data[0, :, :] = rgb[0]
    data[1, :, :] = rgb[1]
    data[2, :, :] = rgb[2]
    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": 3,
        "dtype": "uint8",
        "crs": crs,
        "transform": transform,
    }
    memfile = MemoryFile()
    with memfile.open(**profile) as ds:
        ds.write(data)
    return memfile


@contextmanager
def _opener_for(
    mapping: dict[str, MemoryFile],
    *,
    unreadable_paths: set[str] | None = None,
) -> Iterator[callable]:
    """Yield a ``dataset_opener`` callable backed by an in-memory registry."""
    unreadable_paths = unreadable_paths or set()
    handles: list = []

    def opener(path: str) -> rasterio.DatasetReader:
        if path in unreadable_paths:
            raise rasterio.RasterioIOError(f"Synthetic open failure for {path!r}")
        memfile = mapping.get(path)
        if memfile is None:
            raise rasterio.RasterioIOError(f"Unknown synthetic path {path!r}")
        ds = memfile.open()
        handles.append(ds)
        return ds

    try:
        yield opener
    finally:
        for ds in handles:
            ds.close()
        for memfile in mapping.values():
            memfile.close()


class TestSingleLayerHappyPath:
    def test_layer_pixels_overwrite_background(self) -> None:
        memfile = _make_memfile(
            bounds=(106.0, 10.0, 107.0, 11.0),
            crs=GEOGRAPHIC_CRS,
            rgb=(10, 20, 30),
        )
        layer = RenderLayerRef(
            layer_id="L1", source_path="L1.tif", cache_path="L1.tif", order=0
        )
        spec = _spec(layers=[layer], width=16, height=16, bg_color="#FFFFFF")

        with _opener_for({"L1.tif": memfile}) as opener:
            canvas = render_raster_layers(spec, dataset_opener=opener)

        assert canvas.shape == (16, 16, 3)
        assert canvas.dtype == np.uint8
        # Center pixel should be from the layer, not the background
        cy, cx = 8, 8
        assert tuple(canvas[cy, cx].tolist()) == (10, 20, 30)


class TestCrsMismatch:
    def test_projected_crs_reads_through_warped_vrt(self) -> None:
        forward = get_transformer(GEOGRAPHIC_CRS, "EPSG:3857")
        x0, y0 = forward.transform(106.0, 10.0)
        x1, y1 = forward.transform(107.0, 11.0)
        memfile = _make_memfile(
            bounds=(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)),
            crs="EPSG:3857",
            rgb=(50, 60, 70),
        )
        layer = RenderLayerRef(
            layer_id="L1", source_path="L1.tif", cache_path="L1.tif", order=0
        )
        spec = _spec(layers=[layer], width=16, height=16)

        with _opener_for({"L1.tif": memfile}) as opener:
            canvas = render_raster_layers(spec, dataset_opener=opener)

        # Layer fills the whole geo_window — center pixel must not be background
        assert tuple(canvas[8, 8].tolist()) == (50, 60, 70)


class TestCompositingOrder:
    def test_higher_order_overwrites_lower(self) -> None:
        bottom = _make_memfile(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS, rgb=(10, 10, 10)
        )
        top = _make_memfile(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS, rgb=(200, 200, 200)
        )
        layers = [
            RenderLayerRef(layer_id="BOT", source_path="b.tif", cache_path="b.tif", order=0),
            RenderLayerRef(layer_id="TOP", source_path="t.tif", cache_path="t.tif", order=1),
        ]
        spec = _spec(layers=layers, width=16, height=16)

        with _opener_for({"b.tif": bottom, "t.tif": top}) as opener:
            canvas = render_raster_layers(spec, dataset_opener=opener)

        assert tuple(canvas[8, 8].tolist()) == (200, 200, 200)


class TestPartialOverlap:
    def test_uncovered_area_keeps_background(self) -> None:
        # Layer covers only the western half of the geo_window
        memfile = _make_memfile(
            bounds=(106.0, 10.0, 106.5, 11.0), crs=GEOGRAPHIC_CRS, rgb=(100, 100, 100)
        )
        layer = RenderLayerRef(
            layer_id="L1", source_path="L1.tif", cache_path="L1.tif", order=0
        )
        spec = _spec(layers=[layer], width=32, height=16, bg_color="#FF0000")

        with _opener_for({"L1.tif": memfile}) as opener:
            canvas = render_raster_layers(spec, dataset_opener=opener)

        # West (col=4) covered by layer; east (col=28) still red background
        assert tuple(canvas[8, 4].tolist()) == (100, 100, 100)
        assert tuple(canvas[8, 28].tolist()) == (255, 0, 0)


class TestErrorHandling:
    def test_unreadable_layer_collects_issue_but_others_render(self) -> None:
        good = _make_memfile(
            bounds=(106.0, 10.0, 107.0, 11.0), crs=GEOGRAPHIC_CRS, rgb=(40, 40, 40)
        )
        layers = [
            RenderLayerRef(layer_id="BAD", source_path="bad.tif", cache_path="bad.tif", order=0),
            RenderLayerRef(layer_id="OK", source_path="ok.tif", cache_path="ok.tif", order=1),
        ]
        spec = _spec(layers=layers, width=16, height=16)

        with _opener_for(
            {"ok.tif": good}, unreadable_paths={"bad.tif"}
        ) as opener:
            canvas = render_raster_layers(spec, dataset_opener=opener)

        assert tuple(canvas[8, 8].tolist()) == (40, 40, 40)

    def test_all_layers_fail_raises_render_error(self) -> None:
        layers = [
            RenderLayerRef(layer_id="X", source_path="x.tif", cache_path="x.tif", order=0)
        ]
        spec = _spec(layers=layers, width=16, height=16)

        with _opener_for({}, unreadable_paths={"x.tif"}) as opener:
            with pytest.raises(RenderError) as exc:
                render_raster_layers(spec, dataset_opener=opener)

        ids = [i.issue_id for i in exc.value.issues]
        assert "render.raster.unreadable" in ids
        assert exc.value.issues[0].layer_id == "X"


class TestCanvasShape:
    def test_empty_visible_layers_returns_background_canvas(self) -> None:
        spec = _spec(layers=[], width=24, height=12, bg_color="#0000FF")
        canvas = render_raster_layers(spec)
        assert canvas.shape == (12, 24, 3)
        assert canvas.dtype == np.uint8
        # All pixels should be background blue
        assert (canvas[..., 2] == 255).all()
        assert (canvas[..., 0] == 0).all()
        assert (canvas[..., 1] == 0).all()
