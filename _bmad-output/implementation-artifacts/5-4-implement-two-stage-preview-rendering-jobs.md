# Story 5.4: Implement Two-Stage Preview Rendering Jobs

Status: done

## Story

As an Operator,
I want preview rendering to update quickly while I edit,
So that pan/zoom/layer changes feel responsive without sacrificing settled preview quality.

## Acceptance Criteria

1. Given the Operator changes layer visibility/order, view center/scale, grid, or metadata affecting preview, when preview rendering is requested, then the app schedules a low-resolution interactive preview first and schedules a settled higher-resolution preview after debounce.
2. Given the Operator continues editing while preview jobs are running, when an older preview job completes after a newer request exists, then the app ignores the stale result and only applies results matching the current composition/render revision.
3. Given a preview render is running in a background job, when progress or result updates are emitted, then updates are delivered safely to the Qt main thread and core render services remain independent from Qt widgets.
4. Given preview rendering fails, when the preview panel receives the failure, then it shows `render_error` state with actionable Vietnamese text where possible, and the Operator can continue editing and trigger a later preview.

## Tasks / Subtasks

- [x] Add preview job contracts in `jobs/render_job.py` (AC: 1, 2, 3, 4)
  - [x] Define immutable request/revision models for interactive and settled preview quality.
  - [x] Define preview progress/result/failure payloads that carry `job_id`, composition id, revision, quality, output size, issues, and optional canvas.
  - [x] Keep the job contract Qt-free; use `Issue` and existing `JobState`/progress patterns.
- [x] Implement preview job execution using the existing render pipeline (AC: 1, 3, 4)
  - [x] Call `render_map(spec, is_cancelled=...)` so Story 5.3 raster/background/frame behavior is reused.
  - [x] Emit running and terminal progress events without touching widgets.
  - [x] Convert `RenderError`/unexpected exceptions into structured failure results with Vietnamese remediation.
  - [x] Check cancellation/staleness between stages so obsolete preview work can stop early.
- [x] Implement two-stage scheduling/state model (AC: 1, 2)
  - [x] Provide a controller/model that starts an interactive low-res request immediately.
  - [x] Provide a debounced settled high-res request path.
  - [x] Track the latest revision token and reject stale results deterministically.
  - [x] Do not persist preview artifacts or final render logs in this story.
- [x] Integrate preview job results with `SlidePreviewWidget`/Review Edit without blocking UI (AC: 2, 3, 4)
  - [x] Preserve existing debounced preview states and stale-result rejection behavior.
  - [x] Apply only current-revision results to the preview panel.
  - [x] Surface failure details through `render_error` text and allow later requests.
  - [x] Keep Qt usage inside `editor/` or job adapters, not inside `render/`.
- [x] Add focused tests (AC: 1, 2, 3, 4)
  - [x] Unit-test two-stage scheduling order: interactive first, settled after debounce.
  - [x] Unit-test stale result rejection for older revision/job ids.
  - [x] Unit-test render errors become structured failure/progress payloads with Vietnamese text.
  - [x] Unit-test Qt-free boundaries for `render/` and core job contracts.
  - [x] Update existing preview widget tests only where required by the new job path.
- [x] Run quality gates
  - [x] `pytest`
  - [x] `ruff check .`
  - [x] `python -m thucthengay --smoke`

### Review Findings

- [x] [Review][Patch] Prevent late interactive low-res result from overwriting already-applied settled high-res preview result
  [`src/thucthengay/jobs/render_job.py`, `src/thucthengay/editor/widgets/slide_preview.py`]

## Dev Notes

- Project mandate: Epic 5 render work must prioritize responsiveness, memory control, cancellation/stale handling, and recovery from abnormal render state.
- Owner modules:
  - `render/` owns headless image rendering and must not import PySide6 or `editor`.
  - `jobs/` owns background job contracts, progress events, cancellation and stale-update adapters.
  - `editor/` owns Qt widgets/timers/signals and may adapt job events to UI state.
- Existing reusable pieces:
  - `render/spec.py` provides `RenderSpec`, `build_render_spec()`, `GeoWindow`, `RenderBackground`.
  - `render/core.py` provides `render_map(spec, is_cancelled=...)` and raises `RenderError` with structured issues.
  - `jobs/progress.py` provides `JobState`, `ProgressEvent`, `QueuedProgressDispatcher`, and `ActiveJobProgressModel`.
  - `editor/widgets/slide_preview.py` already has `SlidePreviewState`, `PreviewRequestToken`, debounce behavior, stale token rejection, and `set_render_error()`.
  - `editor/widgets/gis_canvas.py` already has render request token/state methods for stale result rejection.
