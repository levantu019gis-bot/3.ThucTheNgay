# Story 2.5: Run Ingestion as Progress Job

Status: done

## Story

As an Operator,
I want ingestion to run with visible progress,
so that large imagery folders do not make the desktop app feel stalled.

## Acceptance Criteria

1. Given the Operator starts `Lấy dữ liệu`, when ingestion begins, then it runs through the app job/progress model instead of blocking the UI thread and progress updates are delivered safely to the Qt main thread.
2. Given ingestion is running, when progress changes, then the UI can display scanned image count, matched image count, targets with images, warning count, current target, and matched count for the current target, and the progress model supports idle, running, success, warning, and error states.
3. Given ingestion encounters warnings for specific files or targets, when progress is reported, then warning counts update without stopping the whole job unless a fatal setup-level error occurs, and warnings remain available for the post-ingestion summary.
4. Given ingestion is superseded by a new run or cancelled by the operator where cancellation is supported, when a stale progress update arrives, then the app ignores stale updates for the previous job and workspace state is not marked complete until the active job finishes successfully or with warnings.

## Tasks / Subtasks

- [x] Add job progress contracts (AC: 1, 2, 3, 4)
  - [x] Define progress event fields for job id, stage/state, counters, current target, warning count, and issues.
  - [x] Provide an active-job progress model that ignores stale updates.
  - [x] Provide a queue/dispatcher contract that can be drained by the Qt main thread.
- [x] Implement ingestion job orchestration (AC: 1, 2, 3)
  - [x] Run scan, target matching, workspace cache population, and composition creation in order.
  - [x] Emit progress updates after each phase and per target match summary.
  - [x] Treat config/workspace setup failures as fatal errors while retaining non-fatal ingest warnings.
- [x] Add focused tests and run quality gates (AC: 1, 2, 3, 4)

## Dev Notes

- Owner modules: `src/thucthengay/jobs/progress.py` and `src/thucthengay/jobs/ingestion_job.py`.
- Keep jobs headless-testable. Do not import `PySide6`, `editor`, or UI widgets from core job modules.
- Qt main-thread safety should be represented by a core dispatcher/queue contract; the UI adapter can connect it to Qt signals in a later story.
- Reuse Epic 2 ingestion services: `scan_imagery_folder`, `match_imagery_to_targets`, `populate_workspace_cache`, and `create_target_date_compositions`.
- Fatal setup-level errors include invalid/missing config or workspace initialization/clear failures. Per-file and per-target ingestion issues should remain in progress/summary issues and allow other valid data to continue.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.5-Run-Ingestion-as-Progress-Job]
- [Source: _bmad-output/planning-artifacts/architecture.md#FR-3-to-FR-5-Ingestion]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Focused green test: `pytest tests/unit/test_ingestion_job.py` -> 5 passed.
- Full regression: `pytest` -> 73 passed.
- Lint: `ruff check .` -> All checks passed.
- App smoke: `python -m thucthengay` with `DISPLAY`/`WAYLAND_DISPLAY` unset -> `3.ThucTheNgay app ready.`
- Review result: clean after internal review; no open findings.

### Completion Notes List

- Added a headless progress event model with idle/running/success/warning/error states and ingestion counters required by the UI.
- Added a thread-safe queued dispatcher and active-job progress model so UI adapters can drain updates on the Qt main thread and ignore stale job updates.
- Added an ingestion job orchestrator that runs scan, match, cache, and composition creation while preserving non-fatal warnings for summary display.
- Fatal config/workspace setup failures now stop the job with an error state before workspace completion.

### File List

- `_bmad-output/implementation-artifacts/2-5-run-ingestion-as-progress-job.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/jobs/__init__.py`
- `src/thucthengay/jobs/ingestion_job.py`
- `src/thucthengay/jobs/progress.py`
- `tests/unit/test_ingestion_job.py`

### Change Log

- 2026-05-25: Created story context for Epic 2 Story 2.5.
- 2026-05-25: Implemented ingestion progress job and marked story done after internal review.
