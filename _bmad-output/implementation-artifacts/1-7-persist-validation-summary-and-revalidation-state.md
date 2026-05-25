# Story 1.7: Persist Validation Summary and Revalidation State

Status: done

## Story

As an Operator,
I want validation status to persist without storing stale detailed issue lists,
So that the workspace shows reliable status while detailed issues are recalculated when needed.

## Requirement References

- FR8
- FR18
- AR4
- NFR2

## Acceptance Criteria

1. Given a validation service contract returns detailed issues and a summary for a composition, when the composition is saved, then only the validation summary is persisted in composition JSON, detailed issue lists remain derived state owned by the validation service, and Epic 1 defines the storage contract without implementing the full readiness rules.
2. Given layer, view center/scale, grid override, or metadata changes, when the change is saved, then the composition is marked `needs_revalidation=true`, and tree/status indicators can show that the prior validation is stale.
3. Given a composition has a persisted validation summary, when the workspace is reloaded, then aggregate status and counts can be displayed from the summary, and the app does not treat stale summaries as export-ready proof when `needs_revalidation=true`.
4. Given a validation summary is stored for a composition, when UI or export code reads the composition state, then it can distinguish clean, warning, error, and stale validation states from the persisted summary, and full blocking behavior for include/export decisions is implemented by Epic 4 validation stories.

## Implementation Context

- `Composition` already stores `validation_summary` and `needs_revalidation`.
- Full detailed validation rules and issue recomputation are owned by Epic 4.
- Epic 1 should persist only compact summary counts/timestamp and stale state.
- Workspace service remains the only owner of composition JSON writes.
- UI/export code needs a simple persisted-state helper but must not treat it as a substitute for Epic 4 export preflight.

## Tasks

- [x] Add persisted validation state helper for clean/warning/error/stale.
- [x] Add `WorkspaceService` method to save validation summaries without detailed issues.
- [x] Add `WorkspaceService` method to mark important composition edits as needing revalidation.
- [x] Add export-candidate helper that refuses stale persisted state.
- [x] Add unit tests for summary-only persistence, stale transitions, reload status, and export candidate filtering.
- [x] Run quality gates.

## Dev Agent Record

### Debug Log

- 2026-05-25: Confirmed Story 1.7 is the next backlog item after Story 1.6.
- 2026-05-25: Reviewed FR8/FR18 boundaries and confirmed full validation engine remains Epic 4.
- 2026-05-25: Implemented persisted validation state, summary save contract, stale marker, and export candidate filtering.
- 2026-05-25: Ran `pytest`, `ruff check .`, and `python -m thucthengay --smoke`; all passed.

### Completion Notes

- `Composition.persisted_validation_state` now distinguishes `stale`, `clean`, `warning`, and `error` from persisted fields only.
- `WorkspaceService.save_validation_summary()` persists compact validation summary and clears stale state.
- `WorkspaceService.mark_needs_revalidation()` marks edited compositions stale and clears ready/include/review order.
- `WorkspaceService.included_export_candidates()` refuses stale or errored persisted state while leaving full preflight to Epic 4.

### File List

- `_bmad-output/implementation-artifacts/1-7-persist-validation-summary-and-revalidation-state.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/composition.py`
- `src/thucthengay/workspace/service.py`
- `tests/unit/test_models.py`
- `tests/unit/test_workspace_service.py`

### Change Log

- 2026-05-25: Added story context and started implementation.
- 2026-05-25: Completed validation summary/revalidation state storage contract and tests.
