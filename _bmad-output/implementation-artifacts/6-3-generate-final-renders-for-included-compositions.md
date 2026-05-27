# Story 6.3: Generate Final Renders for Included Compositions

Status: done

## Story

As an Operator,
I want export to use current final map renders,
So that the PPTX contains the same map state I approved during review.

## Acceptance Criteria

1. Given an included composition has no current final PNG render, when export preparation runs, then the app requests final rendering using the shared render pipeline from Epic 5, and export waits for a successful current render before using the image.
2. Given an included composition has a stale final render, when preflight or export detects the stale revision, then it schedules or requires a fresh render, and it does not embed the stale PNG into PPTX output.
3. Given final render generation fails for an included composition, when export preparation records the result, then export is blocked or the composition is skipped only according to explicit preflight/export rules, and the failure appears in summary/log with composition reference and remediation where possible.
4. Given final render succeeds, when export continues, then the PPTX export receives the workspace-relative or resolved final PNG path, and the render log can trace the PNG to its composition and render spec revision.

## Tasks / Subtasks

- [x] Build headless export final-render preparation service (AC: 1, 2, 3, 4)
  - [x] Add an `export/` orchestration module that selects included compositions through `WorkspaceService` without importing Qt.
  - [x] Build canonical final `RenderSpec` per included composition from `Composition`, `TargetConfig`, and Story 6.1 `TargetConfig.metadata["template_metadata"]`.
  - [x] Use a deterministic output-size policy derived from the template map frame and keep it under `render.spec.MAX_RENDER_PIXELS`.
  - [x] Return typed per-composition results and aggregate summary so later PPTX/TXT/log stories can consume the final PNG paths.
- [x] Detect current, missing, and stale final renders before export (AC: 1, 2)
  - [x] Reuse `is_final_render_current()` and `render_spec_hash()` instead of only checking that a PNG path exists.
  - [x] Treat missing artifact references, missing files/logs, failed latest logs, output-size mismatch, and spec-hash mismatch as requiring a fresh render.
  - [x] Ensure stale existing PNGs are never exposed as export-ready outputs.
- [x] Generate and persist fresh final renders (AC: 1, 3, 4)
  - [x] Reuse `render_final_png()` from `render/final.py` so raster/background/frame rendering remains shared with Epic 5.
  - [x] On success, persist `final_render_path` and `render_log_path` through `WorkspaceService.record_final_render_artifacts()`.
  - [x] On failure, surface structured `Issue` objects with Vietnamese remediation and do not persist a successful final PNG reference.
  - [x] Support cancellation callback passthrough for long-running export preparation.
- [x] Integrate currentness with export preflight (AC: 2, 3)
  - [x] Update `build_export_preflight_plan()` so existing final render paths are checked for currentness when target/template metadata is available.
  - [x] Add explicit export issues for stale or uncheckable final renders rather than treating any existing PNG as valid.
  - [x] Keep Story 6.2 UI behavior intact: preflight explains blockers; final PPTX export remains for Story 6.4.
- [x] Tests and gates (AC: 1, 2, 3, 4)
  - [x] Unit tests for render preparation: current render skipped, missing/stale render regenerated, workspace artifacts persisted, failure blocks output, and cancellation/failure issues.
  - [x] Unit tests for preflight stale/current final-render detection.
  - [x] Run focused tests, full `pytest`, `ruff check .`, and app smoke.

## Dev Notes

- Owner modules:
  - `export/` owns headless export preparation orchestration and must not import Qt/editor.
  - `render/` owns PNG generation, render spec hashing, and currentness detection.
  - `workspace/` remains the only writer of composition artifact references.
  - `editor/` should not gain export business logic in this story.
- Reuse existing contracts:
  - `build_render_spec()` and `RenderSpecError` in `src/thucthengay/render/spec.py`.
  - `render_final_png()`, `is_final_render_current()`, and `render_spec_hash()` in `src/thucthengay/render/final.py`.
  - `WorkspaceService.record_final_render_artifacts()` in `src/thucthengay/workspace/service.py`.
  - `build_export_preflight_plan()` in `src/thucthengay/export/preflight.py`.
  - Story 6.1 template metadata stored at `TargetConfig.metadata["template_metadata"]`.
