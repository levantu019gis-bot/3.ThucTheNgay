# Story 2.6: Show Ingestion Summary and Warnings

Status: done

## Story

As an Operator,
I want a clear ingestion summary after `Lấy dữ liệu`,
so that I know what was created and what needs attention before review.

## Acceptance Criteria

1. Given ingestion completes successfully or with warnings, when the summary is shown, then it displays scanned images, matched images, targets with images, created compositions, warning count, and workspace path, and the summary distinguishes success-with-warnings from hard failure.
2. Given warnings were produced during scan, metadata extraction, matching, or cache copy, when the Operator opens the warning list, then each warning includes scope, affected target/composition/layer/file when known, Vietnamese message, and remediation text where actionable.
3. Given no imagery matches any enabled target, when ingestion completes, then the summary shows an explicit empty state and explains likely causes such as disabled targets, non-intersecting imagery, invalid GeoTIFF footprints, or incorrect input folder.
4. Given compositions were created, when the Operator proceeds to Review/Edit, then the workspace manifest and composition index provide the created target-date compositions to the next mode, and no UI code reads raw composition JSON directly outside `WorkspaceService`.

## Tasks / Subtasks

- [x] Add ingestion summary contracts (AC: 1, 2, 3, 4)
  - [x] Convert `IngestionJobResult` and workspace path into a stable summary model.
  - [x] Normalize warning rows with scope, affected object, message, remediation, and Review/Edit surfacing flag.
  - [x] Include explicit no-match empty state copy.
- [x] Add Qt summary/warnings display (AC: 1, 2, 3)
  - [x] Render summary counters, status, workspace path, and created composition count.
  - [x] Render warning list rows without reading raw composition JSON.
  - [x] Expose a Setup-mode method for showing the latest ingestion summary.
- [x] Add focused tests and run quality gates (AC: 1, 2, 3, 4)

## Dev Notes

- Owner modules: `src/thucthengay/jobs/ingestion_summary.py` and `src/thucthengay/editor/widgets/ingestion_summary.py`.
- UI code may consume summary models and `WorkspaceService`, but must not parse composition JSON directly.
- Warning rows should preserve original `Issue` semantics and add display helpers only.
- Keep core summary code free of Qt/editor imports.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.6-Show-Ingestion-Summary-and-Warnings]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Component-Strategy]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Focused green test: `pytest tests/unit/test_ingestion_summary.py` -> 4 passed.
- Full regression: `pytest` -> 77 passed.
- Lint: `ruff check .` -> All checks passed.
- App smoke: `python -m thucthengay` with `DISPLAY`/`WAYLAND_DISPLAY` unset -> `3.ThucTheNgay app ready.`
- Review result: clean after internal review; no open findings.

### Completion Notes List

- Added `IngestionSummary` and `IngestionWarningItem` models for stable post-ingestion summary/warning display.
- Warning rows include scope, affected target/composition/layer/file identifier, message, remediation, and a flag for Review/Edit surfacing.
- Added explicit no-match empty-state messaging for disabled targets, non-intersecting imagery, invalid footprints, and incorrect input folders.
- Added `IngestionSummaryWidget` and `SetupMode.show_ingestion_summary()` so Setup can display the latest result without parsing raw composition JSON.

### File List

- `_bmad-output/implementation-artifacts/2-6-show-ingestion-summary-and-warnings.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/modes/setup_mode.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/widgets/ingestion_summary.py`
- `src/thucthengay/jobs/__init__.py`
- `src/thucthengay/jobs/ingestion_summary.py`
- `tests/unit/test_ingestion_summary.py`

### Change Log

- 2026-05-25: Created story context for Epic 2 Story 2.6.
- 2026-05-25: Implemented ingestion summary and warnings display, then marked story done after internal review.
