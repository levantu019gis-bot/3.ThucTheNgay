# Story 3.6: Implement Slide Preview Panel with Debounced Updates

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an Operator,
I want a slide preview that tracks my composition changes,
so that I can trust what will be exported while editing.

## Acceptance Criteria

1. Given a composition is selected, when the preview panel loads, then it shows the current composition preview state with clear loading, stale/needs_update, rendered, and render_error display states.
2. Given view, layer, grid, or metadata-affecting state changes, when the composition state is saved, then preview updates are debounced to avoid excessive rendering and stale preview state is shown until the latest render completes.
3. Given a preview render completes for the current composition state, when the preview panel updates, then the preview reflects center/scale, layer order, grid, and background close to final export expectations.
4. Given preview rendering fails, when the preview panel receives the failure, then it shows a render_error state with actionable Vietnamese text and the Operator can continue editing and trigger a later preview.

## Tasks / Subtasks

- [x] Add Slide Preview widget and state model (AC: 1, 3, 4)
  - [x] Implement a Qt widget with loading, stale/needs_update, rendered, empty/no-layer, and render_error states.
  - [x] Build preview display from composition source of truth: view center/scale, visible layer order, effective grid, and target background/style metadata when available.
  - [x] Keep implementation inside `editor/widgets`; do not implement Epic 5 final render or raster read-window math.
- [x] Wire debounced preview updates into Review/Edit mode (AC: 1, 2)
  - [x] Replace placeholder preview label with the new widget.
  - [x] On selection, load selected composition and schedule preview update.
  - [x] After layer visibility/order, view, or grid edits, show stale state immediately and debounce render update.
  - [x] Ignore stale completion for older preview requests.
- [x] Add focused tests (AC: 1-4)
  - [x] Test preview widget state transitions and stale token guard.
  - [x] Test Review/Edit schedules debounced preview refresh after selection and after layer/view/grid edits.
  - [x] Test render_error can be shown and later cleared by a successful preview update.

### Review Findings

- [x] [Review][Patch] Accept `map_background` string metadata as preview background [`src/thucthengay/editor/modes/review_edit_mode.py:511`]
- [x] [Review][Patch] Prevent stale preview success from overwriting a render error [`src/thucthengay/editor/widgets/slide_preview.py:141`]
- [x] [Review][Patch] Clamp negative debounce intervals to deterministic timer behavior [`src/thucthengay/editor/widgets/slide_preview.py:45`]
- [x] [Review][Patch] Normalize background metadata before adding it to the preview request signature [`src/thucthengay/editor/widgets/slide_preview.py:187`]
- [x] [Review][Patch] Read view rotation from composition state instead of hardcoding preview text [`src/thucthengay/editor/widgets/slide_preview.py:207`]

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `editor/widgets/`: Slide preview UI state and deterministic preview projection belong here.
  - `editor/modes/review_edit_mode.py`: wiring only; no raw JSON reads/writes.
  - `render/` and `gis/`: do not add final rendering, raster IO, CRS/read-window math, or grid drawing in this story.
- Build on Stories 3.1-3.5:
  - `ReviewEditMode` already selects compositions through `WorkspaceService.read_composition()`.
  - Layer, view, and grid edits already mark compositions stale and refresh tree/detail panels.
  - `GisCanvasWidget` already uses generation tokens to reject stale render results; mirror that pattern for preview.
- Preview scope for this story:
  - The MVP preview can be a deterministic Qt-drawn/label-based preview projection instead of actual GeoTIFF rendering.
  - It must expose the state the final renderer will later consume: composition id, center, scale, visible layer order, effective grid interval/label format, and background/style metadata.
  - It must show Vietnamese status/remediation text and must not rely on color alone.
- Keep scope tight: do not implement Story 3.7 review action bar, Epic 4 validation engine, Epic 5 shared render specification, two-stage render jobs, final PNG rendering, or raster/grid drawing.

### Project Structure Notes

- Likely update files:
  - `src/thucthengay/editor/widgets/slide_preview.py`
  - `src/thucthengay/editor/widgets/__init__.py`
  - `src/thucthengay/editor/modes/review_edit_mode.py`
  - `tests/unit/test_review_edit_mode.py`

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.6]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-13 Show slide preview]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Slide Preview Panel]
- [Source: _bmad-output/planning-artifacts/architecture.md#Rendering Architecture]
- [Source: _bmad-output/implementation-artifacts/3-5-implement-per-composition-grid-override-controls.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests/unit/test_review_edit_mode.py` - 17 passed.
- `conda run -n ttn-env pytest` - 102 passed.
- `conda run -n ttn-env ruff check .` - all checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.

### Completion Notes List

- Added `SlidePreviewWidget` with explicit empty, needs_update, loading, rendered, render_error, and no-visible-layer states.
- Preview projection now displays render-affecting source-of-truth values: composition id, view center/scale, visible layer order, effective grid interval/label format, and target preview background metadata.
- Review/Edit now embeds the slide preview widget and schedules debounced preview updates on selection plus layer, view, and grid edits.
- Preview requests use generation/signature tokens so stale debounced completions cannot overwrite newer composition state.
- Sanity review split debounce completion from render completion so `loading` is an observable UI/test state before rendered output applies.
- Render errors show Vietnamese recovery text and are cleared by later successful preview updates.
- Kept scope inside `editor/widgets` and `editor/modes`; no Epic 5 raster/final render pipeline was implemented.
- Code review findings resolved: map background string support, stale success rejection after render error, deterministic debounce interval clamping, normalized metadata signatures, and view rotation display.

### File List

- `_bmad-output/implementation-artifacts/3-6-implement-slide-preview-panel-with-debounced-updates.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/widgets/slide_preview.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context and started implementation.
- 2026-05-25: Implemented debounced slide preview widget, Review/Edit wiring, and focused tests; marked ready for review.
- 2026-05-25: Fixed sanity-review issue where loading state was applied and cleared in the same call.
- 2026-05-25: Resolved code review findings, reran quality gates, and marked story done.
