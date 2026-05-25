# Story 3.5: Implement Per-Composition Grid Override Controls

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an Operator,
I want to override grid interval per composition,
so that grid labels fit the selected map view without changing target defaults.

## Acceptance Criteria

1. Given a selected composition has no grid override, when grid controls are shown, then they display target config defaults, and the label format defaults to `dms_full` unless configured otherwise.
2. Given the Operator edits DMS interval fields, when the override is saved, then the override is persisted only in the composition JSON, and target config defaults remain unchanged.
3. Given a grid override is invalid or outside allowed limits, when the Operator attempts to save or validate, then the UI shows a validation message in Vietnamese, and invalid values do not silently change render output.
4. Given grid settings change, when the composition state is saved, then the preview is marked stale or updated through debounce, and the composition is marked `needs_revalidation=true`.

## Tasks / Subtasks

- [x] Add workspace service API for grid overrides (AC: 2, 4)
  - [x] Persist `Composition.grid_override` by composition id through `WorkspaceService`.
  - [x] Validate override through existing `GridConfig` / `GridInterval` Pydantic models.
  - [x] Mark the composition `needs_revalidation=true` and clear `ready/include/review_order` after grid edits.
  - [x] Preserve layers, view, validation summary, and target config data.
- [x] Add grid override controls to Review/Edit mode (AC: 1-4)
  - [x] Add DMS fields for degrees, minutes, seconds and a label format field/display near the editor controls.
  - [x] Display target grid defaults when the selected composition has no override.
  - [x] Display persisted composition override values when present.
  - [x] Save valid edits through `WorkspaceService` only; do not mutate raw JSON or target config.
  - [x] Show short Vietnamese validation errors and keep prior render-affecting state unchanged on invalid input.
  - [x] Ensure text input arrow keys are protected from review shortcuts by using normal Qt input widgets.
- [x] Wire stale preview and selection refresh behavior (AC: 4)
  - [x] After successful grid save, refresh selected composition, tree/filter projection, GIS/preview stale indicators, and warning summary.
  - [x] Keep scope tight: do not implement Story 3.6 slide preview debounce/rendering or Epic 5 grid drawing.
- [x] Add focused tests (AC: 1-4)
  - [x] Test service grid override persistence, stale-state reset, and target default preservation.
  - [x] Test invalid grid override values do not partially write state.
  - [x] Test Review/Edit shows target defaults, saves valid DMS override, marks preview stale, and shows Vietnamese validation feedback for invalid input.

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `models/`: `GridInterval` and `GridConfig` already define persisted grid shape; extend only if validation semantics are genuinely missing.
  - `workspace/`: source of truth for composition JSON; grid override write APIs belong here.
  - `editor/modes/`: Review/Edit control wiring and service calls only; no raw JSON reads/writes.
  - `render/` and `gis/`: no final grid drawing in this story; Epic 5 consumes the persisted state later.
- Build on Stories 3.1-3.4:
  - `ReviewEditMode` already loads selected composition through `WorkspaceService.read_composition()`.
  - Layer and view edits already mark composition stale, clear `ready/include/review_order`, refresh tree/filter state, and show `Preview cần cập nhật`.
  - Reuse that stale-state pattern for grid edits.
- Grid behavior:
  - Target config default lives at `TargetConfig.grid`.
  - Composition override lives at `Composition.grid_override`.
  - Effective grid for UI display is `composition.grid_override` when present, otherwise target `grid`; if no target is available, fall back only to the selected composition override and show a clear unavailable/default state.
  - Label format comes from the effective grid and defaults to `dms_full`.
  - DMS interval fields must be degrees/minutes/seconds. Existing model bounds: degrees `>=0`, minutes `0..59`, seconds `>=0` and `<60`, and total interval must be greater than zero.
- Invalid input:
  - Do not write any composition change on invalid DMS values.
  - UI message must be in Vietnamese and specific enough to fix, e.g. "Khoảng grid phải lớn hơn 0" or "Phút/giây phải nhỏ hơn 60".
  - Do not silently coerce an invalid value into a valid render-affecting value.
- UX requirements:
  - Review/Edit remains dense and desktop-first; use stable panel dimensions and normal input widgets.
  - The controls should behave like an inspector section, not a modal-heavy workflow.
  - Status must not rely only on color.
- Keep scope tight: do not implement slide preview renderer/debounce, grid line drawing, final render math, metadata editor, validation engine, or review action transitions here.

### Project Structure Notes

- Likely update files:
  - `src/thucthengay/workspace/service.py`
  - `src/thucthengay/editor/modes/review_edit_mode.py`
  - `tests/unit/test_workspace_service.py`
  - `tests/unit/test_review_edit_mode.py`
- Only add a dedicated widget/module if the Review/Edit grid control code becomes materially large; otherwise keep the story narrow.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.5]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-12 Configure grid override per composition]
- [Source: _bmad-output/planning-artifacts/architecture.md#GIS / Spatial Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#State Management Patterns]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Grid interval]
- [Source: _bmad-output/implementation-artifacts/3-4-implement-gis-editor-canvas-view-controls.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `pytest tests/unit/test_workspace_service.py tests/unit/test_review_edit_mode.py` - 37 passed.
- `pytest` - 98 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Added `WorkspaceService.update_grid_override()` so per-composition DMS grid interval edits persist only in composition JSON.
- Grid override edits validate through existing `GridConfig` / `GridInterval`, mark compositions stale, and clear ready/include/review_order while preserving layers, view, and validation summary.
- Added Review/Edit grid controls for degrees/minutes/seconds and label format, showing target defaults when no override exists and persisted override values when present.
- Grid saves preserve the effective grid style so editing interval/label does not silently drop target/override styling metadata.
- Invalid grid inputs show Vietnamese validation feedback and do not write partial state.
- Successful grid saves refresh selected composition, tree/filter state, stale preview text, and warnings summary.

### File List

- `_bmad-output/implementation-artifacts/3-5-implement-per-composition-grid-override-controls.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/workspace/service.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_workspace_service.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context for Epic 3 Story 3.5.
- 2026-05-25: Started implementation.
- 2026-05-25: Implemented grid override persistence, Review/Edit controls, and focused tests; marked ready for review.
- 2026-05-25: Completed internal review, fixed style-preservation issue, and marked story done.

## Senior Developer Review (AI)

Outcome: Approve

### Findings

- Fixed before completion: grid override saves initially rebuilt `GridConfig` from interval/label only, which could drop existing target/override `style` metadata. Updated service/UI flow to preserve effective grid style and added assertions in service/UI tests.

### Verification

- `pytest` - 98 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay --smoke` - app ready.
- `git diff --check` - clean.
