# Story 5.3: Render Coordinate Frame and Map Background Without MVP Extras

Status: done

<!-- Created from Epic 5 backlog context. Scope clarification: "grid" in config means coordinate frame interval for MVP render, not an internal map grid mesh. -->

## Story

As an Operator,
I want coordinate frame labels and map background rendered consistently,
So that the exported map follows the configured slide style without unsupported extras.

## Acceptance Criteria

1. Given the render spec includes grid settings, when the map is rendered, then the renderer draws a coordinate frame around the map output with edge ticks and coordinate labels according to interval and label format, defaulting to `dms_full` where configured.
2. Given the coordinate frame is rendered, when labels are placed, then labels align with the rendered geographic map window and the renderer does not draw an internal grid mesh across the raster area.
3. Given the render spec includes background settings, when raster coverage does not fill the whole output frame, then uncovered areas render using the configured background and the output does not expose transparent or uninitialized pixels unless explicitly configured.
4. Given MVP render output is requested, when rendering completes, then boundary overlay, north arrow, and scale bar are not rendered and tests make this MVP behavior explicit to avoid accidental inclusion.
5. Given grid/frame settings are invalid, when the renderer attempts to draw the coordinate frame, then rendering returns a structured error rather than silently drawing incorrect labels, and the error can be surfaced as a Vietnamese remediation through validation/UI layers.

## Tasks / Subtasks

- [x] Add coordinate frame rendering module in `render/frame.py` (AC: 1, 2, 4, 5)
  - [x] Convert `GridConfig.interval` DMS values to degree interval with validation.
  - [x] Generate longitude/latitude tick values inside the `RenderSpec.geo_window` bounds.
  - [x] Format coordinate labels, supporting `dms_full` default and `dms_short`.
  - [x] Draw only outer frame, edge ticks, and labels; do not draw internal mesh lines.
  - [x] Return structured render issues through `RenderError` for invalid interval/format.
- [x] Add composed render entry point in `render/core.py` (AC: 1, 3, 4, 5)
  - [x] Call existing raster renderer first so background and raster coverage remain Story 5.2 behavior.
  - [x] Overlay coordinate frame on the returned canvas.
  - [x] Preserve non-fatal raster issues in the composed result.
  - [x] Export public API from `render/__init__.py`.
- [x] Add focused unit tests in `tests/unit/test_render_frame.py` (AC: 1, 2, 4, 5)
  - [x] Frame/tick/label pixels appear on edges.
  - [x] Interior pixels remain unchanged when no raster/background changes occur, proving no internal mesh.
  - [x] Label/tick placement aligns to geo_window edge mapping.
  - [x] Unsupported label format raises `RenderError` with Vietnamese remediation.
- [x] Add composed render tests in `tests/unit/test_render_core.py` (AC: 3, 4, 5)
  - [x] Background survives uncovered raster areas.
  - [x] Composed result includes coordinate frame and keeps raster issues.
  - [x] Tests explicitly assert there is no boundary/north-arrow/scale-bar artifact.
- [x] Run quality gates
  - [x] `pytest`
  - [x] `ruff check .`
  - [x] `python -m thucthengay --smoke`

### Review Findings

- [x] [Review][Patch] Add safe tick-count guard for overly dense frame intervals
  [`src/thucthengay/render/frame.py`]
- [x] [Review][Patch] Preserve prior raster issues when coordinate frame rendering fails
  [`src/thucthengay/render/core.py`]
- [x] [Review][Patch] Check cancellation after raster rendering before drawing frame
  [`src/thucthengay/render/core.py`]
- [x] [Review][Patch] Clamp coordinate labels using measured text bounds and render edge labels
  [`src/thucthengay/render/frame.py`]
- [x] [Review][Patch] Treat empty/whitespace label format as invalid instead of defaulting silently
  [`src/thucthengay/render/frame.py`]
- [x] [Review][Patch] Strengthen MVP exclusion test with coordinate-frame-only expected output
  [`tests/unit/test_render_core.py`]

## Dev Notes