- Preview quality should be represented explicitly, for example `interactive_low_res` and `settled_high_res`; do not infer quality only from dimensions or labels.
- The low-res and high-res previews must share the same render source of truth as final: composition view center/scale, visible layer order, grid/frame config, background, and map frame aspect. Resolution may differ, math must not.
- For this story, preview output may stay in memory as a NumPy canvas/result object. Do not write final PNGs, render logs, or export artifacts; those belong to Story 5.5.
- The UI currently shows deterministic text preview. Replace or wrap only the parts needed to exercise the job lifecycle; avoid broad visual redesign.
- User-facing failures must use Vietnamese text and should prefer messages/remediations from `Issue` when available.
- Tests should avoid real long-running threads where deterministic model tests are enough. If Qt timers/signals are touched, keep tests small and use existing `qapp()` patterns.

### Project Structure Notes

- Expected new file: `src/thucthengay/jobs/render_job.py`.
- Likely updates: `src/thucthengay/jobs/__init__.py`, `src/thucthengay/editor/widgets/slide_preview.py`, and focused tests under `tests/unit/`.
- Keep import-boundary tests green: core `render/` and job contracts must not import `thucthengay.editor`; `render/` must not import PySide6.

### References

- [Source: _bmad-output/project-context.md#Epic 5 Rendering Engine Mandate]
- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.4]
- [Source: _bmad-output/planning-artifacts/architecture.md#Rendering Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Slide Preview Panel]
- [Source: _bmad-output/implementation-artifacts/5-3-render-grid-and-map-background-without-mvp-extras.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests\unit\test_render_job.py` - RED failed before implementation because preview job contracts were missing; passed after implementation (`5 passed`).
- `conda run -n ttn-env pytest tests\unit\test_review_edit_mode.py -k "preview_job or slide_preview_applies" tests\unit\test_render_job.py` - RED failed on missing `SlidePreviewWidget.track_preview_plan`; passed after widget adapter implementation.
- `conda run -n ttn-env pytest tests\unit\test_render_job.py tests\unit\test_review_edit_mode.py tests\unit\test_core_import_boundaries.py` with workspace `TEMP/TMP` - passed (`37 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check src\thucthengay\jobs src\thucthengay\editor\widgets\slide_preview.py tests\unit\test_render_job.py tests\unit\test_review_edit_mode.py` - fixed line-length/unused import findings, then passed.
- `conda run -n ttn-env pytest` with workspace `TEMP/TMP` - full regression passed (`235 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check .` - All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - App ready.
- `conda run -n ttn-env pytest tests\unit\test_render_job.py tests\unit\test_review_edit_mode.py -k "late_low_res"` with workspace `TEMP/TMP` - review regression test passed (`2 passed`).
- `conda run -n ttn-env ruff check src\thucthengay\jobs\render_job.py src\thucthengay\editor\widgets\slide_preview.py tests\unit\test_render_job.py tests\unit\test_review_edit_mode.py` - passed after review fix.
- `conda run -n ttn-env pytest` with workspace `TEMP/TMP` - full regression passed after review fix (`237 passed`, one pytest cache permission warning).
- `conda run -n ttn-env ruff check .` - All checks passed after review fix.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - App ready after review fix.

### Completion Notes List

- Added Qt-free preview render job contracts and execution in `jobs/render_job.py`, including explicit `interactive_low_res` and `settled_high_res` quality values, revision/job ids, output dimensions, issues, optional canvas payload, and progress events.
- Implemented `PreviewRenderController` to create immediate low-res and debounced settled preview requests, resize only output dimensions while preserving render math source fields, and reject stale job results deterministically.
- Reused `render_map(spec, is_cancelled=...)` for preview execution so raster/background/coordinate-frame behavior remains shared with Stories 5.2 and 5.3.
- Added `SlidePreviewWidget` adapter methods to track two-stage preview plans, apply only current-revision results, and show recoverable render errors without changing core render/job module boundaries.
- Added focused unit coverage for scheduling order, stale rejection, progress/success payloads, render error payloads, Qt-free job contracts, and preview widget job-result handling.
- Code review fix added quality-rank guards so a late `interactive_low_res` result cannot overwrite an already-applied `settled_high_res` result for the same revision.

### File List

- `_bmad-output/implementation-artifacts/5-4-implement-two-stage-preview-rendering-jobs.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/jobs/render_job.py`
- `src/thucthengay/jobs/__init__.py`
- `src/thucthengay/editor/widgets/slide_preview.py`
- `tests/unit/test_render_job.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-26: Created Story 5.4 artifact with preview job orchestration scope and moved status to ready-for-dev.
- 2026-05-26: Implemented two-stage preview render job contracts/controller, widget result adapter, and focused tests. Quality gates passed; moved to review.
- 2026-05-26: Completed code review fix for late low-res overwrite, reran quality gates, and moved Story 5.4 to done.
