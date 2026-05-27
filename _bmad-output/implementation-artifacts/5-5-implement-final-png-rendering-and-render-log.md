# Story 5.5: Implement Final PNG Rendering and Render Log

Status: done

## Story

As an Operator,
I want final map PNGs generated at template output quality,
So that exported PPTX slides use reliable image assets.

## Acceptance Criteria

1. Given a composition passes render readiness validation, when final render runs, then it creates a PNG using target config, template metadata, output size, visible layers, view center/scale, grid, background, and map frame aspect from the shared render spec, and the output dimensions match the requested template output quality.
2. Given final PNG rendering succeeds, when the result is recorded, then the render log includes output path, PNG width/height, composition reference, render spec revision or hash, visible layer references, and timestamp, and the composition can reference the final render artifact through workspace-relative path where possible.
3. Given final rendering fails, when the failure is recorded, then the render log includes the composition reference and failure reason, and export can block or skip according to preflight/export rules rather than embedding a missing image.
4. Given final render output already exists for an older composition revision, when the composition state has changed, then the app treats the prior render as stale, and a fresh final render is required before export uses the asset.

## Tasks / Subtasks

- [x] Add final render log/result contracts (AC: 2, 3, 4)
  - [x] Extend render models with typed final render status, log entry, log file, and result contracts.
  - [x] Include composition id, target id, workspace-relative output path, width/height, render spec hash, visible layer refs, timestamp, failure reason, and issues.
  - [x] Keep models JSON-friendly with `extra="forbid"` and focused round-trip tests.
- [x] Implement final PNG renderer in `render/` (AC: 1, 2, 3)
  - [x] Reuse `render_map(spec, ...)` so raster, background, and coordinate-frame behavior match preview.
  - [x] Save PNG through Pillow using an atomic temp-file replace so partial PNGs are never success artifacts.
  - [x] Write a render log entry for both success and expected render failures.
  - [x] Keep `render/` independent from Qt/editor and avoid export PPTX generation in this story.
- [x] Persist final render artifact references through workspace service (AC: 2, 4)
  - [x] Add a workspace method to record final render path/log path on a composition.
  - [x] Prefer workspace-relative paths under `renders/` when workspace root is known.
  - [x] Ensure composition edits that mark validation stale also invalidate prior final render artifact references.
- [x] Add stale-final-render detection (AC: 4)
  - [x] Hash the canonical render spec used for final PNG output.
  - [x] Provide a deterministic check that rejects missing files, failed logs, mismatched paths, and mismatched spec hashes.
  - [x] Cover stale detection after view/layer/grid changes through unit tests.
- [x] Add focused tests and quality gates (AC: 1, 2, 3, 4)
  - [x] Test final PNG dimensions and log contents with a synthetic render function.
  - [x] Test failure logging does not leave a successful output path.
  - [x] Test workspace artifact persistence and invalidation on edits.
  - [x] Test render import boundaries remain Qt/editor-free.
  - [x] Run `pytest`, `ruff check .`, and `python -m thucthengay --smoke`.

### Review Findings

- [x] [Review][Patch] Validate final canvas dimensions before recording success [`src/thucthengay/render/final.py:60`]
- [x] [Review][Patch] Reject final artifact paths outside workspace `renders/` during currentness checks [`src/thucthengay/render/final.py:121`]

## Dev Notes

- Owner modules:
  - `render/` owns headless preview/final image rendering and must not import PySide6 or `editor`.
  - `workspace/` is the only module that writes composition JSON and should own artifact path persistence.
  - `export/` will consume final PNGs in Epic 6; do not implement PPTX/TXT export here.
- Reuse existing render pipeline:
  - `render/spec.py` provides `RenderSpec` and `build_render_spec()`.
  - `render/core.py` provides `render_map(spec, is_cancelled=...)`.
  - `render/raster.py` provides `RasterRenderResult` and `RenderError`.
  - `models/composition.py` already has `CompositionArtifacts.final_render_path` and `export_log_path`.
