# Story 4.3: Run Validation on Select, Include, and Export Preflight

Status: done

<!-- Note: Created from Epic 4 backlog context and started immediately per project autonomous execution mandate. -->

## Story

As an Operator,
I want validation to run at the moments where decisions are made,
so that stale or invalid state cannot slip into ready or export output.

## Acceptance Criteria

1. Given the Operator selects a composition, when selection completes, then detailed validation issues are recomputed for that composition, and validation summary is persisted through `WorkspaceService`.
2. Given the Operator presses Right or clicks Include/Validate, when validation passes with no blocking errors, then the app may set ready/include according to review workflow rules, and the validation summary records the passing state.
3. Given the Operator presses Right or clicks Include/Validate, when validation returns a blocking error, then the app does not set `ready=true` or `include=true`, and the selected composition remains active for correction.
4. Given export preflight starts, when included compositions are checked, then detailed validation is recomputed for each included composition, and any blocking error prevents export from starting.
5. Given validation details are recomputed, when the workspace is saved, then only the summary is persisted in composition JSON, and detailed issues remain derived state for the current app session/UI.

## Tasks / Subtasks

- [x] Run validation on Review/Edit selection (AC: 1, 5)
  - [x] Recompute detailed readiness issues after selection.
  - [x] Persist compact summary through `WorkspaceService.save_validation_summary()`.
  - [x] Keep detailed issues in UI/session only.
- [x] Run validation on Include/Revalidate decisions (AC: 2, 3, 5)
  - [x] Include persists current validation summary before transition.
  - [x] Blocking issues prevent `ready/include` transition and keep selection active.
  - [x] Revalidate persists pass/fail summary without promoting ready/include.
- [x] Add export preflight validation helper (AC: 4, 5)
  - [x] Recompute detailed validation for each included composition context.
  - [x] Return blocking result if any included composition has blocking issues.
  - [x] Do not write workspace or export files from validation.
- [x] Add focused tests (AC: 1-5)
  - [x] Test selection persists compact summary without storing detailed issues in JSON.
  - [x] Test Include pass and Include blocked persist appropriate summary state.
  - [x] Test export preflight aggregates blocking issues.

### Review Findings

- [x] [Review][Patch] Remove stale local review-gate code and repair UTF-8 text corruption introduced during cleanup [`src/thucthengay/editor/modes/review_edit_mode.py`]

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `editor/modes/review_edit_mode.py`: validation timing for selection/include/revalidate through workspace service.
  - `validation/composition_rules.py`: readiness result source of truth.
  - `validation/export_preflight.py`: core export preflight contract only; no file output and no UI.
  - `workspace/service.py`: persists only compact summaries and review transitions.
- Scope guard:
  - Do not implement Warnings panel rows/tree issue indicators; Story 4.4 owns detailed UI surfacing.
  - Do not implement metadata editor; Story 4.5 owns correction UI.
  - Do not implement final export generation; Epic 6 owns PPTX/TXT export.
  - Template metadata loading remains outside validation; Review/Edit may consume parsed `target.metadata["template_metadata"]` when present.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.3]
- [Source: _bmad-output/implementation-artifacts/4-1-define-validation-engine-and-issue-schema.md]
- [Source: _bmad-output/implementation-artifacts/4-2-validate-composition-readiness-rules.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_review_edit_mode.py tests/unit/test_composition_readiness_validation.py` - 33 passed.
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest` - 123 passed.
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - all checks passed.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Review/Edit now recomputes readiness validation on selection and persists only `ValidationSummary` through `WorkspaceService`.
- Include/Validate persists the current validation summary and blocks ready/include transitions when readiness validation returns blocking issues.
- Revalidate persists pass/fail summaries without promoting ready/include state.
- Added `validate_export_preflight()` to recompute detailed validation for export candidate contexts without mutating workspace/export files.
- Added focused tests for compact summary persistence, transition blocking, and export preflight aggregation.
- Resolved review finding by removing stale gate code and repairing affected UTF-8 UI/test strings.

### File List

- `_bmad-output/implementation-artifacts/4-3-run-validation-on-select-include-and-export-preflight.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `src/thucthengay/validation/__init__.py`
- `src/thucthengay/validation/export_preflight.py`
- `tests/unit/test_composition_readiness_validation.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context from Epic 4 backlog and started implementation.
- 2026-05-25: Implemented validation timing, export preflight helper, focused tests, review fix, and marked done.
