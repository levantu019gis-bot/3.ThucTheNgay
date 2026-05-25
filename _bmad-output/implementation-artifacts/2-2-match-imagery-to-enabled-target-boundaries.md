# Story 2.2: Match Imagery to Enabled Target Boundaries

Status: done

## Story

As an Operator,
I want scanned imagery matched to enabled target boundaries,
so that each target only receives imagery that intersects its configured area.

## Acceptance Criteria

1. Given enabled targets have valid GeoJSON boundary files, when ingestion loads target boundaries, then it reads each GeoJSON through the config-resolved path and prepares geometries for intersection checks without changing the source GeoJSON files.
2. Given scanned imagery has a valid footprint and CRS, when ingestion compares imagery against targets, then it transforms geometries as needed using `pyproj`/rasterio CRS metadata and records a match when the imagery footprint intersects the target boundary.
3. Given a target is disabled in config, when matching runs, then no imagery is matched to that target and no compositions are created for that target.
4. Given a target boundary is missing, invalid, or cannot be transformed, when matching reaches that target, then ingestion records a blocking target-level issue or warning appropriate to the failure and processing continues for other valid targets where possible.

## Tasks / Subtasks

- [x] Add target boundary loading contracts (AC: 1, 4)
  - [x] Load GeoJSON from config-resolved target paths only.
  - [x] Support FeatureCollection, Feature, and bare geometry documents.
  - [x] Emit target-level issues for missing, unreadable, invalid, or empty boundaries.
- [x] Add intersection matching service (AC: 2, 3)
  - [x] Build imagery footprint polygons from Story 2.1 scan bounds and CRS.
  - [x] Transform target geometry to raster CRS when needed.
  - [x] Match only enabled targets supplied by config loading.
  - [x] Return target-to-imagery matches without copying files or creating compositions.
- [x] Add focused tests and run quality gates (AC: 1, 2, 3, 4)
  - [x] Cover direct CRS matches, CRS transformation, disabled target exclusion, missing/invalid target warnings, and continuation after a bad target.
  - [x] Run `pytest`, `ruff check .`, and app smoke through `ttn-env`.

## Dev Notes

### Scope Boundaries

- This story consumes scan results from Story 2.1 and resolved config paths from Story 1.3.
- Do not copy imagery into workspace cache, create composition JSON, mutate manifest, or write workspace state.
- Disabled targets should already be filtered by `ConfigLoadResult.enabled_targets`; this story must not reintroduce disabled targets from raw config.

### Architecture Requirements

- Owner module: `src/thucthengay/ingestion/intersection.py`.
- Use `shapely` for geometry and intersection checks, `pyproj` for CRS transformations.
- Return shared `Issue` objects for target-level problems.
- Core ingestion code must not import `PySide6`, `editor`, or `workspace`.

### Implementation Guidance

- GeoJSON with no explicit CRS should be treated as `EPSG:4326`, which is the normal GeoJSON convention.
- If GeoJSON includes a legacy `crs` object with a `name`, respect it when possible.
- Transform target geometry into the raster CRS before calling `intersects`.
- A target boundary issue should not stop other valid targets from being matched.
- Matching result should be deterministic: preserve enabled target order from config and scan result order from Story 2.1.

### Previous Story Learnings

- Story 2.1 returns `ScannedGeoTiff` with raster CRS/bounds and stable unique `ImageLayer.layer_id`; reuse that rather than reopening rasters.
- Story 2.1 warnings are non-blocking and scan results exclude rasters without a valid footprint, so this story can assume scanned rasters are valid for footprint matching.

### Testing Requirements

- Tests may generate tiny GeoTIFF fixtures at runtime using `rasterio`; do not commit binary imagery.
- Tests may write temporary GeoJSON files under `tmp_path`.
- Run full regression after implementation:
  - `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest`
  - `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .`
  - `/home/ongtu/miniconda3/bin/conda run -n ttn-env env -u DISPLAY -u WAYLAND_DISPLAY UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay`

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.2-Match-Imagery-to-Enabled-Target-Boundaries]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-3-Scan-and-match-GeoTIFF-imagery]
- [Source: _bmad-output/planning-artifacts/architecture.md#GIS-Spatial-Architecture]
- [Source: _bmad-output/project-context.md#Module-Ownership-Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Red test: `pytest tests/unit/test_ingestion_intersection.py` failed on missing `match_imagery_to_targets` import before implementation.
- Focused green test: `pytest tests/unit/test_ingestion_intersection.py` -> 5 passed.
- Full regression: `pytest` -> 60 passed.
- Lint: `ruff check .` -> All checks passed.
- App smoke: `python -m thucthengay` with `DISPLAY`/`WAYLAND_DISPLAY` unset -> `3.ThucTheNgay app ready.`
- Review result: clean after edge-case hardening; no open findings.

### Completion Notes List

- Added `ingestion/intersection.py` for target GeoJSON loading, CRS-aware target/raster intersection, and match result contracts.
- Matching uses only `ConfigLoadResult.enabled_targets`, so disabled targets are excluded from output.
- Target boundary failures produce blocking target-level `Issue` objects while valid targets continue processing.
- Added tests for direct CRS intersection, CRS transformation, disabled target exclusion, invalid/missing boundaries, and non-object GeoJSON handling.
- Code review hardening added explicit non-object GeoJSON handling and target-level issue reporting for CRS transform failures.

### File List

- `_bmad-output/implementation-artifacts/2-2-match-imagery-to-enabled-target-boundaries.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/ingestion/__init__.py`
- `src/thucthengay/ingestion/intersection.py`
- `tests/unit/test_ingestion_intersection.py`

### Change Log

- 2026-05-25: Created story context for Epic 2 Story 2.2.
- 2026-05-25: Implemented target boundary matching; story moved to review.
- 2026-05-25: Completed internal review and marked story done.