- Project mandate: Epic 5 rendering code must be memory-safe, Qt-free, cancellable at render boundaries where applicable, and covered by focused unit tests.
- Owner module: `render/` owns preview/final render. Use `gis/` only for CRS/grid math helpers if needed; do not import `editor` or `PySide6`.
- Existing Story 5.1 provides `RenderSpec`, `GeoWindow`, `RenderBackground`, and `GridConfig` selection from composition override vs target default.
- Existing Story 5.2 provides `render_raster_layers()` returning `RasterRenderResult(canvas, issues, painted_layer_ids)` with background fill, partial raster coverage behavior, memory guards, and structured `RenderError`.
- Scope clarification from product owner: although historical docs say "grid", Story 5.3 must render a coordinate frame around the map output, with edge tick marks and coordinate labels. It must not render a grid mesh of internal horizontal/vertical lines over the raster.
- MVP exclusions remain strict: no boundary overlay, no north arrow, no scale bar.
- Tests should use synthetic specs/canvases only; no real GeoTIFF, PPTX, network, or Qt event loop.

### References

- [Source: _bmad-output/project-context.md#Epic 5 Rendering Engine Mandate]
- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.3]
- [Source: _bmad-output/planning-artifacts/architecture.md#Rendering Architecture]
- [Source: _bmad-output/implementation-artifacts/5-1-build-shared-render-specification-from-composition-state.md]
- [Source: _bmad-output/implementation-artifacts/5-2-implement-raster-window-and-crs-transform-rendering-core.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests/unit/test_render_frame.py tests/unit/test_render_core.py` - initially failed on missing API, then passed after implementation (`8 passed`).
- `conda run -n ttn-env ruff check src\thucthengay\render tests\unit\test_render_frame.py tests\unit\test_render_core.py` - fixed line-length findings, then passed.
- `conda run -n ttn-env pytest` - first full run failed because pytest could not access `C:\Users\Admin\AppData\Local\Temp\pytest-of-Admin`; rerun with workspace `TEMP/TMP` passed (`223 passed`).
- `conda run -n ttn-env ruff check .` - All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - App ready.
- `conda run -n ttn-env pytest tests\unit\test_render_frame.py tests\unit\test_render_core.py` - after review fixes passed (`13 passed`).
- `conda run -n ttn-env ruff check src\thucthengay\render tests\unit\test_render_frame.py tests\unit\test_render_core.py` - passed after import/line-length cleanup.
- `conda run -n ttn-env pytest` with workspace `TEMP/TMP` - full regression passed (`228 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check .` - All checks passed after review fixes.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - App ready after review fixes.

### Completion Notes List

- Implemented `draw_coordinate_frame()` for MVP coordinate frame rendering: outer border, edge ticks, DMS labels, style defaults, and structured `RenderError` issues for invalid canvas/interval/label format.
- Implemented `render_map()` composed entry point that reuses Story 5.2 raster/background rendering, overlays the coordinate frame, and preserves non-fatal raster issues.
- Tests explicitly guard the clarified scope: coordinate frame only, no internal grid mesh, no boundary overlay, no north arrow, no scale bar.
- No Qt/editor imports were added to render modules; import-boundary tests passed in full regression.
- Code review fixes resolved dense interval safety, frame-error issue preservation, cancellation before frame overlay, edge-label rendering/clamping, empty label-format validation, and stronger MVP exclusion coverage.

### File List

- `_bmad-output/implementation-artifacts/5-3-render-grid-and-map-background-without-mvp-extras.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/render/core.py`
- `src/thucthengay/render/frame.py`
- `src/thucthengay/render/__init__.py`
- `tests/unit/test_render_core.py`
- `tests/unit/test_render_frame.py`

## Change Log

- 2026-05-26: Created Story 5.3 artifact with clarified coordinate-frame scope and started implementation.
- 2026-05-26: Implemented coordinate frame renderer and composed map render API with focused tests. Quality gates passed; moved to review.
- 2026-05-26: Completed code review fixes, reran quality gates, and moved Story 5.3 to done.