- This story does not implement combined PPTX copy/replacement, TXT writing, or export summary/log writing. Those remain Stories 6.4-6.6.
- Preflight from Story 6.2 currently checks only that `final_render_path` exists and that the referenced file exists. Story 6.3 must harden that to check render-log/spec currentness when enough context exists.
- The final render output-size policy should be conservative and deterministic. Use map-frame dimensions from template metadata converted to pixels at a fixed final-render DPI unless a future config field exists.
- If target/template metadata is missing or invalid, return export/render issues; do not synthesize a render spec from partial template state.
- Long-running behavior can remain headless/synchronous in this story as long as the public API accepts a cancellation callback and returns structured progress-ready results. Qt job wiring can be added later if needed.
- Failure path must not write a success artifact reference into composition JSON. Render logs may contain failure entries from `render_final_png()`.

### Project Structure Notes

- Expected new or updated files:
  - `src/thucthengay/export/final_render.py`
  - `src/thucthengay/export/preflight.py`
  - `src/thucthengay/export/__init__.py`
  - `src/thucthengay/models/export.py`
  - `src/thucthengay/models/__init__.py`
  - focused tests under `tests/unit/`
- Keep import-boundary tests green: export/render core modules must not import `PySide6` or `thucthengay.editor`.

### Previous Story Intelligence

- Story 6.2 added export plan models, `build_export_preflight_plan()`, Export mode UI, and tests. It intentionally treated missing final renders as blocking and did not trigger render generation.
- Story 6.2 review fixed target/global template issue attribution in preflight; preserve that issue counting behavior when adding stale-render issues.
- Story 5.5 already implemented final PNG writing, success/failure render logs, workspace-relative artifact persistence, and deterministic currentness checks.
- Story 5.5 invalidates final render artifact references when composition edits mark validation stale, but export still needs to detect stale paths from old JSON/log combinations.
- Full gates after Story 6.2 passed: `260 passed`, `ruff check .`, and app smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.3]
- [Source: _bmad-output/planning-artifacts/architecture.md#Export Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Rendering Architecture]
- [Source: _bmad-output/implementation-artifacts/5-5-implement-final-png-rendering-and-render-log.md]
- [Source: _bmad-output/implementation-artifacts/6-2-build-export-preflight-and-export-plan-ui.md]
- [Source: _bmad-output/project-context.md#Module Ownership Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_final_render.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - RED failed before implementation because `ExportFinalRenderStatus` was missing; passed after implementation (`6 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_final_render.py tests/unit/test_export_preflight_plan.py tests/unit/test_final_render.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed after updating preflight fixtures for current render logs (`14 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_final_render.py tests/unit/test_export_preflight_plan.py tests/unit/test_export_mode.py tests/unit/test_final_render.py tests/unit/test_workspace_service.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`42 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest -q -p no:cacheprovider --basetemp=.tmp/pytest` - full regression passed (`266 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - passed.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Created comprehensive Story 6.3 context and moved sprint status to ready-for-dev.
- Added headless export final-render preparation service that builds canonical export render specs, skips current PNGs, regenerates missing/stale PNGs, and returns typed row/summary results.
- Added deterministic final output sizing from PPTX map-frame points at fixed final-render DPI with a MAX_RENDER_PIXELS guard.
- Integrated preflight currentness checks so stale/missing-log/mismatched final renders block export instead of any existing PNG being accepted.
- Added focused unit tests and updated export mode/preflight fixtures to use current render logs.
- Verified focused, full regression, ruff, and app smoke gates.
- Code review completed clean with no patch findings; Story 6.3 is done.

### File List

- `_bmad-output/implementation-artifacts/6-3-generate-final-renders-for-included-compositions.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/export/final_render.py`
- `src/thucthengay/export/preflight.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/export.py`
- `tests/unit/test_export_final_render.py`
- `tests/unit/test_export_mode.py`
- `tests/unit/test_export_preflight_plan.py`

## Change Log

- 2026-05-26: Created Story 6.3 artifact and moved status to ready-for-dev.
- 2026-05-26: Started implementation and moved status to in-progress.
- 2026-05-26: Implemented export final-render preparation/currentness integration and moved status to review.
- 2026-05-26: Code review completed clean; moved status to done.
