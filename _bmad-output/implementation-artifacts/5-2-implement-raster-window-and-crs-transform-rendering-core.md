# Story 5.2: Implement Raster Window and CRS Transform Rendering Core

Status: done

## Story

As an Operator,
I want raster imagery rendered from the selected target-centered map view,
So that the map output matches the area I framed in Review/Edit.

## Acceptance Criteria

1. Given the render spec contains view center, scale denominator, derived geographic map window, and visible raster layers, when the rendering core prepares a layer, then it uses rasterio/GDAL metadata and `pyproj` transformations as needed to convert the derived geographic map window to the raster CRS/read window AND handles rasters whose CRS differs from the geographic CRS used by the composition view center.
2. Given multiple visible layers overlap the output area, when the renderer composites them, then it draws layers in render spec order (lower `order` first, higher `order` on top) AND hidden layers do not affect the output pixels.
3. Given the derived map window only partially overlaps a raster, when the renderer reads the raster window, then it clips to available raster bounds AND fills non-covered areas with the configured background rather than failing the whole render.
4. Given a raster cannot be opened or read during rendering, when rendering reaches that layer, then the renderer returns a structured render error/issue with the affected `layer_id` AND callers can decide whether preview shows an error or validation blocks export.

## Performance Mandate (Epic 5 cross-story)

- Always use windowed reads (`rasterio.windows.from_bounds` + `out_shape=`) — never load full rasters into memory.
- On-the-fly CRS handling via `WarpedVRT`, no temp files written to disk.
- Cache `pyproj.Transformer` instances per (src_crs, dst_crs) tuple to avoid re-init.
- Default dtype `uint8` RGB(A); preallocated single output canvas; in-place compositing.
- `Resampling.bilinear` for the preview path (fast); the final-quality path is owned by Story 5.5.
- Each raster is opened once per render call inside a `with` block (released deterministically).
- Bounds-overlap check **before** opening downstream IO when possible.

## Tasks / Subtasks

- [x] Add CRS/window helpers in `gis/crs.py` (AC: 1, 3)
  - [x] `get_transformer(src_crs, dst_crs)` LRU-cached factory.
  - [x] `geographic_window_to_raster_window(geo_window, dataset)` returning `(rasterio.windows.Window, clipped_geo_window | None)` — clipped to dataset bounds; None when no overlap.
  - [x] Handle WGS84 ↔ projected reprojection of the geo_window corners (use densified bbox for accuracy on projected CRS).
- [x] Add raster rendering core in `render/raster.py` (AC: 1, 2, 3, 4)
  - [x] `RenderError(Exception)` carrying `issues: list[Issue]`.
  - [x] `render_raster_layers(spec, *, dataset_opener=rasterio.open) -> np.ndarray` returns `(H, W, 3)` uint8.
  - [x] Fills canvas with `spec.background.color` first.
  - [x] Iterates `spec.visible_layers` ascending; opens each lazily; uses `WarpedVRT` only when CRS differs from spec geographic CRS (EPSG:4326).
  - [x] Reads only the window intersecting `geo_window`; clips to raster bounds; uses `out_shape` for GDAL-side decimation.
  - [x] Pastes into the destination subregion of the canvas; non-overlapping areas keep background.
  - [x] On per-layer IO/CRS failure, accumulates an `Issue(render.raster.unreadable | render.raster.crs_missing | ...)` and continues other layers; raises `RenderError` only if **no** layer rendered AND at least one issue exists.
  - [x] `dataset_opener` dependency-injection seam keeps tests Qt-free and lets us pass `MemoryFile.open()` synthetic datasets.
- [x] Update `render/__init__.py` exports for `render_raster_layers`, `RenderError`.
- [x] Tests `tests/unit/test_gis_crs.py` (AC: 1, 3)
  - [x] Same-CRS window math against synthetic EPSG:4326 raster.
  - [x] Cross-CRS reprojection against synthetic EPSG:3857 raster.
  - [x] No-overlap returns `None`.
  - [x] Partial overlap clips to dataset bounds.
  - [x] `get_transformer` cache returns same instance.
- [x] Tests `tests/unit/test_render_raster.py` (AC: 1, 2, 3, 4)
  - [x] Synthetic in-memory GeoTIFF in EPSG:4326 — pixel sanity check vs. background.
  - [x] CRS-mismatch path (EPSG:3857 source vs. WGS84 geo_window).
  - [x] Two-layer compositing — higher `order` overwrites lower.
  - [x] Hidden layers excluded (covered transitively because spec excludes them, but assert canvas remains background).
  - [x] Partial overlap → uncovered area stays background color.
  - [x] Unopenable layer → `Issue('render.raster.unreadable', layer_id=...)`, other layers still render.
  - [x] All-fail case → `RenderError`.
  - [x] Output `dtype == uint8`, `shape == (output_height, output_width, 3)`.

### Review Findings

- [x] [Review][Patch] Return a structured `RasterRenderResult` containing canvas, non-fatal issues, and painted layer ids so partial layer failures are no longer silently swallowed.
- [x] [Review][Patch] Add output pixel budget and `MemoryError` guards before/around allocation and per-layer reads to avoid OOM/freeze crashes.
- [x] [Review][Patch] Preserve existing pixels for nodata/masked/alpha-transparent raster areas instead of overwriting lower layers/background.
- [x] [Review][Patch] Scale non-`uint8` integer/float rasters to `uint8` deliberately instead of clipping/saturating common `uint16`/float GeoTIFFs.
- [x] [Review][Patch] Guard CRS/window math against non-finite projection results, rotated/sheared transforms, malformed CRS exceptions, and all-visible-layers-no-overlap blank renders.
- [x] [Review][Patch] Use floor/ceil destination pixel bounds and a bounded `WarpedVRT` memory limit to reduce seams and warp memory spikes.
- [x] [Review][Patch] Expose a cancellation callback at the render-core boundary. Full Qt worker/thread orchestration remains Story 5.4, which owns two-stage preview rendering jobs.

