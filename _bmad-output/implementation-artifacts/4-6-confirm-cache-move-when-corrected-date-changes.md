# Story 4.6: Confirm Cache Move When Corrected Date Changes

Status: done

<!-- Created from Epic 4 backlog context per project autonomous execution mandate. -->

## Story

As an Operator,
I want date corrections that affect cache grouping to be explicit,
so that manual metadata fixes do not silently move files or change composition grouping.

## Acceptance Criteria

1. Given the Operator changes a layer capture date to a different target-date grouping, when they save the correction, then the app shows a confirmation dialog before moving cached files or regrouping the layer, and the safe/default action cancels the move/regroup operation.
2. Given the Operator confirms the date-changing correction, when the app applies it, then cached path references, composition layer membership, and affected composition summaries are updated through workspace services, and the operation is atomic enough that failed updates do not leave invalid composition JSON.
3. Given the move or regroup operation cannot be completed safely, when the app detects the failure, then it blocks the correction from being treated as fully applied, and it shows Vietnamese remediation explaining how to resolve the file/workspace issue.
4. Given a date correction changes which composition should contain the layer, when regrouping completes, then source and destination compositions are marked `needs_revalidation=true`, and review/include status is not silently promoted by the metadata correction.

## Tasks / Subtasks

- [x] Add `WorkspaceService.move_layer_between_compositions()` (AC: 2, 4)
  - [x] Signature: `move_layer_between_compositions(source_composition_id, layer_id, *, new_composition_id, new_target_id, new_capture_date, capture_time, cloud_percent, metadata_source, metadata_status) -> tuple[Composition, Composition]`.
  - [x] Read source composition; find and remove layer; mark stale.
  - [x] Read destination composition; if not found, create new composition shell with the layer's target_id, new capture_date, default ViewState (use source composition's view as starting point).
  - [x] Add layer with updated metadata + reorder index to end.
  - [x] Mark both compositions `needs_revalidation=true` and ensure include/ready not promoted.
  - [x] Atomic ordering: write destination first, then source; raise WorkspaceError if either fails with descriptive message.
  - [x] Tests: layer moves from source to existing dest; layer moves to newly-created dest; both compositions marked stale; ready/include not promoted; missing layer raises.

- [x] Build confirmation dialog helper (AC: 1)
  - [x] Add `confirm_date_change_dialog(layer_id, new_composition_id, parent) -> bool` in `editor/widgets/metadata_editor.py`.
  - [x] Uses `QMessageBox` with Vietnamese text, default button = Cancel (safe).
  - [x] Title: "Xác nhận đổi ngày"; text explains new composition_id will receive the layer and current one will lose it.
  - [x] Returns True only if user explicitly accepts.

- [x] Wire date-change detection into `ReviewEditMode._apply_layer_metadata` (AC: 1, 3, 4)
  - [x] Compute candidate composition_id from `target_id__YYYYMMDD` using new capture_date.
  - [x] If candidate != current composition_id and capture_date is not None: show confirmation dialog.
  - [x] On cancel: do nothing (no save).
  - [x] On confirm: call `WorkspaceService.move_layer_between_compositions(...)` instead of `update_layer_metadata`.
  - [x] On `WorkspaceError`: set `action_summary` with Vietnamese remediation text.
  - [x] After successful move: refresh tree projection; select destination composition.
  - [x] If capture_date is None (cleared), fall through to plain `update_layer_metadata` (no regroup).

- [x] Add focused tests (AC: 1-4)
  - [x] WorkspaceService `move_layer_between_compositions` unit tests covering both new-dest and existing-dest paths, atomicity, ready/include not promoted.
  - [x] Confirmation helper tests (mock QMessageBox.exec or use direct return value).
  - [x] ReviewEditMode integration: same-date save uses update_layer_metadata; cross-date save invokes move_layer (mock the confirmation).
  - [x] Run full pytest + ruff check + smoke test.

### Review Findings

- [x] [Review][Patch] Destination read failures were treated as missing destination compositions [src/thucthengay/workspace/service.py:315]
- [x] [Review][Patch] Cross-composition move bypassed nested ImageLayer validation [src/thucthengay/workspace/service.py:345]
- [x] [Review][Patch] Existing destination identity/duplicate layer conflicts were not blocked [src/thucthengay/workspace/service.py:317]
- [x] [Review][Patch] Source layer order was not normalized after removing the moved layer [src/thucthengay/workspace/service.py:357]
- [x] [Review][Patch] Source write failure could leave a newly written destination unrolled back [src/thucthengay/workspace/service.py:382]
- [x] [Review][Patch] Confirmation helper safe-default behavior lacked direct regression coverage [tests/unit/test_move_layer_date_change.py:512]
- [x] [Review][Patch] Move failure UI needed explicit Vietnamese remediation text [src/thucthengay/editor/modes/review_edit_mode.py:687]

