# Story 4.4: Surface Issues in Tree, Layer UI, and Warnings Panel

Status: done

<!-- Created from Epic 4 backlog context per project autonomous execution mandate. -->

## Story

As an Operator,
I want issues shown where I can act on them,
so that I can jump from a warning or error to the related target, composition, or layer.

## Acceptance Criteria

1. Given validation issues exist for a composition, when the Review/Edit tree renders, then tree rows show severity icons, issue counts, and status text without relying on color alone, and tooltips expose the issue summary.
2. Given an issue belongs to a layer, when the layer stack renders, then the affected layer row shows a non-color-only issue indicator, and the indicator can expose the Vietnamese message/remediation.
3. Given the Warnings panel is open, when issues are listed, then each issue row shows severity icon, message, scope label, target/composition/layer reference, remediation, and jump action, and row content remains readable at the supported desktop minimum width.
4. Given the Operator activates a jump action from an issue row, when the referenced object exists, then the app navigates to the relevant target/composition/layer and selects or highlights it, and if the object no longer exists, the UI explains that the issue reference is stale.

## Tasks / Subtasks

- [x] Verify tree issue indicators are sufficient (AC: 1)
  - [x] Confirm CompositionTreeModel returns DecorationRole icon, SEVERITY_TEXT, ISSUE_COUNT for target and composition nodes.
  - [x] Write focused unit tests asserting tree model returns non-None DecorationRole and correct ISSUE_COUNT for compositions with ERROR/WARNING summary.

- [x] Add layer issue indicator column to LayerStackModel (AC: 2)
  - [x] Add ISSUE = 6 to LayerStackColumn (shifting ACTIONS to 7); update HEADERS with "Lỗi".
  - [x] Add `set_issues(issues: Iterable[Issue])` to LayerStackModel building a `dict[str, IssueSeverity]` (highest per layer_id).
  - [x] In `data()`, for ISSUE column: DisplayRole returns "✗ ERROR", "⚠ WARN", "ℹ INFO", or "" based on layer severity; ToolTipRole returns Vietnamese message/remediation for that layer.
  - [x] Reset issue map in `set_composition()` (clear on new composition).
  - [x] Write focused tests: layer with ERROR issue shows non-empty display; layer without issue shows ""; tooltip includes message; set_composition clears issues.

- [x] Build WarningsPanelWidget (AC: 3, 4)
  - [x] Create `src/thucthengay/editor/widgets/warnings_panel.py`.
  - [x] `WarningsPanelWidget(QWidget)` contains a `QListWidget` with a header label "Validation Issues".
  - [x] `set_issues(issues, *, composition_id: str = "", target_id: str = "")`: populates QListWidget — one `QListWidgetItem` per issue; item text: "[SEV] message | scope:ref | remediation → điều hướng"; sets item icon via `_standard_icon(severity)`.
  - [x] Store per-item jump data as `QListWidgetItem` user data tuple `(target_id, composition_id, layer_id)`.
  - [x] Expose `jumpRequested = Signal(str, str, str)` — emitted on item double-click with `(target_id, composition_id, layer_id)` from item data.
  - [x] When `issues` is empty: show single item "Không có vấn đề nào." with no icon.
  - [x] Export `WarningsPanelWidget` from `editor/widgets/__init__.py`.
  - [x] Write focused tests (no Qt event loop): `set_issues()` produces correct item count; item text contains severity/message/remediation; empty issues shows placeholder row.

- [x] Wire WarningsPanelWidget into ReviewEditMode and add jump navigation (AC: 3, 4)
  - [x] Replace `self.warnings_summary` (QLabel) with `self.warnings_panel` (WarningsPanelWidget).
  - [x] Update `_build_right_panel()` to add `self.warnings_panel` where `warnings_summary` was.
  - [x] After selection validation: call `self.warnings_panel.set_issues(gate.issues, composition_id=..., target_id=...)` and `self.layer_model.set_issues(gate.issues)`.
  - [x] After include/revalidate actions: same pattern.
  - [x] Replace `_show_review_issues()` to delegate to `warnings_panel.set_issues()` + update `action_summary`.
  - [x] Connect `warnings_panel.jumpRequested` to `_handle_issue_jump(target_id, composition_id, layer_id)`.
  - [x] Implement `_handle_issue_jump`: if `composition_id` given and visible in tree → `tree_view.setCurrentIndex(...)` to navigate; if `layer_id` given → select the matching row in `layer_table`; if reference is stale (not found) → set `action_summary` with explanatory text "Tham chiếu không còn tồn tại.".
  - [x] Update any reference to `warnings_summary` in other parts of `review_edit_mode.py` to use `warnings_panel.set_issues()` or clear.

- [x] Add focused integration tests (AC: 1-4)
  - [x] Test: after mock gate with issues, warnings_panel item count matches issue count.
  - [x] Test: jump signal from warnings_panel causes tree model index lookup to be called.
  - [x] Test: stale composition_id jump sets explanatory action_summary text.
  - [x] Run full pytest + ruff check + smoke test.

### Review Findings

