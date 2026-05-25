# Story 2.1: Scan Imagery Folder and Extract GeoTIFF Metadata

Status: done

## Story

As an Operator,
I want the app to scan my imagery folder and extract required GeoTIFF metadata,
so that usable imagery can enter the workflow even when separate metadata files are missing.

## Acceptance Criteria

1. Given the Operator has selected a valid imagery input folder, when ingestion scans the folder, then it recursively discovers supported GeoTIFF files and ignores unsupported files without failing the entire ingestion run.
2. Given a GeoTIFF has PlanetScope-style filename metadata or an available sidecar metadata file, when metadata extraction runs, then the app parses capture date/time, cloud percent when available, and source identifiers from that metadata source, and the layer records the metadata source used for each parsed field.
3. Given a GeoTIFF has no usable sidecar metadata file, when metadata extraction runs, then the app uses `rasterio` to read required information directly from the GeoTIFF, including CRS, bounds or transform, width/height, band count, nodata when available, and embedded tags when available, and the file can continue to target matching when a valid footprint can be derived.
4. Given capture date/time or cloud percent cannot be derived from filename, sidecar metadata, or embedded GeoTIFF tags, when the layer metadata is created, then the missing fields are marked with `metadata_status=needs_manual_correction` where required by later workflow and ingestion creates a warning rather than failing the entire run.
5. Given a GeoTIFF cannot be opened or has no valid geospatial footprint, when metadata extraction attempts to process it, then ingestion records a warning with the file path and reason and the invalid file is excluded from target matching.

## Tasks / Subtasks

- [x] Add ingestion scan result contracts and public package exports (AC: 1, 3, 4, 5)
  - [x] Define scan result objects for valid rasters and warnings without persisting workspace state.
  - [x] Keep ingestion contracts independent from Qt/editor and workspace writes.
- [x] Add recursive supported GeoTIFF discovery (AC: 1)
  - [x] Support `.tif` and `.tiff` case-insensitively.
  - [x] Ignore unsupported files and sidecar JSON files.
- [x] Add filename/sidecar/embedded metadata extraction (AC: 2, 3, 4)
  - [x] Parse PlanetScope-style leading `YYYYMMDD_HHMMSS` filename metadata.
  - [x] Parse optional JSON sidecars next to the GeoTIFF when present.
  - [x] Fall back to rasterio tags for embedded metadata.
  - [x] Track the metadata source selected for capture date/time and cloud/source identifiers.
- [x] Add rasterio GeoTIFF metadata reading and warning handling (AC: 3, 5)
  - [x] Capture CRS, bounds, transform, width, height, band count, nodata, and tags.
  - [x] Exclude unreadable rasters or rasters without a valid footprint from target matching results.
  - [x] Emit non-blocking Vietnamese warnings containing file path and reason.
- [x] Add focused tests and run quality gates (AC: 1, 2, 3, 4, 5)
  - [x] Cover recursive discovery, unsupported ignores, filename metadata, sidecar precedence, embedded fallback, missing business metadata warning, and invalid raster warning.
  - [x] Run `pytest`, `ruff check .`, and app import/smoke command through `ttn-env`.

### Review Findings

- [x] [Review][Patch] Prevent duplicate layer IDs for recursive files with the same stem [src/thucthengay/ingestion/scanner.py:127]

## Dev Notes

### Scope Boundaries

- This story owns scan and metadata extraction only. Do not match target GeoJSON boundaries, copy cache files, create compositions, update manifests, or mutate workspace JSON; those are later Epic 2 stories.
- Invalid/unusable files must not abort the whole scan. They produce warning `Issue` objects and are absent from the valid raster list.
- Missing capture date/time or cloud percent is not fatal when raster footprint is valid. Mark metadata as needing manual correction and produce a warning for later UX/validation workflows.

### Architecture Requirements

- Owner modules: `src/thucthengay/ingestion/` for scanner/parser contracts, optionally `src/thucthengay/models/layer.py` only if the existing metadata status enum must be aligned with this story.
- Use `rasterio/GDAL` for raster metadata and footprint. Do not introduce alternate GIS libraries.
- Return shared `Issue` objects for warnings so later warnings UI and validation can reuse the same contract.
- Core ingestion code must not import `PySide6`, `editor`, or `workspace`.
- User project imagery is read-only source data outside the app source tree.

### Implementation Guidance

