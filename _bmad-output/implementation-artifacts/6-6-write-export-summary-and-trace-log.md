# Story 6.6: Write Export Summary and Trace Log

Status: done

## Story

As an Operator,
I want export summary and logs written next to the output files,
So that I can verify what was generated and diagnose skipped or failed items.

## Acceptance Criteria

1. Given export completes successfully, with warnings, or with recoverable skipped items, when the export summary is shown and written, then it includes slide count, target count, skipped count, warnings, errors if any, PPTX output path, TXT output path, and log path, and the UI distinguishes success, success-with-warnings, and failure states.
2. Given compositions are exported or skipped, when the trace log is written, then it maps each composition to PPTX slide number, TXT line number, exported/skipped status, and skipped reason where applicable, and it includes an issue summary for warnings/errors encountered during preflight/export.
3. Given an output file cannot be written due to permission, locked file, or missing folder, when export attempts to write it, then the app reports a blocking export error with Vietnamese remediation, and it does not report export success for incomplete outputs.
4. Given export artifacts are written into the workspace or selected output folder, when the operation finishes, then output paths are recorded in workspace/export state or export log as appropriate, and the Operator can inspect the files outside the application.

## Tasks / Subtasks

- [x] Add export completion/log contracts (AC: 1, 2, 4)
  - [x] Extend shared export models with completion state, trace entries, issue summary, and summary/log result models.
  - [x] Keep the existing `ExportLog` model backward-compatible while adding fields needed by Story 6.6.
- [x] Implement headless summary/trace log writer (AC: 1, 2, 3, 4)
  - [x] Add `src/thucthengay/export/log_writer.py`.
  - [x] Build summary metrics from preflight, PPTX result, and TXT result.
  - [x] Write one UTF-8 JSON log inside the workspace and return workspace-relative `log_path`.
  - [x] Return blocking Vietnamese `Issue` objects when the log path is outside workspace or cannot be written.
- [x] Trace exported and skipped compositions (AC: 2)
  - [x] Map composition id to PPTX slide number and TXT line number when both outputs export the row.
  - [x] Mark blocking preflight rows or missing output rows as skipped/failed with a clear skipped reason.
  - [x] Include grouped issue counts by issue id and severity.
- [x] Tests and gates (AC: 1, 2, 3, 4)
  - [x] Unit test success summary/log JSON with PPTX/TXT paths and exported trace rows.
  - [x] Unit test warning or skipped rows produce `success_with_warnings`.
  - [x] Unit test write failure/out-of-workspace path returns a blocking export issue and no success state.
  - [x] Run focused tests, full `pytest`, `ruff check .`, and app smoke.

## Dev Notes

- Owner modules:
  - `export/` owns log/summary generation and must not import Qt/editor.
  - `models/` owns reusable export contracts consumed by UI and tests.
  - `workspace/` remains the path boundary and source of workspace-relative artifact paths.
- Reuse existing contracts:
  - `ExportPreflightPlan` / `ExportPlanRow` from `src/thucthengay/models/export.py`.
  - `ExportPptxResult` from Story 6.4.
  - `ExportTxtResult` from Story 6.5.
  - Existing `Issue` model for blocking write/path errors.
- Completion state rules:
  - `success` only when PPTX/TXT results are ok, there are no errors, and no skipped rows.
  - `success_with_warnings` when output succeeds but warnings or recoverable skipped rows exist.
  - `failure` when any blocking/error issue exists, any required output result is not ok, or log writing fails.
- Trace rows should be deterministic in export/preflight order and workspace paths should be workspace-relative where possible.
- This story writes headless contracts/logs only. UI wiring can consume the state/result but does not need a new widget in this story.

### Project Structure Notes

- Expected new or updated files:
  - `src/thucthengay/export/log_writer.py`
  - `src/thucthengay/export/__init__.py`
  - `src/thucthengay/models/export.py`
  - `src/thucthengay/models/__init__.py`
  - focused tests under `tests/unit/`
- Keep import-boundary tests green: export core modules must not import `PySide6` or `thucthengay.editor`.

### Previous Story Intelligence

- Story 6.4 established workspace-contained output path resolution, PPTX result models, and concrete PowerPoint file tests.
- Story 6.5 established TXT result models, deterministic review_order output, and blocking Vietnamese export issues.
- Story 6.5 explicitly left combined summary/log writing for this story.
- Full gates after Story 6.5 passed: `274 passed`, `ruff check .`, and app smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.6]
- [Source: _bmad-output/planning-artifacts/architecture.md#Export Architecture]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Export]
- [Source: _bmad-output/implementation-artifacts/6-4-export-combined-pptx-from-target-specific-sample-slides.md]
- [Source: _bmad-output/implementation-artifacts/6-5-export-txt-report-lines.md]
- [Source: _bmad-output/project-context.md#Module Ownership Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_log_writer.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - RED expected before implementation because `thucthengay.export.log_writer` does not exist.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_log_writer.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed after implementation (`4 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_txt_exporter.py::test_export_txt_report_rejects_out_of_workspace_output_path tests/unit/test_pptx_exporter.py::test_export_combined_pptx_rejects_out_of_workspace_output_path -q -p no:cacheprovider --basetemp=.tmp/pytest` - RED exposed PPTX/TXT outside-workspace path exceptions; passed after review patch (`2 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check --fix src/thucthengay/export/log_writer.py src/thucthengay/export/pptx_exporter.py src/thucthengay/export/txt_exporter.py tests/unit/test_export_log_writer.py tests/unit/test_pptx_exporter.py tests/unit/test_txt_exporter.py` - fixed formatting/import ordering only.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_log_writer.py tests/unit/test_txt_exporter.py tests/unit/test_pptx_exporter.py tests/unit/test_export_preflight_plan.py tests/unit/test_models.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed after review patch (`31 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest -q -p no:cacheprovider --basetemp=.tmp/pytest` - full regression passed (`280 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - passed.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Created comprehensive Story 6.6 context and moved sprint status to ready-for-dev.
- Started implementation and moved sprint status to in-progress.
- Added completion state, trace entry, issue summary, and log write result models while preserving existing `ExportLog` round-trip behavior.
- Added `write_export_summary_and_trace_log()` to write UTF-8 JSON summary/trace logs inside the workspace, with workspace-relative PPTX/TXT/log paths.
- Added deterministic trace mapping from preflight rows to PPTX slide numbers and TXT line numbers, including skipped/failed reasons and grouped issue counts.
- Code review patch hardened output write errors across PPTX, TXT, and log writing so invalid/out-of-workspace paths return blocking Vietnamese export issues instead of reporting success or throwing uncaught exceptions.
- Verified focused, full regression, ruff, and app smoke gates; Story 6.6 is done.

### File List

- `_bmad-output/implementation-artifacts/6-6-write-export-summary-and-trace-log.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/export/log_writer.py`
- `src/thucthengay/export/pptx_exporter.py`
- `src/thucthengay/export/txt_exporter.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/export.py`
- `tests/unit/test_export_log_writer.py`
- `tests/unit/test_pptx_exporter.py`
- `tests/unit/test_txt_exporter.py`

## Change Log

- 2026-05-26: Created Story 6.6 artifact and moved status to ready-for-dev.
- 2026-05-26: Started implementation and moved status to in-progress.
- 2026-05-26: Implemented export summary and trace log writer.
- 2026-05-26: Hardened PPTX/TXT/log output write errors and moved status to done.