- [x] [Review][Patch] Mojibake-corrupted Vietnamese UI strings in Review/Edit mode [src/thucthengay/editor/modes/review_edit_mode.py:94]
- [x] [Review][Patch] Suppressed selection refresh still runs validation gate [src/thucthengay/editor/modes/review_edit_mode.py:397]
- [x] [Review][Patch] Failed validation summary is saved without refreshing tree/filter projection [src/thucthengay/editor/modes/review_edit_mode.py:443]
- [x] [Review][Patch] Blocking Include/Validate message is overwritten by ready-state text [src/thucthengay/editor/modes/review_edit_mode.py:450]
- [x] [Review][Patch] Invalid fallback map_frame metadata can crash validation instead of becoming an issue [src/thucthengay/editor/modes/review_edit_mode.py:541]
- [x] [Review][Patch] Issue jump treats filtered-out compositions as stale references [src/thucthengay/editor/modes/review_edit_mode.py:580]
- [x] [Review][Patch] Missing or stale layer references are not explained during issue jump [src/thucthengay/editor/modes/review_edit_mode.py:592]
- [x] [Review][Patch] Warning rows do not show an explicit visible jump action label [src/thucthengay/editor/widgets/warnings_panel.py:76]

## Dev Notes

- Follow `_bmad-output/project-context.md` before all implementation.
- Owner modules:
  - `editor/models/layer_stack_model.py`: add ISSUE column and `set_issues()`.
  - `editor/widgets/warnings_panel.py`: new WarningsPanelWidget (NEW FILE).
  - `editor/widgets/__init__.py`: export WarningsPanelWidget.
  - `editor/modes/review_edit_mode.py`: wire warnings_panel and jump handler; replace warnings_summary QLabel.
- Scope guard:
  - Do NOT implement metadata editor; Story 4.5 owns correction UI.
  - Do NOT add new workspace JSON fields; all issue data is session/derived state only.
  - Do NOT change Issue model, ValidationResult, or composition_rules; Story 4.4 only adds UI surfacing.
  - Tree model (CompositionTreeModel) already returns severity icons and issue counts — confirm only, no new logic needed there.
- `LayerStackColumn` enum change shifts ACTIONS from 6 to 7; update `_persist_layer_visibility` column check in review_edit_mode accordingly.
- `WarningsPanelWidget` must NOT import workspace or validation modules directly; receive `Issue` objects from the caller.
- Tests must not use Qt event loop (no `QApplication`, use model/widget in headless mode or mock the signals).
- After each implementation batch: run `pytest`, `ruff check .`, and `python -m thucthengay --smoke`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.4]
- [Source: _bmad-output/implementation-artifacts/4-3-run-validation-on-select-include-and-export-preflight.md]
- [Source: src/thucthengay/editor/models/composition_tree_model.py]
- [Source: src/thucthengay/editor/models/layer_stack_model.py]
- [Source: src/thucthengay/editor/modes/review_edit_mode.py]
- [Source: src/thucthengay/models/issue.py]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest` — 145 passed.
- `conda run -n ttn-env ruff check .` — All checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` — App ready.

### Completion Notes List

- Added `ISSUE` column (index 6) to `LayerStackModel`; ACTIONS shifted to 7. `set_issues()` computes highest severity per layer from validation issues; `set_composition()` clears issue state.
- Created `WarningsPanelWidget` with `QListWidget`: severity icon, structured text per issue, `jumpRequested` signal on double-click.
- Exported `WarningsPanelWidget` from `editor/widgets/__init__.py`.
- Replaced `warnings_summary` QLabel in `ReviewEditMode` with `warnings_panel`; all workspace errors routed to `action_summary`; validation issues routed to `warnings_panel.set_issues()` + `layer_model.set_issues()`.
- Added `_handle_issue_jump()` and `_select_layer_by_id()` for navigation from Warnings panel.
- Tree model indicators (DecorationRole + ISSUE_COUNT + SEVERITY_TEXT) already complete from prior stories — confirmed with 5 focused tests.
- 22 new tests in `test_warnings_panel_and_issue_ui.py`; updated 3 existing tests in `test_review_edit_mode.py`.
- Code review fixes applied: restored corrupted Vietnamese UI text, avoided validation during suppressed refresh, refreshed tree/filter state after failed validation, preserved blocking action text, caught invalid fallback `map_frame`, handled filtered/stale target/composition/layer issue jumps, and added visible "điều hướng" labels.
- Verification after review fixes: full pytest 197 passed; full ruff passed; smoke app ready.

### File List

- `_bmad-output/implementation-artifacts/4-4-surface-issues-in-tree-layer-ui-and-warnings-panel.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/models/layer_stack_model.py`
- `src/thucthengay/editor/widgets/warnings_panel.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_warnings_panel_and_issue_ui.py`
- `tests/unit/test_review_edit_mode.py`
- `src/thucthengay/editor/models/composition_tree_model.py`

## Change Log

- 2026-05-25: Created story context from Epic 4 backlog and started implementation.
- 2026-05-25: Implemented all ACs — layer issue column, WarningsPanelWidget, jump navigation, 22 new tests. All gates pass.
- 2026-05-25: Code review found 8 patch findings; all fixed and verified. Story marked done.
