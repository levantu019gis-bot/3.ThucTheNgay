# Story 6.4: Export Combined PPTX from Target-Specific Sample Slides

Status: done

## Story

As an Operator,
I want one combined PowerPoint report created from target-specific sample slides,
So that the final report is ordered and ready for delivery.

## Acceptance Criteria

1. Given preflight has passed and final renders exist for included compositions, when PPTX export runs, then it creates one combined PPTX containing one slide per included composition, and slides are ordered by composition `review_order`.
2. Given each included composition belongs to a target, when its slide is created, then the exporter copies the only slide from that target's template PPTX, and replaces the map image placeholder with the composition final PNG.
3. Given text placeholders are configured as PPTX element-id mappings in target export config, when the exporter creates a slide, then it replaces configured placeholders using composition, target, layer/time label, and export context values, and unresolved required placeholders create blocking export errors.
4. Given PowerPoint slide-copy logic is needed, when the implementation adds it, then risky copy behavior is isolated in `export/pptx_slide_copy.py`, and an initial vertical-slice test covers at least one target, one sample slide, and one exported slide.

## Tasks / Subtasks

- [x] Add combined PPTX export contracts and result models (AC: 1, 3)
  - [x] Extend shared export models with a PPTX export result/summary that can carry output path, exported slide rows, and structured blocking issues.
  - [x] Keep result data UI-neutral and serializable through Pydantic.
- [x] Implement headless combined PPTX exporter (AC: 1, 2, 3)
  - [x] Add `src/thucthengay/export/pptx_exporter.py` that selects included compositions through `WorkspaceService`, sorts by `review_order`, runs/reuses export preflight, and writes one combined PPTX.
  - [x] Resolve target template metadata from `TargetConfig.metadata["template_metadata"]` and target export placeholder config; do not parse raw config paths in the exporter.
  - [x] Block export with Vietnamese `Issue` objects when preflight has blocking errors, final PNG files are missing/unresolved, target metadata is missing, or required placeholders cannot be resolved.
  - [x] Return exported composition rows with slide numbers and render paths for Story 6.6 log writing.
- [x] Isolate PowerPoint slide copy and placeholder replacement (AC: 2, 4)
  - [x] Add `src/thucthengay/export/pptx_slide_copy.py` for copying the one template slide into the destination presentation.
  - [x] Replace the map image placeholder by configured element id using the final PNG, preserving the placeholder rectangle.
  - [x] Replace configured text placeholders by element id and leave optional unresolved placeholders empty.
- [x] Tests and gates (AC: 1, 2, 3, 4)
  - [x] Unit test vertical slice: one target, one template slide, one final PNG, one exported slide.
  - [x] Unit test multi-composition ordering by `review_order`.
  - [x] Unit test blocking issue for unresolved required text placeholder and missing final PNG.
  - [x] Run focused tests, full `pytest`, `ruff check .`, and app smoke.

## Dev Notes

- Owner modules:
  - `export/` owns PPTX generation and must not import Qt/editor.
  - `workspace/` remains the source of truth for included compositions and final render artifact paths.
  - `models/` owns reusable export result contracts.
- Reuse existing contracts:
  - `build_export_preflight_plan()` in `src/thucthengay/export/preflight.py`.
  - `ensure_final_renders_for_export()` outputs and persisted `Composition.artifacts.final_render_path` from Story 6.3.
  - `TemplatePlaceholder`, `PlaceholderType`, and `TemplateMetadata` in `src/thucthengay/models/template.py`.
  - `ExportedComposition` and `ExportLog` in `src/thucthengay/models/export.py`.
- PowerPoint details:
  - Use `python-pptx>=1.0`.
  - Target templates are one-slide PPTX files validated by Story 6.1.
  - Shape lookup is by configured PPTX element id (`shape.shape_id`); shape names are diagnostics only.
  - Copy-slide/XML relationship risk must stay in `export/pptx_slide_copy.py`.
  - This story writes PPTX only. TXT export and final export summary/log remain Stories 6.5 and 6.6.