- Final rendering must use the same source of truth as preview: `view.center`, `view.scale`, visible layer order, grid/frame config, background, map frame aspect, and output dimensions from the shared `RenderSpec`.
- "Grid" in Epic 5 means the coordinate/map frame with edge coordinate labels; Story 5.3 implemented this as `draw_coordinate_frame()`, not an internal cell mesh.
- Stale detection should be based on the canonical `RenderSpec` hash plus file/log presence. A changed composition should either clear the prior artifact reference or fail the currentness check before export.
- User-facing failures must use shared `Issue` with Vietnamese message/remediation where possible.
- Use Pillow, already in `pyproject.toml`, for PNG writing. Do not add dependencies.
- Tests should use synthetic canvases/render functions when possible; do not require real GeoTIFF/PPTX files for this story.
- Preserve Story 5.4 behavior: preview jobs stay in memory and do not persist preview artifacts or logs.

### Project Structure Notes

- Expected new file: `src/thucthengay/render/final.py`.
- Likely updates: `src/thucthengay/render/__init__.py`, `src/thucthengay/models/render.py`, `src/thucthengay/models/__init__.py`, `src/thucthengay/workspace/service.py`, and focused tests under `tests/unit/`.
- Keep import-boundary tests green: core `render/` must not import PySide6 or `thucthengay.editor`.

### References

- [Source: _bmad-output/project-context.md#Epic 5 Rendering Engine Mandate]
- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.5]
- [Source: _bmad-output/planning-artifacts/architecture.md#Rendering Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Export Architecture]
- [Source: _bmad-output/implementation-artifacts/5-4-implement-two-stage-preview-rendering-jobs.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests\unit\test_final_render.py tests\unit\test_workspace_service.py -k "final_render"` - RED failed before implementation because `FinalRenderStatus` was missing; passed after model/render/workspace implementation (`4 passed`).
- `conda run -n ttn-env pytest tests\unit\test_final_render.py tests\unit\test_workspace_service.py tests\unit\test_models.py tests\unit\test_core_import_boundaries.py` with workspace `TEMP/TMP` - passed (`46 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check src\thucthengay\render\final.py src\thucthengay\render\__init__.py src\thucthengay\models\render.py src\thucthengay\models\composition.py src\thucthengay\models\__init__.py src\thucthengay\workspace\service.py tests\unit\test_final_render.py tests\unit\test_workspace_service.py tests\unit\test_models.py` - passed.
- `conda run -n ttn-env pytest` with workspace `TEMP/TMP` - full regression passed (`242 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check .` - All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - App ready.
- `conda run -n ttn-env pytest tests\unit\test_final_render.py tests\unit\test_workspace_service.py tests\unit\test_models.py tests\unit\test_core_import_boundaries.py` with workspace `TEMP/TMP` after code review fixes - passed (`48 passed`, one pytest cache permission warning).
- `conda run -n ttn-env pytest` with workspace `TEMP/TMP` after code review fixes - full regression passed (`244 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check .` after code review fixes - All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` after code review fixes - App ready.

### Completion Notes List

- Added final render status/log/result/currentness models with JSON round-trip tests.
- Added `render/final.py` with canonical `RenderSpec` hashing, final PNG writing under `renders/`, atomic temp-file replace, success/failure render log entries, and deterministic currentness checks.
- Reused `render_map()` as the default final render path so raster, background, and coordinate-frame behavior stay shared with preview.
- Added workspace persistence for `final_render_path` and `render_log_path`, and invalidated those references when composition edits mark validation stale.
- Kept final render code Qt/editor-free and did not implement PPTX/TXT export scope.
- Code review fixed final PNG dimension validation and artifact currentness path hardening.

### File List

- `_bmad-output/implementation-artifacts/5-5-implement-final-png-rendering-and-render-log.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/models/composition.py`
- `src/thucthengay/models/render.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/render/final.py`
- `src/thucthengay/render/__init__.py`
- `src/thucthengay/workspace/service.py`
- `tests/unit/test_final_render.py`
- `tests/unit/test_models.py`
- `tests/unit/test_workspace_service.py`

## Change Log

- 2026-05-26: Created Story 5.5 artifact with final PNG/render log scope and moved status to ready-for-dev.
- 2026-05-26: Implemented final PNG rendering, render log/currentness checks, workspace artifact persistence, and focused tests. Quality gates passed; moved to review.
- 2026-05-26: Completed code review fixes, reran quality gates, and moved status to done.
