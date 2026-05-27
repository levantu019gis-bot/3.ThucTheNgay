# Story 6.5: Export TXT Report Lines

Status: done

## Story

As an Operator,
I want a TXT report generated alongside the PPTX,
So that each included composition has a corresponding text line for downstream reporting.

## Acceptance Criteria

1. Given included compositions are sorted by `review_order`, when TXT export runs, then it writes one line per included composition in the same order as the PPTX slides, and each line is rendered from the configured `txt_line_template`.
2. Given the TXT template references required placeholders, when placeholder values are resolved, then missing required values produce validation/export errors, and export does not silently write unresolved placeholder tokens.
3. Given the TXT template references optional placeholders, when optional values are missing, then they render empty only when marked optional by configuration, and this behavior is covered by tests or export validation fixtures.
4. Given a line requires a time label, when the line is rendered, then the time label comes from visible valid layers according to composition state, and unresolved metadata required for the time label blocks export with remediation pointing to metadata correction.

## Tasks / Subtasks

- [x] Add TXT export contracts and value resolver (AC: 1, 2, 3, 4)
  - [x] Extend shared export models with TXT result/summary data for output path, exported line rows, and structured issues.
  - [x] Add a shared TXT field resolver for `capture_date`, `composition_id`, `slide_number`, `target_alias`, `target_id`, `target_name`, `target_title`, and `time_label`.
  - [x] Resolve `time_label` only from visible layers with valid metadata and a capture time.
- [x] Implement headless TXT exporter (AC: 1, 2, 3, 4)
  - [x] Add `src/thucthengay/export/txt_exporter.py` that selects included compositions through `WorkspaceService`, sorts by `review_order`, runs/reuses export preflight, and writes one UTF-8 TXT file.
  - [x] Render one line per included composition from `TargetConfig.export.txt_line_template`.
  - [x] Block export with Vietnamese `Issue` objects when preflight has blocking errors, target config is missing, `txt_line_template` is missing, required placeholders are unknown/unresolved, or required `time_label` cannot be built.
  - [x] Support explicit optional placeholders using `{field?}` syntax until a future config schema provides a richer optional placeholder list.
- [x] Keep preflight behavior consistent with TXT exporter (AC: 2, 3, 4)
  - [x] Update `build_export_preflight_plan()` TXT checks to use the same placeholder resolver rules as the exporter.
  - [x] Ensure optional placeholders are allowed only when explicitly marked optional and required missing metadata remains blocking.
- [x] Tests and gates (AC: 1, 2, 3, 4)
  - [x] Unit test TXT vertical slice: two included compositions produce two lines sorted by `review_order`.
  - [x] Unit test required unknown/unresolved placeholders block without writing a TXT file.
  - [x] Unit test optional placeholders render empty only with `{field?}`.
  - [x] Unit test `time_label` ignores hidden/invalid layers and blocks when required visible-valid time is unavailable.
  - [x] Run focused tests, full `pytest`, `ruff check .`, and app smoke.

## Dev Notes

- Owner modules:
  - `export/` owns TXT generation and must not import Qt/editor.
  - `workspace/` remains the source of truth for included compositions.
  - `models/` owns reusable export result contracts.
- Reuse existing contracts:
  - `build_export_preflight_plan()` in `src/thucthengay/export/preflight.py`.
  - Existing preflight TXT supported field vocabulary in `src/thucthengay/export/preflight.py`.
  - Story 6.4 `export_combined_pptx()` ordering/export row pattern.
  - `ExportedComposition` and `ExportLog` models in `src/thucthengay/models/export.py`.
- TXT formatting rules:
  - Use Python format-template parsing with supported field names only.
  - Required placeholders use normal `{field}` syntax.
  - Optional placeholders use `{field?}` syntax in this story because current target config has no separate optional-placeholder schema.
  - Unknown required fields and unresolved required values are blocking export issues.
  - Optional unknown/unresolved fields render as empty only with `{field?}`.
  - Do not leave unresolved `{placeholder}` tokens in output.