## Dev Notes

- Render canvas convention: numpy array shaped `(H, W, 3)` uint8 RGB; rows top→bottom, cols left→right; (row=0, col=0) corresponds to `(min_lon, max_lat)` of `geo_window` — i.e. north-west.
- Geo→pixel mapping: `col = (lon - min_lon)/(max_lon - min_lon) * W`; `row = (max_lat - lat)/(max_lat - min_lat) * H`.
- Why `WarpedVRT` over `rasterio.warp.reproject`: VRT does on-the-fly reprojection during `read()`, avoiding a full intermediate array materialization.
- Why `out_shape` on read: GDAL applies decimation/overview selection at IO time — orders of magnitude less memory than read-then-resize.
- Background hex `#RRGGBB` parsed to RGB tuple; default `#FFFFFF` from Story 5.1.
- Per Story 5.3 boundary: this story does **NOT** draw grid, north arrow, or scale bar.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.2]
- [Source: src/thucthengay/render/spec.py — RenderSpec, GeoWindow]
- [Source: src/thucthengay/models/issue.py — Issue, IssueScope.RENDER]

## Dev Agent Record

### Agent Model Used

claude-opus-4-7

### Debug Log References

- `conda run -n ttn-env pytest` — **193 passed** (+14 new across `test_gis_crs.py` & `test_render_raster.py`).
- `conda run -n ttn-env ruff check .` — All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` — App ready.
- Initial failure `WarpedVRT does not permit boundless reads` resolved by removing `boundless=True` from `src.read()`; the window is already clipped to dataset bounds by `geographic_window_to_raster_window` so boundless is unnecessary.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest tests/unit/test_render_spec.py tests/unit/test_render_raster.py tests/unit/test_gis_crs.py` — 35 passed after review patches.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check src/thucthengay/render src/thucthengay/gis tests/unit/test_render_spec.py tests/unit/test_render_raster.py tests/unit/test_gis_crs.py` — All checks passed after review patches.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` — 215 passed.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` — All checks passed.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay --smoke` — App ready.

### Completion Notes List

- **`gis/crs.py`** owns CRS/window math (per module ownership). Public surface: `GEOGRAPHIC_CRS`, `WindowResolution`, `get_transformer` (LRU-cached), `normalize_crs_key`, `geographic_window_to_raster_window`. Takes/returns primitive bbox tuples — no dependency on `render/`.
- **`render/raster.py`** orchestrates compositing into a single preallocated `uint8` RGB canvas. Performance choices baked in:
  - GDAL-side decimation via `out_shape=`, never read-then-resize.
  - `WarpedVRT` for on-the-fly CRS reprojection (no intermediate file).
  - LRU-cached `Transformer` instances.
  - Single canvas, in-place paste, `uint8` throughout.
  - `dataset_opener` injection keeps the module Qt-free and lets tests use `MemoryFile`.
- **Error model**: per-layer IO/CRS issues accumulate as structured `Issue`s (`render.raster.unreadable`, `render.raster.crs_missing`) with Vietnamese remediation and `layer_id`. If *no* layer painted AND issues exist, raises `RenderError`. Otherwise we return a best-effort canvas and let callers decide (preview shows warning; export validation will block).
- **Compositing order**: lower `order` painted first; later layers overwrite — matches Story 5.1 sorting.
- **Partial overlap**: `_geo_to_pixel` maps the clipped `covered_bbox` back to canvas coordinates, so uncovered area keeps the configured background color.
- **CRS-mismatch verified**: synthetic EPSG:3857 raster reads through `WarpedVRT` and lands on the canvas correctly.
- Tests use `rasterio.MemoryFile` exclusively — no disk IO, no network, no Qt event loop, no real GeoTIFF.
- Review hardening changed the public render return to `RasterRenderResult` so callers can surface partial layer issues while still using the best-effort canvas.
- The render core now rejects oversized outputs before allocation, catches `MemoryError`, handles nodata/masks/alpha, scales non-`uint8` inputs to bounded RGB, reports no-overlap renders, and rejects rotated/sheared source transforms with structured render issues.
- The core exposes `is_cancelled`; Story 5.4 must run render calls off the Qt main thread and wire generation/cancel behavior for preview responsiveness.

### File List

- `_bmad-output/implementation-artifacts/5-2-implement-raster-window-and-crs-transform-rendering-core.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/gis/crs.py` (NEW)
- `src/thucthengay/gis/__init__.py`
- `src/thucthengay/render/raster.py` (NEW)
- `src/thucthengay/render/__init__.py`
- `tests/unit/test_gis_crs.py` (NEW)
- `tests/unit/test_render_raster.py` (NEW)
- `src/thucthengay/render/spec.py`
- `tests/unit/test_render_spec.py`

## Change Log

- 2026-05-25: Created story context from Epic 5 backlog and started implementation.
- 2026-05-25: Implemented gis/crs.py + render/raster.py with WarpedVRT-based CRS handling, windowed reads, and structured per-layer error issues. 14 new tests added (pytest 193 passed, ruff clean, smoke OK). Moved to review.
- 2026-05-26: Addressed code-review hardening findings for structured partial issues, memory safety, nodata/alpha/dtype handling, CRS guards, no-overlap detection, and cancel hook. Full gates passed; moved to done.
