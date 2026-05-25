# Story 3.2: Add Queue Filters and Empty States

Status: done

## Story

As an Operator,
I want queue filters for review status and issue severity,
so that I can focus on the compositions that need action.

## Acceptance Criteria

1. Given the Review/Edit tree has loaded compositions, when the filter bar is shown, then it provides filters: `Tất cả`, `Chưa duyệt`, `Ready`, `Include`, `Có warning`, and `Có error`, and each filter can show an aggregate count where the data is available.
2. Given the Operator selects a filter, when the filter is applied, then the tree only shows matching compositions while preserving target grouping where useful, and clearing the filter returns to the full queue without losing selection state when the selected composition remains visible.
3. Given a filter has no matching compositions, when the filtered view is rendered, then the UI shows an explicit empty state explaining that no compositions match the filter, and the empty state does not obscure the filter controls.
4. Given validation summary or review status changes, when the tree model refreshes, then filter counts and visible rows update consistently, and stale validation state can be represented distinctly from clean ready state.

## Tasks / Subtasks

- [x] Add queue filter support to the composition tree model (AC: 1, 2, 4)
  - [x] Add a typed queue filter enum/contract for `Tất cả`, `Chưa duyệt`, `Ready`, `Include`, `Có warning`, and `Có error`.
  - [x] Preserve target grouping while hiding target groups that have no visible composition matches.
  - [x] Recompute aggregate filter counts from the full composition set whenever model contents refresh.
  - [x] Treat stale validation distinctly from clean ready state in status/severity data.
- [x] Add filter controls and empty-state UI to Review/Edit mode (AC: 1, 2, 3)
  - [x] Add a stable filter bar above the tree without obscuring the tree or future panels.
  - [x] Display counts on filters when available.
  - [x] Show an explicit no-match empty state below the filter controls when a filter yields no compositions.
  - [x] Preserve selected composition when clearing/applying filters if the selected row remains visible.
- [x] Keep data access and ownership boundaries intact (AC: 2, 4)
  - [x] Continue loading compositions through `WorkspaceService.list_compositions()`.
  - [x] Continue loading selected details through `WorkspaceService.read_composition()`.
  - [x] Do not read raw workspace JSON from UI code.
- [x] Add focused tests (AC: 1-4)
  - [x] Test filter labels/counts and matching logic for review status and issue severity.
  - [x] Test filtered target grouping and no-match empty state.
  - [x] Test selection is preserved when the selected composition remains visible.
  - [x] Test refreshed review/validation state updates counts and visible rows.

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `editor/models/`: Qt tree model projection and filter state only.
  - `editor/modes/`: PySide6 Review/Edit widgets and selection preservation behavior.
  - `workspace/`: source of truth for manifest/composition JSON; UI must use `WorkspaceService`.
  - `models/`: shared Pydantic contracts; avoid adding duplicate persisted models for UI filters.
- Story 3.1 created `CompositionTreeModel` and `ReviewEditMode`; build on those classes rather than replacing the Review/Edit layout.
- Existing composition fields available for filters:
  - `reviewed`, `ready`, `include`, `needs_revalidation`, `review_order`
  - `validation_summary.warning_count`, `validation_summary.error_count`, `validation_summary.info_count`
  - `persisted_validation_state`, which is `STALE` when `needs_revalidation` is true, otherwise `ERROR`, `WARNING`, or `CLEAN`
- Required filters:
  - `Tất cả`: all compositions.
  - `Chưa duyệt`: compositions where `reviewed` is false.
  - `Ready`: compositions where `ready` is true and `include` is false.
  - `Include`: compositions where both `ready` and `include` are true.
  - `Có warning`: compositions whose persisted validation state is `WARNING` or whose summary has warnings.
  - `Có error`: compositions whose persisted validation state is `ERROR` or whose summary has errors.
- Stale validation should not be silently presented as clean ready; keep existing `STALE` severity/status text and ensure counts/filters refresh when `needs_revalidation` changes.
- UX requirements:
  - Queue Filter Bar options: `Tất cả`, `Chưa duyệt`, `Ready`, `Include`, `Có warning`, `Có error`.
  - Filter must not lose selection if the selected item remains visible.
  - If the filter hides all matching rows, show a clear empty state and keep filter controls visible.
- Keep scope tight: do not implement layer stack controls, GIS canvas controls, slide preview rendering, or review action transitions in this story.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.2]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-9]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Queue Filter Bar]
- [Source: _bmad-output/implementation-artifacts/3-1-build-review-edit-layout-and-composition-tree.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `pytest tests/unit/test_review_edit_mode.py` - 7 passed.
- `pytest` - 84 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.

### Completion Notes List

- Added typed `QueueFilter` support to `CompositionTreeModel` with full-queue counts and filtered target grouping.
- Added Review/Edit filter bar with labels/counts for `Tất cả`, `Chưa duyệt`, `Ready`, `Include`, `Có warning`, and `Có error`.
- Added explicit empty-state text for no-match filters while keeping filter controls above the tree.
- Preserved selection by `composition_id` when applying/clearing filters and when reloading workspace data.
- Kept UI data access through `WorkspaceService.list_compositions()` and `WorkspaceService.read_composition()`.
- Review fix: `load_workspace()` now restores the current composition after model refresh when it remains visible.

### File List

- `_bmad-output/implementation-artifacts/3-2-add-queue-filters-and-empty-states.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/models/composition_tree_model.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context for Epic 3 Story 3.2.
- 2026-05-25: Implemented Review/Edit queue filters, aggregate counts, empty state, selection restoration, and tests.
- 2026-05-25: Completed internal review and marked story done after quality gates passed.

## Senior Developer Review (AI)

Outcome: Approve

### Findings

- Fixed before completion: `load_workspace()` refreshed the tree but did not restore selection after status/validation refresh. Updated it to preserve the current `composition_id` when still visible.

### Verification

- `pytest` - 84 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.