## Dev Notes

- Follow `_bmad-output/project-context.md` for env/quality rules.
- Owner modules:
  - `workspace/service.py`: add `move_layer_between_compositions()`.
  - `editor/widgets/metadata_editor.py`: add `confirm_date_change_dialog` helper.
  - `editor/modes/review_edit_mode.py`: detect date change, show confirmation, dispatch to right service method.
- Scope guard:
  - This story does NOT physically move cache files on disk. `cache_path` references in `ImageLayer` keep pointing to the original cache file; cache file lifecycle is owned by Story 2.x ingestion. We only update composition JSON ownership.
  - Composition `composition_id` format: `target_id__YYYYMMDD` (existing convention).
  - Destination composition view defaults: when creating a new destination composition, copy `view` from source composition (operator can adjust later).
- Atomicity: write destination first (so if source write fails, the layer is duplicated, not lost — easier to recover than the inverse).
- After implementation: pytest + ruff + smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.6]
- [Source: src/thucthengay/workspace/service.py — `update_layer_metadata` pattern]
- [Source: src/thucthengay/editor/widgets/metadata_editor.py]
- [Source: src/thucthengay/editor/modes/review_edit_mode.py — `_apply_layer_metadata`]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- `conda run -n ttn-env pytest` — 166 passed.
- `conda run -n ttn-env ruff check .` — All checks passed.
- `PYTHONPATH=src conda run -n ttn-env python -m thucthengay --smoke` — App ready.
- `conda run -n ttn-env uv run --no-sync pytest tests/unit/test_move_layer_date_change.py` — 17 passed.
- `conda run -n ttn-env uv run --no-sync pytest tests/unit/test_move_layer_date_change.py tests/unit/test_metadata_editor.py tests/unit/test_review_edit_mode.py tests/unit/test_workspace_service.py` — 81 passed.
- `conda run -n ttn-env uv run --no-sync ruff check src/thucthengay/workspace/service.py src/thucthengay/editor/modes/review_edit_mode.py tests/unit/test_move_layer_date_change.py` — All checks passed.
- `conda run -n ttn-env uv run --no-sync pytest` — 207 passed.
- `conda run -n ttn-env uv run --no-sync ruff check .` — All checks passed.
- `conda run -n ttn-env uv run --no-sync python -m thucthengay --smoke` — App ready.

### Completion Notes List

- Added `WorkspaceService.move_layer_between_compositions()` — moves a layer from source to destination composition (creates dest if needed). Writes dest first, then source for safer recovery on partial failure. Returns `(updated_source, updated_dest)`.
- Both compositions are marked stale via `_mark_composition_edit_stale`, ensuring `needs_revalidation=true`, `ready=false`, `include=false`, `review_order=None`.
- Added `confirm_date_change_dialog()` helper using QMessageBox with Vietnamese text; default button = Cancel for safety.
- `ReviewEditMode._apply_layer_metadata` now detects date changes that cross target-date grouping (`{target_id}__{YYYYMMDD}` differs from current). If detected, prompts via `_confirm_date_change` (overridable for tests) and dispatches to `move_layer_between_compositions`; otherwise falls through to `update_layer_metadata`.
- 9 new tests in `test_move_layer_date_change.py`: workspace service (5) + ReviewEditMode integration (4).
- Code review fixes: destination JSON corruption now blocks instead of being treated as missing, existing destination target/date and duplicate layer conflicts are rejected, moved layer metadata is revalidated through `ImageLayer.model_validate`, source/destination orders are normalized, source-write failure rolls destination back best-effort, move failures show remediation text, and confirm dialog safe-default behavior has direct tests.

### File List

- `_bmad-output/implementation-artifacts/4-6-confirm-cache-move-when-corrected-date-changes.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/workspace/service.py`
- `src/thucthengay/editor/widgets/metadata_editor.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_move_layer_date_change.py`

## Change Log

- 2026-05-25: Created story context from Epic 4 backlog and started implementation.
- 2026-05-25: Implemented move_layer service + confirmation dialog + ReviewEditMode integration + 9 tests. Epic 4 complete.
- 2026-05-25: Code review found 7 patch findings; all fixed and full gates pass. Story marked done.
