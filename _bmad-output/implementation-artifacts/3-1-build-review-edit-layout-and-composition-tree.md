# Story 3.1: Build Review/Edit Layout and Composition Tree

Status: done

## Story

As an Operator,
I want a Review/Edit workstation with a target-composition tree,
so that I can navigate review work by target and date with clear status context.

## Acceptance Criteria

1. Given the workspace contains target-date compositions, when the Operator enters Review/Edit mode, then the UI shows a desktop splitter layout with composition tree, layer/editor workspace, preview, actions, and warnings areas, and splitter min/max sizes keep content usable at 1280x720 and recommended 1440x900+ layouts.
2. Given compositions are loaded from the workspace, when the tree is populated, then targets can expand to show composition rows ordered by configured target order and composition date/review order as applicable, and each row shows label/date/time, status badge, severity icon, issue count, selected state, and tooltip with issue summary where available.
3. Given a composition row is selected, when selection changes, then the app loads the composition through `WorkspaceService`, and detail panels update without UI code reading raw JSON directly.
4. Given status or issue severity is displayed, when the Operator views the row, then status is conveyed through text/icon as well as color, and row height remains stable when indicators change.

## Tasks / Subtasks

- [x] Create Review/Edit layout shell (AC: 1)
  - [x] Add `ReviewEditMode` under `src/thucthengay/editor/modes/`.
  - [x] Use `QSplitter`/Qt widgets for composition tree, layer/editor placeholder, slide preview placeholder, review actions, and warnings areas.
  - [x] Set stable minimum sizes and uniform tree row height suitable for 1280x720+.
- [x] Implement composition tree projection model (AC: 2, 4)
  - [x] Add `CompositionTreeModel` under `src/thucthengay/editor/models/`.
  - [x] Group by target and order groups by enabled target `sort_order` when target config is available.
  - [x] Order composition rows by `review_order` first where set, then `capture_date`, then `composition_id`.
  - [x] Expose visible text, status, severity, issue counts, stable icon/text indicators, and tooltips from `Composition` fields.
- [x] Wire selection through workspace service (AC: 3)
  - [x] Add a load method that accepts `WorkspaceService` and optional `TargetConfig` list.
  - [x] On composition selection, call `WorkspaceService.read_composition()` and update detail placeholders from the loaded model.
  - [x] Do not read raw JSON from UI code.
- [x] Integrate Review/Edit mode into the app shell (AC: 1)
  - [x] Make Review/Edit reachable from `AppShell` without removing Setup mode.
  - [x] Keep disabled/export future modes out of scope unless needed for navigation.
- [x] Add focused tests (AC: 1-4)
  - [x] Test target grouping/order and composition ordering.
  - [x] Test display status/severity/tooltip values are text/icon based.
  - [x] Test selection loads via `WorkspaceService` and updates detail panels.
  - [x] Test app shell exposes Review/Edit mode.

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `editor/modes/`: PySide6 mode widgets only.
  - `editor/models/`: Qt view models only.
  - `workspace/`: source of truth for manifest/composition JSON.
  - `models/`: shared Pydantic contracts.
- Do not put business logic or JSON file reading into UI classes; call `WorkspaceService`.
- Existing composition state available for display: `reviewed`, `ready`, `include`, `needs_revalidation`, `review_order`, `validation_summary`, `persisted_validation_state`, `layers`, `capture_date`.
- Existing config state available for target order/labels: `TargetConfig.id`, `sort_order`, `name`, `alias`.
- Use domain names exactly: `Target`, `Composition`, `ImageLayer`, `Workspace`, `Issue`.
- Review/Edit layout from UX: top mode area, left composition/layers/preview area, right GIS editor area, bottom or docked warnings panel, keyboard review actions visible.
- Story 3.1 should create placeholders for future layer stack, GIS editor, preview rendering, warnings, and review action behavior; do not implement story 3.2+ filters, story 3.3 layer controls, story 3.4 GIS canvas, or story 3.7 keyboard transitions yet.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.1]
- [Source: _bmad-output/planning-artifacts/architecture.md#Editor Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Review status transitions]
- [Source: _bmad-output/planning-artifacts/architecture.md#FR-9 to FR-14 Review/Edit]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Review/Edit layout]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Composition Tree Item]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `pytest tests/unit/test_review_edit_mode.py` - 4 passed.
- `pytest` - 81 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.

### Completion Notes List

- Added Review/Edit tab in `AppShell` while preserving Setup mode.
- Added `ReviewEditMode` splitter layout with composition tree, placeholder panels for future Epic 3 stories, visible review action area, and warnings panel.
- Added `CompositionTreeModel` that groups workspace `Composition` objects by target, orders by target config and review/date order, and exposes text/icon/status/severity/tooltip data without reading raw JSON.
- Selection in Review/Edit reloads the selected composition via `WorkspaceService.read_composition()` and updates detail panels.
- Review fix: target rows now show issue counts directly and composition rows include the `composition_id` label before date/time.

### File List

- `_bmad-output/implementation-artifacts/3-1-build-review-edit-layout-and-composition-tree.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/app_shell.py`
- `src/thucthengay/editor/models/composition_tree_model.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context for Epic 3 Story 3.1.
- 2026-05-25: Implemented Review/Edit layout, composition tree model, workspace-service-backed selection, AppShell integration, and tests.
- 2026-05-25: Completed internal review follow-up for visible tree row issue counts and composition labels; marked story done after quality gates passed.

## Senior Developer Review (AI)

Outcome: Approve

### Findings

- Fixed before completion: target tree rows showed aggregate issue counts only in tooltip, not visible row text. Updated `CompositionTreeModel` and tests so target rows visibly include issue counts.
- Fixed before completion: composition rows showed date/time/status but not an explicit composition label. Updated row display to include `composition_id`.

### Verification

- `pytest` - 81 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.