- Placeholder values initially supported for text fields should match the export preflight/TXT field vocabulary where applicable: `capture_date`, `composition_id`, `slide_number`, `target_alias`, `target_id`, `target_name`, `target_title`, and `time_label`.
- Required unresolved placeholders are blocking errors; optional unresolved text placeholders may be cleared.

### Project Structure Notes

- Expected new or updated files:
  - `src/thucthengay/export/pptx_exporter.py`
  - `src/thucthengay/export/pptx_slide_copy.py`
  - `src/thucthengay/export/__init__.py`
  - `src/thucthengay/models/export.py`
  - `src/thucthengay/models/__init__.py`
  - focused tests under `tests/unit/`
- Keep import-boundary tests green: export core modules must not import `PySide6` or `thucthengay.editor`.

### Previous Story Intelligence

- Story 6.1 added direct target `export.template_pptx_file`, element-id placeholder mapping, `load_target_template()`, and compatibility warnings.
- Story 6.2 added `build_export_preflight_plan()` and export plan rows sorted by `review_order`.
- Story 6.3 hardened final-render currentness and persisted current final PNG/log paths before PPTX export.
- Full gates after Story 6.3 passed: `266 passed`, `ruff check .`, and app smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.4]
- [Source: _bmad-output/planning-artifacts/architecture.md#Export Architecture]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-05-26-epic-6-pptx-direct-template.md#Story 6.4]
- [Source: _bmad-output/implementation-artifacts/6-1-load-target-specific-powerpoint-template-metadata.md]
- [Source: _bmad-output/implementation-artifacts/6-2-build-export-preflight-and-export-plan-ui.md]
- [Source: _bmad-output/implementation-artifacts/6-3-generate-final-renders-for-included-compositions.md]
- [Source: _bmad-output/project-context.md#Module Ownership Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_pptx_exporter.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - RED failed before implementation because `export_combined_pptx` was missing; passed after implementation (`4 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_pptx_exporter.py tests/unit/test_export_final_render.py tests/unit/test_export_preflight_plan.py tests/unit/test_final_render.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`18 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_pptx_exporter.py tests/unit/test_export_final_render.py tests/unit/test_export_preflight_plan.py tests/unit/test_export_mode.py tests/unit/test_config_service.py tests/unit/test_core_import_boundaries.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`32 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest -q -p no:cacheprovider --basetemp=.tmp/pytest` - full regression passed (`270 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - initially failed on import order in `src/thucthengay/export/__init__.py`, passed after fix.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.
- Code review patch verification: updated the vertical-slice test template to include an existing logo image; RED exposed broken PPTX media relationship copy, then `pptx_slide_copy.py` was patched and focused test passed (`4 passed`).
- Final verification after review patch: full regression passed (`270 passed`), `ruff check .` passed, and app smoke passed.

### Completion Notes List

- Created comprehensive Story 6.4 context and moved sprint status to ready-for-dev.
- Started implementation and moved sprint status to in-progress.
- Added UI-neutral combined PPTX result models and exported them from `models`.
- Added headless `export_combined_pptx()` orchestration that preflights included compositions, sorts by `review_order`, copies target-specific template slides, replaces map/text placeholders by element id, and returns exported slide rows for later logs.
- Isolated template slide copy and element-id map/text replacement in `export/pptx_slide_copy.py`.
- Added focused PPTX export tests for vertical slice, review-order sorting, unresolved required text placeholder blocking, and missing final render blocking.
- Code review found and fixed one PPTX media relationship copy issue for template slides containing existing images/logos.
- Verified focused, full regression, ruff, and app smoke gates after the review patch; Story 6.4 is done.

### File List

- `_bmad-output/implementation-artifacts/6-4-export-combined-pptx-from-target-specific-sample-slides.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/export/pptx_exporter.py`
- `src/thucthengay/export/pptx_slide_copy.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/export.py`
- `tests/unit/test_pptx_exporter.py`

## Change Log

- 2026-05-26: Created Story 6.4 artifact and moved status to ready-for-dev.
- 2026-05-26: Started implementation and moved status to in-progress.
- 2026-05-26: Implemented combined PPTX export vertical slice and moved status to review.
- 2026-05-26: Fixed code review finding for PPTX image relationship copy; moved status to done.
