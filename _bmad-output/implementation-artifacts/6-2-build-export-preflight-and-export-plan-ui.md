# Story 6.2: Build Export Preflight and Export Plan UI

Status: done

## Story

As an Operator,
I want to see a preflight summary and export plan before exporting,
So that I can fix blocking issues and understand exactly what will be generated.

## Acceptance Criteria

1. Given the Operator enters Export mode, when export preflight runs, then it validates included compositions, target-specific PPTX templates, required element-id mappings, required renders, TXT placeholders, and blocking composition issues, and it recomputes detailed validation for included compositions rather than trusting stale summaries.
2. Given preflight completes, when the Export Summary Metrics are shown, then they include included slides, target count, skipped count, warning count, error count, and preflight state, and blocking errors disable the final export action with a tooltip or message explaining why.
3. Given included compositions are available, when the Export Plan is rendered, then each row shows slide number, target alias/title, date/time label, template status, issue count, and jump back action to the composition, and rows are sorted by `review_order`.
4. Given a plan row has an issue, when the Operator activates its jump action, then the app navigates back to the related Review/Edit composition or target context, and the issue remains visible for correction.

## Tasks / Subtasks

- [x] Build headless export preflight planning contract (AC: 1, 2, 3)
  - [x] Add export plan/preflight result models in `models/export.py` or a focused export module without importing Qt.
  - [x] Select candidates from workspace compositions where `include=true`, preserving all included rows even when stale/blocked so the UI can explain skipped/blocked state.
  - [x] Sort planned rows by `review_order`; compositions missing `review_order` must surface an export issue instead of receiving an implicit order.
  - [x] Aggregate summary metrics: included slide count, unique target count, skipped/blocked count, warnings, errors, and preflight state.
- [x] Recompute included-composition validation for export (AC: 1)
  - [x] Reuse `validate_export_preflight()` and `validate_composition_readiness()` instead of trusting persisted `validation_summary`.
  - [x] Build `ValidationContext` for each included composition from target config plus derived Story 6.1 `target.metadata["template_metadata"]`.
  - [x] Pass Story 6.1 `template_compatibility_issues()` results into export preflight so unknown/incompatible multi-template cases appear in Export mode.
- [x] Add Story 6.2 export-specific checks without implementing export (AC: 1, 2)
  - [x] Required render check: included composition must have a current-enough `artifacts.final_render_path` before final export can be enabled; for Story 6.2, a missing final render is a blocking preflight issue or explicit "not ready for export" state, not a render job trigger.
  - [x] Template mapping check: required map image and required text/image placeholder element-id mappings must be present in target config or derived template load issues.
  - [x] TXT placeholder check: validate that the configured TXT line template can be resolved far enough to block unresolved required placeholders; do not write TXT in this story.
- [x] Implement Export mode UI shell and summary metrics (AC: 2)
  - [x] Add `editor/modes/export_mode.py` using Qt Widgets only.
  - [x] Add `editor/widgets/export_summary.py` for compact metric display and preflight state text.
  - [x] Add Export tab to `AppShell` after Review/Edit.
  - [x] Expose one primary disabled/export placeholder action and a secondary `Preflight` action; final export must remain disabled when blocking errors exist because Stories 6.3-6.6 are not implemented yet.
- [x] Implement export plan model/view and jump action (AC: 3, 4)
  - [x] Add `editor/models/export_plan_model.py` with stable row height, display roles, issue count, target/composition refs, and tooltip/remediation text.
  - [x] Render columns/fields: slide number, target alias/title, composition date/time label, template status, issue count, and jump action affordance.
  - [x] When a row issue/jump is activated, switch to Review/Edit and call the existing issue navigation path (`ReviewEditMode._handle_issue_jump` or a small public wrapper) without making UI write workspace JSON directly.
- [x] Tests and gates (AC: 1, 2, 3, 4)
  - [x] Unit tests for export preflight plan sorting, summary counts, stale/recomputed validation, missing render issue, template compatibility propagation, and placeholder/TXT checks.
  - [x] Qt/offscreen tests for Export mode tab, summary metrics, disabled final export with tooltip/message, export plan row data, and jump-to-review behavior.
  - [x] Run focused tests, full `pytest`, `ruff check .`, and app smoke.

### Review Findings

- [x] [Review][Patch] Attach target/global template issues to export plan rows and avoid duplicate summary counting in `src/thucthengay/export/preflight.py`.

## Dev Notes

- Owner modules:
  - `models/` owns shared export/preflight/plan data contracts.
  - `validation/` owns reusable `Issue` returning rules; it must not mutate workspace.
  - `export/` may own headless preflight orchestration helpers, template compatibility integration, and future export services; it must not import Qt widgets.
  - `editor/` owns PySide6 Export mode widgets/models only.
  - `workspace/` remains the only owner of composition JSON reads/writes.
