# Story 1.6: Persist Composition Status and Review State

Status: done

## Story

As an Operator,
I want review status and keyboard decisions to persist per composition,
So that I can resume the review workflow without losing decisions.

## Requirement References

- FR7
- AR4
- UX-DR10
- UX-DR15
- NFR7

## Acceptance Criteria

1. Given a composition JSON exists in the workspace, when the Operator changes notes or status through the app, then `reviewed`, `ready`, `include`, `review_order`, and `notes` are persisted through `WorkspaceService`, and reloading the workspace restores the same values.
2. Given the Operator uses the right-arrow include action after a caller has supplied a passing validation gate result, when the status transition is applied, then the composition is marked reviewed and ready according to the PRD transition rules, `include`/`review_order` are updated consistently with the include action, and this story persists the transition only; full validation rule evaluation is implemented in Epic 4.
3. Given the Operator uses the up-arrow skip action, when the skip transition is applied, then the composition is marked reviewed but not included, and the app advances according to the review queue behavior.
4. Given the Operator uses the left-arrow previous action, when a previous composition exists, then the app navigates back without corrupting the current composition status, and no text input field consumes review shortcuts while focused for text editing.

## Implementation Context

- Story 1.5 introduced `WorkspaceService` as the only owner of `manifest.json` and `compositions/*.json`.
- `Composition` already contains `reviewed`, `ready`, `include`, `review_order`, and `notes`.
- PRD transition rules:
  - Right arrow: after full validation pass, set `reviewed=true`, `ready=true`, `include=true`, assign `review_order`, then advance.
  - Up arrow: set `reviewed=true`, `ready=false`, `include=false`, clear `review_order`, then advance.
  - Left arrow: navigate previous; if reset of a ready composition is needed later, confirmation belongs to Review/Edit UI stories.
- This story must not implement full validation rules; it should require a caller-provided passing gate for include.
- Keyboard shortcut handling must avoid firing review shortcuts when focus is inside text-editing widgets.

## Tasks

- [x] Add review state update contract in `WorkspaceService`.
- [x] Add include/skip transitions that persist through composition JSON.
- [x] Add queue helpers for next/previous review navigation without mutating current state.
- [x] Add shortcut focus guard for text-editing widgets.
- [x] Add unit tests for persistence, include, skip, previous, and shortcut focus behavior.
- [x] Run quality gates.

## Dev Agent Record

### Debug Log

- 2026-05-25: Confirmed Story 1.6 is the next backlog item after Story 1.5.
- 2026-05-25: Reviewed PRD/UX transition rules and workspace service boundary.
- 2026-05-25: Implemented review state persistence, include/skip transitions, queue navigation helpers, and shortcut focus guard.
- 2026-05-25: Ran `pytest`, `ruff check .`, and `python -m thucthengay --smoke`; all passed.

### Completion Notes

- `WorkspaceService.update_review_state()` persists `reviewed`, `ready`, `include`, `review_order`, and `notes`.
- `WorkspaceService.apply_include_transition()` requires a caller-supplied passing validation gate and assigns deterministic `review_order`.
- `WorkspaceService.apply_skip_transition()` marks reviewed while clearing ready/include/review order.
- Previous/next queue helpers navigate by manifest composition order without mutating the current composition.
- `review_shortcuts_enabled_for_focus()` prevents review shortcuts from firing while text-editing widgets have focus.

### File List

- `_bmad-output/implementation-artifacts/1-6-persist-composition-status-and-review-state.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/shortcuts.py`
- `src/thucthengay/workspace/service.py`
- `tests/unit/test_review_shortcuts.py`
- `tests/unit/test_workspace_service.py`

### Change Log

- 2026-05-25: Added story context and started implementation.
- 2026-05-25: Completed review state persistence and transition tests.
