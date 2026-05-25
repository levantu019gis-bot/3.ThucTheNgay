# Story 5.1: Build Shared Render Specification from Composition State

Status: done

<!-- Created from Epic 5 backlog context per project autonomous execution mandate. -->

## Story

As a Developer,
I want a shared render specification derived from composition state,
So that preview and final rendering use the same source of truth.

## Acceptance Criteria

1. Given a composition, target config, template metadata, and requested output size are available, when the render spec builder runs, then it produces a normalized render spec containing view center, scale denominator, template map-frame physical size/aspect, derived geographic map window, visible layers in draw order, grid settings, background settings, output dimensions, and template references. The spec uses composition `view.center` `[lon, lat]` and `view.scale` (interpreted as the map scale denominator) as the persisted source of truth.
2. Given a composition has hidden layers or custom layer ordering, when the render spec is built, then hidden layers are excluded from drawing and visible layers preserve persisted layer order from the composition.
3. Given a composition has a per-composition grid override, when the render spec is built, then the override is used instead of target defaults, and target defaults remain unchanged.
4. Given required render inputs are missing or invalid, when the render spec builder runs, then it returns structured errors or issues rather than partially rendering unknown state, and the render code remains usable in tests without Qt widget dependencies.

## Tasks / Subtasks

- [x] Define render spec models in `render/spec.py` (AC: 1, 2, 3)
  - [x] `GeoWindow` (min/max lon/lat) with validation.
  - [x] `RenderLayerRef` (layer_id, source_path, cache_path, order).
  - [x] `RenderBackground` (color default white).
  - [x] `RenderSpec` aggregating composition_id, target_id, output dims, view center/scale, MapFrame, aspect, GeoWindow, visible layers, GridConfig, background, template refs (template_metadata_file, template_pptx, slide_index).
- [x] Implement `build_render_spec(...)` function (AC: 1, 2, 3, 4)
  - [x] Validates target.id == composition.target_id.
  - [x] Validates output_width/height > 0.
  - [x] Validates template.map_frame width/height > 0.
  - [x] Computes map_frame_aspect = width/height.
  - [x] Derives geographic map window from view.scale (denominator) + map_frame physical size + center latitude using a documented approximation (1 pt = 1/72 inch; meters/degree latitude ≈ 111320; cos-latitude for longitude).
  - [x] Filters layers by `visible=True`, sorts by persisted `order` ascending.
  - [x] Uses `composition.grid_override` if present, else `target.grid`. Does NOT mutate target.
  - [x] On any validation failure raises `RenderSpecError(issues=[...])` with Vietnamese remediation.
- [x] Wire exports in `render/__init__.py` (AC: 4)
- [x] Add tests `tests/unit/test_render_spec.py` (AC: 1-4)
  - [x] Happy path: spec fields populated correctly; aspect; geo window math.
  - [x] Hidden layers excluded; visible order preserved.
  - [x] grid_override overrides target.grid; target object unchanged.
  - [x] target_id mismatch raises RenderSpecError with Vietnamese remediation.
  - [x] output_width <= 0 raises.
  - [x] Empty visible layers allowed (spec built; downstream decides).
  - [x] Import boundary: `thucthengay.render` does NOT import PySide6.
- [x] Run pytest + ruff + smoke.

### Review Findings

- [x] [Review][Patch] Replace the scale/window approximation with a pyproj-backed geodesic span so the shared spec no longer bakes in latitude/cosine drift before Story 5.2 reads rasters.
- [x] [Review][Patch] Add finite WGS84 bounds validation and reject antimeridian/pole-crossing windows with structured Vietnamese `RenderSpecError` issues instead of letting invalid CRS math reach rasterio.
- [x] [Review][Patch] Add an output pixel budget guard so bad template/export dimensions cannot allocate huge render buffers and freeze or crash the app.
- [x] [Review][Patch] Validate background colors as `#RRGGBB` at model construction so render callers receive predictable inputs.