- This story is UI and preflight planning only. Do not implement final PNG rendering jobs (Story 6.3), PPTX copy/replacement (Story 6.4), TXT writer (Story 6.5), or summary/log writer (Story 6.6).
- Export preflight must not trust persisted `validation_summary`; it recomputes detailed issues for included compositions. Persisted summaries can help display existing state, but blocking/export decisions come from fresh `Issue` objects.
- Do not use `WorkspaceService.included_export_candidates()` as the only source for plan rows because it intentionally drops stale/errored compositions. Story 6.2 needs to show included-but-blocked/skipped rows so the Operator can fix them.
- Reuse existing contracts:
  - `ValidationContext`, `ValidationResult`, `validate_export_preflight()` in `src/thucthengay/validation/`.
  - `Issue`, `IssueSeverity`, `IssueScope` in `src/thucthengay/models/issue.py`.
  - `Composition.artifacts.final_render_path`, `include`, `ready`, `needs_revalidation`, and `review_order` in `src/thucthengay/models/composition.py`.
  - Story 6.1 derived template metadata in `TargetConfig.metadata["template_metadata"]`.
  - Existing Review/Edit issue navigation behavior in `ReviewEditMode`.
- Target/title display should prefer `TargetConfig.name` and fall back to `target.id`. Plan sorting must use `review_order`, not target/date or manifest order.
- Time label for a row should derive from visible valid layers in the same way validation/readiness expects. If no valid visible layer can produce a label, surface a blocking issue rather than inventing a placeholder.
- Required render check in this story is deliberately conservative: missing `final_render_path` blocks/enables remediation. Actual scheduling/generation of final renders belongs to Story 6.3.
- TXT placeholder validation should be minimal and headless: identify unresolved required tokens/config gaps and return `Issue`. Writing TXT lines belongs to Story 6.5.
- UI expectations:
  - Export mode is a dashboard, not a Review/Edit canvas clone.
  - Summary metrics must show included slides, targets, skipped/blocked, warnings, errors, and preflight state.
  - Blocking errors disable final export with visible Vietnamese remediation/tooltip.
  - Status must not rely on color alone; use text/icon/tooltip.
  - Use Qt model/view (`QTableView` or `QListView`) for the export plan.
  - Keep dense desktop layout with stable row heights and no nested decorative cards.

### Project Structure Notes

- Expected new or updated files:
  - `src/thucthengay/models/export.py`
  - `src/thucthengay/validation/export_preflight.py`
  - `src/thucthengay/export/` helper module if orchestration grows beyond validation helpers
  - `src/thucthengay/editor/app_shell.py`
  - `src/thucthengay/editor/modes/export_mode.py`
  - `src/thucthengay/editor/models/export_plan_model.py`
  - `src/thucthengay/editor/widgets/export_summary.py`
  - focused tests under `tests/unit/`
- Avoid adding business logic to `app.py` or UI widgets. UI should call a headless builder/service and render returned models.
- No new third-party dependency is needed. Use current stack from `pyproject.toml`: Python 3.11, PySide6, Pydantic v2, pytest, ruff.

### Previous Story Intelligence

- Story 6.1 completed direct one-slide PPTX template loading and now propagates derived `TemplateMetadata` into `TargetConfig.metadata["template_metadata"]`.
- Story 6.1 added `template_compatibility_issues()` and patched `validate_export_preflight(..., template_issues=...)`; Story 6.2 must consume those issues from Export mode, not leave compatibility only at config-load time.
- Story 6.1 review fixed duplicate/ambiguous placeholder guards. Story 6.2 should rely on those structured template issues and avoid duplicating python-pptx shape parsing in UI code.
- Review/Edit already has `_validation_context_for()` and issue jump behavior. Export mode should reuse or extract a small shared context builder if needed, rather than implementing a second incompatible validation path.
- Full gates after Story 6.1 passed: `254 passed`, `ruff check .`, and app smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.2]
- [Source: _bmad-output/planning-artifacts/epics.md#FR18-FR23]
- [Source: _bmad-output/planning-artifacts/architecture.md#Export Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#FR-20-to-FR-23-Export]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UJ-4-Export-bao-cao]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Export-Summary-Metrics]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Export-Plan-Row]
- [Source: _bmad-output/project-context.md#Module Ownership Rules]
- [Source: _bmad-output/implementation-artifacts/6-1-load-target-specific-powerpoint-template-metadata.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_export_preflight_plan.py tests/unit/test_export_mode.py tests/unit/test_composition_readiness_validation.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`18 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - passed.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`260 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Created comprehensive Story 6.2 context and moved sprint status to ready-for-dev.
- Added headless export preflight planning with sorted plan rows, summary metrics, recomputed readiness validation, render/template/TXT checks, and compatibility issue propagation.
- Added Export mode UI with summary metrics, preflight action, disabled final export placeholder, plan table, and jump-to-Review/Edit behavior.
- Added focused unit/offscreen Qt tests and verified full regression/lint/smoke gates.
- Resolved code review finding for template issue attribution/counting and reran focused/full gates.

### File List

- `_bmad-output/implementation-artifacts/6-2-build-export-preflight-and-export-plan-ui.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/app_shell.py`
- `src/thucthengay/editor/models/export_plan_model.py`
- `src/thucthengay/editor/modes/export_mode.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/widgets/export_summary.py`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/export/preflight.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/export.py`
- `tests/unit/test_export_mode.py`
- `tests/unit/test_export_preflight_plan.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-26: Created Story 6.2 artifact and moved status to ready-for-dev.
- 2026-05-26: Started implementation and moved status to in-progress.
- 2026-05-26: Implemented export preflight/plan UI and moved status to review.
- 2026-05-26: Applied code review patch, reran gates, and moved status to done.