- `time_label` must come from visible valid layers according to composition state. Hidden layers and invalid metadata layers do not satisfy required time metadata.
- This story writes TXT only. Combined export summary/log writing remains Story 6.6.

### Project Structure Notes

- Expected new or updated files:
  - `src/thucthengay/export/txt_exporter.py`
  - `src/thucthengay/export/preflight.py`
  - `src/thucthengay/export/__init__.py`
  - `src/thucthengay/models/export.py`
  - `src/thucthengay/models/__init__.py`
  - focused tests under `tests/unit/`
- Keep import-boundary tests green: export core modules must not import `PySide6` or `thucthengay.editor`.

### Previous Story Intelligence

- Story 6.2 added export preflight TXT checks but intentionally did not write TXT.
- Story 6.4 added a headless exporter pattern with preflight blocking, `review_order` sorting, workspace-relative output paths, and exported row models.
- Story 6.4 review found PowerPoint media-copy issues; not relevant to TXT, but keep export tests concrete and file-opening based rather than only checking return models.
- Full gates after Story 6.4 passed: `270 passed`, `ruff check .`, and app smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.5]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-22]
- [Source: _bmad-output/planning-artifacts/architecture.md#Export Architecture]
- [Source: _bmad-output/implementation-artifacts/6-2-build-export-preflight-and-export-plan-ui.md]
- [Source: _bmad-output/implementation-artifacts/6-4-export-combined-pptx-from-target-specific-sample-slides.md]
- [Source: _bmad-output/project-context.md#Module Ownership Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_txt_exporter.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - RED failed before implementation because `export_txt_report` was missing; passed after implementation (`4 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_txt_exporter.py tests/unit/test_export_preflight_plan.py tests/unit/test_export_mode.py tests/unit/test_pptx_exporter.py tests/unit/test_export_final_render.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`20 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check --fix src/thucthengay/export/txt_exporter.py src/thucthengay/export/txt_values.py src/thucthengay/export/preflight.py src/thucthengay/export/__init__.py src/thucthengay/models/export.py src/thucthengay/models/__init__.py tests/unit/test_txt_exporter.py` - fixed import ordering only.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_txt_exporter.py tests/unit/test_export_preflight_plan.py tests/unit/test_export_mode.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed after code review patch (`10 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest -q -p no:cacheprovider --basetemp=.tmp/pytest` - full regression passed (`274 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - passed.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Created comprehensive Story 6.5 context and moved sprint status to ready-for-dev.
- Started implementation and moved sprint status to in-progress.
- Added UI-neutral TXT export result models and exported them from `models`.
- Added shared TXT placeholder resolver with supported export fields, explicit `{field?}` optional syntax, and visible-valid-layer `time_label` resolution.
- Added headless `export_txt_report()` that writes one UTF-8 line per included composition sorted by `review_order`, returns exported line rows, and blocks unresolved required placeholders without writing output.
- Integrated the shared TXT resolver into export preflight so preflight/export issue behavior stays aligned.
- Code review tightened optional behavior so unknown placeholders remain blocking even when written as `{unknown?}`; optional empty rendering is limited to known supported fields.
- Verified focused, full regression, ruff, and app smoke gates; Story 6.5 is done.

### File List

- `_bmad-output/implementation-artifacts/6-5-export-txt-report-lines.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/export/preflight.py`
- `src/thucthengay/export/txt_exporter.py`
- `src/thucthengay/export/txt_values.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/export.py`
- `tests/unit/test_txt_exporter.py`

## Change Log

- 2026-05-26: Created Story 6.5 artifact and moved status to ready-for-dev.
- 2026-05-26: Started implementation and moved status to in-progress.
- 2026-05-26: Implemented TXT report export and preflight resolver alignment.
- 2026-05-26: Fixed code review finding for unknown optional placeholders; moved status to done.