## Dev Notes

- Follow `_bmad-output/project-context.md` for env/quality rules.
- Owner module: `render/` (new submodule `render/spec.py`).
- Geographic window math is an MVP approximation; Story 5.2 will refine with proper CRS via `pyproj`/`rasterio`. Document the formula explicitly so Story 5.2 has a baseline to compare against.
- Treat `template.map_frame` width/height as **PowerPoint points** (1 pt = 1/72 inch). PPTX EMU is 914400/inch; if a future template uses different units, a conversion layer can be added without changing this story.
- Background: MVP default white `#FFFFFF`. AC requires "background settings"; we expose a `RenderBackground` model so Story 5.3 can extend.
- `RenderSpec` is a Pydantic model with `extra="forbid"` for parity with other persisted/passed schemas, even though it's a derived (non-persisted) object.
- No Qt or editor imports — enforced by import-boundary test.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.1]
- [Source: src/thucthengay/models/composition.py — ViewState, Composition]
- [Source: src/thucthengay/models/template.py — TemplateMetadata, MapFrame]
- [Source: src/thucthengay/models/config.py — TargetConfig, GridConfig]

## Dev Agent Record

### Agent Model Used

claude-opus-4-7

### Debug Log References

- `conda run -n ttn-env pytest` — 179 passed (13 new tests in `test_render_spec.py`).
- `conda run -n ttn-env ruff check .` — All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` — App ready.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest tests/unit/test_render_spec.py tests/unit/test_render_raster.py tests/unit/test_gis_crs.py` — 35 passed after review patches.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check src/thucthengay/render src/thucthengay/gis tests/unit/test_render_spec.py tests/unit/test_render_raster.py tests/unit/test_gis_crs.py` — All checks passed after review patches.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` — 215 passed.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` — All checks passed.
- `conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay --smoke` — App ready.

### Completion Notes List

- Added `render/spec.py` containing `RenderSpec`, `GeoWindow`, `RenderLayerRef`, `RenderBackground`, `RenderSpecError`, and `build_render_spec()`.
- Builder validates target↔composition id match, positive output dims, and positive map_frame dims; collects all issues and raises `RenderSpecError(issues=[...])` with Vietnamese remediation.
- Derived geographic window uses documented MVP formula: paper-to-meters at scale denominator, lat constant 111320, cosine-lat for longitude. Story 5.2 will swap in proper CRS via `pyproj`/`rasterio` and can compare numerically against this baseline.
- Hidden layers excluded; visible layers sorted by persisted `order` (preserves UX-DR layer ordering).
- `grid_override` precedence over `target.grid`; target object is not mutated (verified by test).
- Import-boundary test runs in a clean subprocess to confirm `thucthengay.render` does not transitively pull in PySide6.
- Review hardening replaced the initial meters-per-degree approximation with a pyproj geodesic calculation from the persisted center/scale/map frame, while keeping the same shared spec contract for preview/final parity.
- Render spec now rejects unsafe output sizes and invalid/extreme WGS84 windows before raster allocation or CRS transforms can trigger OOM, hangs, or low-level exceptions.
- Background color validation is model-level, keeping render code from receiving malformed color strings in normal use.

### File List

- `_bmad-output/implementation-artifacts/5-1-build-shared-render-specification-from-composition-state.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/render/spec.py` (NEW)
- `src/thucthengay/render/__init__.py`
- `tests/unit/test_render_spec.py` (NEW)
- `tests/unit/test_render_raster.py`
- `src/thucthengay/gis/crs.py`

## Change Log

- 2026-05-25: Created story context from Epic 5 backlog and started implementation.
- 2026-05-25: Implemented RenderSpec + builder + 13 tests. pytest 179 passed, ruff clean, smoke OK. Moved to review.
- 2026-05-26: Addressed code-review hardening findings for geodesic window derivation, safe WGS84 bounds, background validation, and output pixel budget. Full gates passed; moved to done.
