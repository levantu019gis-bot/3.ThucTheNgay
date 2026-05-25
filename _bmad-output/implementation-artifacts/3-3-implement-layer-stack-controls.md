# Story 3.3: Implement Layer Stack Controls

Status: done

## Story

As an Operator,
I want to control layer visibility and order for a composition,
so that the selected image stack reflects what should appear on the report slide.

## Acceptance Criteria

1. Given a composition has one or more layers, when the layer stack is displayed, then each layer row shows visibility control, order control, timestamp, cloud percent, metadata status, short filename, action menu, and full filename/path tooltip, and long filenames are elided without changing row height.
2. Given the Operator toggles layer visibility, when the change is saved, then the composition layer visibility is persisted through `WorkspaceService`, and the composition is marked `needs_revalidation=true`.
3. Given the Operator changes layer order, when the change is saved, then the new order is persisted in the composition JSON, and subsequent preview/render operations use the persisted layer order.
4. Given no layer remains visible, when validation is triggered for the composition, then validation produces a blocking error, and the layer stack and tree expose the issue in a non-color-only way.

## Tasks / Subtasks

- [x] Add workspace service APIs for layer edits (AC: 2, 3)
  - [x] Persist layer visibility changes by composition/layer id.
  - [x] Persist layer order changes with normalized `order` values.
  - [x] Mark the composition `needs_revalidation=true` and clear ready/include/review_order after layer edits.
  - [x] Raise `WorkspaceError` for missing layer ids without partially writing state.
- [x] Add a layer stack Qt model for Review/Edit (AC: 1, 3, 4)
  - [x] Show stable columns for visibility, order, timestamp, cloud percent, metadata status, short filename, and action menu.
  - [x] Provide full source/cache path tooltip and elide display text for long filenames.
  - [x] Expose custom roles for layer id, full path, visible state, and no-visible warning state.
  - [x] Keep row height stable through fixed/default table sizing.
- [x] Wire layer stack controls into `ReviewEditMode` (AC: 1-4)
  - [x] Replace the Story 3.1 placeholder layer summary with a table and order controls.
  - [x] Load layers whenever tree selection changes through `WorkspaceService.read_composition()`.
  - [x] Save visibility changes through `WorkspaceService`.
  - [x] Save move up/down order changes through `WorkspaceService` and refresh selected composition/tree state.
  - [x] Show a non-color-only warning when no visible layers remain, without implementing full Epic 4 validation.
- [x] Add focused tests (AC: 1-4)
  - [x] Test service visibility persistence and stale-state reset.
  - [x] Test service layer order persistence and normalized order values.
  - [x] Test layer stack model display roles, check state, tooltip, and no-visible warning.
  - [x] Test Review/Edit UI saves visibility/order through the service and exposes the no-visible warning.

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `workspace/`: source of truth for persisted composition JSON; layer edit methods belong here.
  - `models/`: shared persisted `ImageLayer`/`Composition` contracts already exist; do not duplicate persisted schemas for UI.
  - `editor/models/`: Qt model projection for layer stack rows only.
  - `editor/modes/`: Review/Edit widget wiring and service calls only; no raw JSON reads/writes.
- Build on Story 3.1 and 3.2:
  - `ReviewEditMode` already loads selected composition via `WorkspaceService.read_composition()`.
  - `CompositionTreeModel` already shows stale state as text/icon (`Cần kiểm tra lại` / `STALE`).
  - `load_workspace()` already refreshes tree counts and restores selection when visible.
- Existing layer fields available:
  - `layer_id`, `source_path`, `cache_path`, `visible`, `order`
  - `capture_date`, `capture_time`, `cloud_percent`
  - `metadata_status`, `metadata_source`
- Layer order rule:
  - Display and render-facing code should consume layers sorted by persisted `order`.
  - When order changes, normalize `order` values to `0..n-1` and persist through `WorkspaceService`.
- Visibility edit rule:
  - Any layer visibility/order edit must mark the composition stale: `needs_revalidation=true`, `ready=false`, `include=false`, `review_order=None`.
  - Preserve existing `validation_summary`; stale state is inferred from `needs_revalidation`.
- Validation dependency:
  - Full validation engine and blocking issue objects arrive in Epic 4.
  - For this story, surface the no-visible-layer condition in the layer stack and tree using text/tooltips/filterable error state; do not implement the full validator.
- UX requirements:
  - Layer row anatomy includes visibility control, order control, timestamp, cloud percent, metadata status, filename, action menu, tooltip with full path.
  - Long filenames must be elided/truncated without row-height changes.
  - Status must not rely only on color.
- Keep scope tight: do not implement GIS canvas pan/zoom, grid overrides, slide preview rendering, metadata editor, warnings panel jump links, or review action transitions in this story.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.3]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-10]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UJ-2]
- [Source: _bmad-output/planning-artifacts/architecture.md#Review/Edit UI]
- [Source: _bmad-output/implementation-artifacts/3-2-add-queue-filters-and-empty-states.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `pytest tests/unit/test_workspace_service.py tests/unit/test_review_edit_mode.py` - 29 passed.
- `pytest` - 90 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.

### Completion Notes List

- Added `WorkspaceService.set_layer_visibility()` and `WorkspaceService.reorder_layers()` so layer edits persist through the workspace source of truth.
- Layer visibility/order edits now mark compositions stale and clear ready/include/review_order while preserving the existing validation summary.
- Added `LayerStackModel` with checkbox visibility, normalized order display, timestamp, cloud percent, metadata status, elided filename, action menu text, and full path tooltip roles.
- Replaced the Review/Edit layer placeholder with a `QTableView` layer stack and move up/down controls.
- Added non-color-only no-visible-layer handling in the layer stack and composition tree, including tree status/severity/count/filter updates.
- Kept full validation issue generation deferred to Epic 4.

### File List

- `_bmad-output/implementation-artifacts/3-3-implement-layer-stack-controls.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/workspace/service.py`
- `src/thucthengay/editor/models/composition_tree_model.py`
- `src/thucthengay/editor/models/layer_stack_model.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_workspace_service.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context for Epic 3 Story 3.3 and started implementation.
- 2026-05-25: Implemented layer stack model/UI, workspace layer edit APIs, no-visible-layer tree warning, and tests.
- 2026-05-25: Completed internal review and marked story done after quality gates passed.

## Senior Developer Review (AI)

Outcome: Approve

### Findings

- Fixed before completion: tree rows initially only reflected generic stale state after all layers were hidden. Added explicit non-color-only `Không có layer bật` status, `ERROR` severity, issue count, tooltip note, and `Có error` filter matching while leaving full validation engine work for Epic 4.

### Verification

- `pytest` - 90 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.
