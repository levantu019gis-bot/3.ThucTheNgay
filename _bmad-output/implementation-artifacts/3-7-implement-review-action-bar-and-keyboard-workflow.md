# Story 3.7: Implement Review Action Bar and Keyboard Workflow

Status: done

<!-- Note: Created from Epic 3 backlog context and started immediately per project autonomous execution mandate. -->

## Story

As an Operator,
I want review actions and keyboard shortcuts for include, skip, and previous,
so that I can process many compositions efficiently without losing validation safety.

## Acceptance Criteria

1. Given a composition is selected, when the Review Action Bar is shown, then it provides Previous, Skip, Include/Validate, and Revalidate actions where applicable, and there is only one primary action for the current review context.
2. Given the Operator presses Right or clicks Include/Validate, when the validation service contract returns a passing gate result, then the app applies the include/ready transition through workspace services and advances according to the review queue behavior.
3. Given the Operator presses Right or clicks Include/Validate, when the validation service contract returns blocking issues, then the app does not mark the composition ready or included, keeps the composition selected, exposes the returned blocking issues, and wires the UI to the validation contract while Epic 4 implements full validation rules.
4. Given the Operator presses Up or clicks Skip, when the skip action is valid, then the app marks the composition reviewed but not included and persists the transition through `WorkspaceService`.
5. Given the Operator presses Left or clicks Previous, when a previous composition exists, then the app navigates back without changing include/ready status unless an explicit action is taken, and keyboard shortcuts do not fire while a text input needs arrow keys for editing.

## Tasks / Subtasks

- [x] Add Review Action Bar controls and action state model (AC: 1)
  - [x] Replace disabled placeholder buttons with persistent Previous, Skip, Include/Validate, and Revalidate buttons.
  - [x] Make Include/Validate the only primary action when a selectable composition is loaded.
  - [x] Show Vietnamese action/status feedback and disabled-state tooltips without relying on color alone.
- [x] Wire review transitions through `WorkspaceService` (AC: 2, 3, 4, 5)
  - [x] Include/Validate uses a validation gate contract and calls `apply_include_transition()` only on pass.
  - [x] Blocking gate results leave the current selection unchanged and surface issues in the warnings panel.
  - [x] Skip calls `apply_skip_transition()` and advances to the next composition when available.
  - [x] Previous navigates through `previous_composition_id()` without mutating review state.
  - [x] Revalidate reruns the current lightweight gate and refreshes visible status without promoting state.
- [x] Add keyboard workflow and text-input guards (AC: 2-5)
  - [x] Right Arrow mirrors Include/Validate.
  - [x] Up Arrow mirrors Skip.
  - [x] Left Arrow mirrors Previous.
  - [x] Shortcuts must not fire while focus is inside editable text fields used by grid controls.
- [x] Add focused tests (AC: 1-5)
  - [x] Test action bar enabled/disabled state and single primary action.
  - [x] Test include pass, include blocked, skip, and previous behavior.
  - [x] Test keyboard shortcuts and text-input guard.

### Review Findings

- [x] [Review][Patch] Allow Revalidate to clear stale persisted error summaries when the current lightweight gate passes [`src/thucthengay/editor/modes/review_edit_mode.py:513`]

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `editor/modes/review_edit_mode.py`: Review Action Bar UI, keyboard handling, validation contract wiring, and workspace transition calls.
  - `workspace/service.py`: already owns persisted review transitions; do not bypass it or edit composition JSON directly.
  - `validation/`: Epic 4 owns full validation rules; this story may add a minimal contract/helper only if needed, but must not implement Epic 4 validation engine.
- Existing services/patterns:
  - `WorkspaceService.apply_include_transition(composition_id, validation_passed=True)` persists right-arrow include state and assigns `review_order`.
  - `WorkspaceService.apply_skip_transition(composition_id)` persists up-arrow skip state and clears include/review order.
  - `WorkspaceService.next_composition_id()` and `previous_composition_id()` provide queue navigation without direct model mutation.
  - After any transition, refresh tree/filter counts and restore selection through existing `ReviewEditMode._refresh_workspace_projection()`.
- Validation contract scope for this story:
  - Use a lightweight gate object/result that can be replaced by Epic 4.
  - Passing gate must be explicit before include transition.
  - Blocking gate result should produce Vietnamese issue/remediation text in the warnings panel and must not persist ready/include.
  - Do not implement the full Issue engine, metadata correction, or export preflight rules here.
- Keyboard/accessibility:
  - Buttons must be visible and keyboard actions mirrored.
  - `Right`, `Up`, and `Left` shortcuts must be ignored when focus is in `QLineEdit` grid inputs so arrow-key text editing is preserved.
  - Keep focus order compatible with UX: tree -> layer panel -> GIS editor -> review actions -> warnings.
- Previous story learnings from 3.6:
  - Keep state changes deterministic and testable without a long-running Qt event loop.
  - Use workspace/model source of truth, then refresh UI projections.
  - Add explicit tests for stale/blocked branches, not only happy paths.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.7]
- [Source: _bmad-output/planning-artifacts/architecture.md#Review status transitions]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Review Action Bar]
- [Source: _bmad-output/implementation-artifacts/3-6-implement-slide-preview-panel-with-debounced-updates.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests/unit/test_review_edit_mode.py` - 21 passed.
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - all checks passed.
- `conda run -n ttn-env pytest` - 106 passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.
- `git diff --check` - clean, LF/CRLF warnings only.

### Completion Notes List

- Replaced placeholder Review Action Bar with visible Previous, Skip, Include/Validate, and Revalidate buttons.
- Added a lightweight `ReviewGateResult` contract in Review/Edit mode so Include/Validate only persists include state after an explicit passing gate.
- Blocking gate results keep selection unchanged and surface Vietnamese remediation text in the warnings panel.
- Skip and Include transitions use `WorkspaceService` and advance to the next composition when available.
- Previous navigation uses `WorkspaceService.previous_composition_id()` and does not mutate review state.
- Right/Up/Left keyboard actions mirror the buttons, with a QLineEdit focus guard for grid editing fields.
- Code review finding resolved: stale persisted error summaries can now be cleared by Revalidate when the current lightweight gate passes.

### File List

- `_bmad-output/implementation-artifacts/3-7-implement-review-action-bar-and-keyboard-workflow.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context and started implementation.
- 2026-05-25: Implemented Review Action Bar, keyboard workflow, validation gate wiring, and focused tests; marked ready for review.
- 2026-05-25: Resolved code review finding, reran quality gates, and marked story done.