- Supported imagery extensions are `.tif` and `.tiff`, matched case-insensitively.
- Sidecar metadata lookup should be conservative and local to the GeoTIFF path, such as `<image>.json`, `<image>.metadata.json`, and `<stem>.json`.
- Parse common metadata fields from sidecar root or `properties`: `capture_datetime`, `acquired`, `published`, `capture_date`, `capture_time`, `cloud_percent`, `cloud_cover`, `cloud_cover_percent`, `source_id`, `item_id`, `satellite_id`.
- PlanetScope-style filename support must at least handle stems beginning with `YYYYMMDD_HHMMSS`; source id can be the full stem or useful leading tokens, but must be stable.
- Cloud percentage from filename can be best-effort for explicit tokens such as `cloud12`, `cloud_12.5`, `cloud-cover-12`, or `cc12`.
- A valid footprint requires readable raster metadata, positive width/height, CRS, and finite non-zero bounds.

### Previous Story Learnings

- Keep source-of-truth state writes inside `WorkspaceService`; this story should not add any workspace writes.
- Existing models use Pydantic v2 and `ConfigDict(extra="forbid")` for persisted schemas. Ingestion-only transient result objects may use dataclasses if not persisted.
- Existing tests run headlessly and must not require network, LAN paths, or a Qt event loop.
- Use the conda/uv command pattern from `_bmad-output/project-context.md` because plain `uv` may not be on PATH.

### Project Structure Notes

- Expected new files:
  - `src/thucthengay/ingestion/metadata_parser.py`
  - `src/thucthengay/ingestion/scanner.py`
  - `tests/unit/test_ingestion_scanner.py`
- Expected updates:
  - `src/thucthengay/ingestion/__init__.py`
  - possibly `src/thucthengay/models/layer.py` and `src/thucthengay/models/__init__.py` if `needs_manual_correction` must be exposed exactly.

### Testing Requirements

- Add tiny GeoTIFF fixtures at test runtime using `rasterio`; do not commit binary test imagery.
- Tests must cover acceptance criteria and failure paths.
- Run full suite and ruff after implementation:
  - `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest`
  - `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .`
  - `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay`

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.1-Scan-Imagery-Folder-and-Extract-GeoTIFF-Metadata]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-3-Scan-and-match-GeoTIFF-imagery]
- [Source: _bmad-output/planning-artifacts/architecture.md#GIS-Spatial-Architecture]
- [Source: _bmad-output/project-context.md#Critical-Implementation-Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Red test: `pytest tests/unit/test_ingestion_scanner.py` failed on missing `scan_imagery_folder` import before implementation.
- Focused green test: `pytest tests/unit/test_ingestion_scanner.py` -> 6 passed.
- Full regression: `pytest` -> 54 passed.
- Lint: `ruff check .` -> All checks passed.
- App smoke: `python -m thucthengay` with `DISPLAY`/`WAYLAND_DISPLAY` unset -> `3.ThucTheNgay app ready.`
- Review patch gate: `pytest` -> 55 passed; `ruff check .` -> All checks passed; app smoke -> `3.ThucTheNgay app ready.`

### Completion Notes List

- Added recursive GeoTIFF discovery for `.tif`/`.tiff` files with deterministic ordering and unsupported-file ignore behavior.
- Added sidecar, filename, and embedded tag business metadata parsing with source tracking for capture date/time, cloud percent, and source identifier.
- Added rasterio metadata extraction for CRS, bounds, transform, dimensions, band count, nodata, and tags; invalid/unreadable rasters produce warning `Issue` objects and are excluded from valid scan output.
- Added `needs_manual_correction` metadata status for Epic 2 while preserving the previous `needs_correction` enum value.
- Added focused unit tests with runtime-generated tiny GeoTIFF fixtures.
- Code review patch added stable unique layer IDs for duplicate filenames discovered in different subfolders.

### File List

- `_bmad-output/implementation-artifacts/2-1-scan-imagery-folder-and-extract-geotiff-metadata.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/ingestion/__init__.py`
- `src/thucthengay/ingestion/metadata_parser.py`
- `src/thucthengay/ingestion/scanner.py`
- `src/thucthengay/models/layer.py`
- `tests/unit/test_ingestion_scanner.py`

### Change Log

- 2026-05-25: Created story context for Epic 2 Story 2.1.
- 2026-05-25: Implemented GeoTIFF scan and metadata extraction; story moved to review.
- 2026-05-25: Addressed code review patch for duplicate layer IDs; story marked done.
