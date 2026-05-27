# Story 5.6: Verify Preview/Final Alignment with Fixtures

Status: done

## Story

As a Developer,
I want tests that compare preview and final render behavior,
So that future changes do not break map output fidelity.

## Acceptance Criteria

1. Given test fixtures include config, GeoJSON, GeoTIFF, template metadata, and workspace composition data, when render tests run, then they cover render spec creation, raster window selection, layer ordering, grid rendering, and final PNG output, and tests can run without launching the Qt UI.
2. Given the same composition state is rendered as preview and final output, when alignment checks compare the two outputs at appropriate tolerances, then they confirm center/scale, layer order, grid placement, and background behavior remain consistent, and known resolution differences between preview and final are accounted for explicitly.
3. Given a composition includes hidden layers and reordered visible layers, when fixtures are rendered, then tests verify hidden layers do not appear and visible order affects output as expected, and newest-on-top default behavior is covered when no manual order override exists.
4. Given invalid render inputs are supplied in fixtures, when render services run, then tests assert structured errors or issues are returned, and no partial final PNG is treated as successful output.

## Tasks / Subtasks

- [x] Add headless render alignment fixtures (AC: 1)
  - [x] Create tests that materialize config, GeoJSON, GeoTIFF, template metadata, and composition JSON under `tmp_path`.
  - [x] Load fixture data through project models and build `RenderSpec` without Qt.
- [x] Verify preview/final alignment behavior (AC: 1, 2)
  - [x] Render preview and final from the same composition state.
  - [x] Compare normalized sample points so resolution differences are explicit.
  - [x] Assert coordinate frame/background/raster placement remain aligned.
- [x] Verify layer visibility and ordering behavior (AC: 3)
  - [x] Assert hidden layers are excluded from `RenderSpec` and render output.
  - [x] Assert visible layer order affects output.
  - [x] Cover ingestion default newest-first ordering.
- [x] Verify invalid fixture handling (AC: 4)
  - [x] Assert structured render issues for invalid raster input.
  - [x] Assert final render failure writes no successful PNG artifact.
- [x] Run focused tests and quality gates (AC: 1, 2, 3, 4)
  - [x] Run focused render alignment tests.
  - [x] Run relevant render/model regression tests.
  - [x] Run `ruff check .`, `pytest`, and `python -m thucthengay --smoke`.

## Dev Notes

- Story 5.6 is a verification story. Prefer focused tests around existing render APIs over new product behavior unless an alignment defect is exposed.
- Owner modules:
  - `render/` owns headless preview/final rendering and must remain free of Qt/editor imports.
  - `jobs/render_job.py` owns preview request sizing and stale-result behavior.
  - `render/final.py` owns final PNG persistence and currentness checks.
- Existing APIs to reuse:
  - `build_render_spec()` from `render/spec.py`.
  - `render_map()` from `render/core.py`.
  - `run_preview_render_job()` and `PreviewRenderController` from `jobs/render_job.py`.
  - `render_final_png()` from `render/final.py`.
- Coordinate "grid" means the Story 5.3 coordinate frame with edge labels/ticks, not an internal cell mesh.
- Alignment checks should account for preview/final output size differences explicitly. Use normalized sample points or deterministic downsampling rather than byte-for-byte equality across resolutions.
- Tests should use synthetic fixture data and `rasterio` temporary GeoTIFFs, not require real operator data or launching the PySide6 UI.

### References

- [Source: _bmad-output/project-context.md#Rendering Engine Mandate]
- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.6]
- [Source: _bmad-output/implementation-artifacts/5-5-implement-final-png-rendering-and-render-log.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; conda run -n ttn-env pytest tests\unit\test_render_alignment.py -q` - passed (`4 passed`).
- `conda run -n ttn-env ruff check tests\unit\test_render_alignment.py` - passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env pytest tests\unit\test_render_alignment.py tests\unit\test_render_core.py tests\unit\test_render_raster.py tests\unit\test_render_spec.py tests\unit\test_final_render.py tests\unit\test_render_job.py -q` - passed (`48 passed`).
- `$env:PYTHONPATH='src'; $env:TEMP="$PWD\.tmp"; $env:TMP="$PWD\.tmp"; conda run -n ttn-env pytest -q` - full regression passed (`248 passed`).
- `conda run -n ttn-env ruff check .` - All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - App ready.

### Completion Notes List

- Added fixture-based render alignment tests that create config, GeoJSON, temporary GeoTIFFs, template metadata, and composition JSON under `tmp_path`.
- Verified preview/final rendering from the same `RenderSpec` using normalized samples to account for preview/final resolution differences.
- Covered hidden-layer exclusion, visible layer ordering impact, default newest-first ingestion ordering, structured invalid-raster failure, and no partial final PNG success artifact.
- No production render code changes were required for Story 5.6.

### Review Notes

- 2026-05-26: BMad code review completed. Clean review; no decision-needed, patch, or deferred findings.

### File List

- `_bmad-output/implementation-artifacts/5-6-verify-preview-final-alignment-with-fixtures.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `tests/unit/test_render_alignment.py`

## Change Log

- 2026-05-26: Created Story 5.6 artifact and moved status to in-progress.
- 2026-05-26: Added fixture-based preview/final alignment tests, ran quality gates, and moved status to review.
- 2026-05-26: Completed BMad code review and moved story to done.
