# Story 3.4: Implement GIS Editor Canvas View Controls

Status: done

## Story

As an Operator,
I want to pan and zoom imagery under a fixed map frame,
so that I can choose the exact target-centered map view used in the slide map.

## Acceptance Criteria

1. Given a selected composition has visible raster layers, when the GIS editor canvas loads, then it displays raster layers under a fixed map frame overlay, and it shows loading/error/empty states when raster data is not ready or unavailable.
2. Given the Operator pans or zooms the canvas, when the interaction completes, then the source-of-truth `view.center` `[lon, lat]` and `view.scale` are persisted in the composition, and rotation remains fixed at 0 with no MVP rotation UI.
3. Given the Operator uses mouse wheel zoom or optional zoom slider, when zoom changes, then `view.scale` changes while the map frame aspect is preserved according to template metadata/config, and the composition is marked `needs_revalidation=true` and preview stale/needs update.
4. Given raster rendering is in progress, when a newer canvas interaction supersedes an older render request, then stale render results are ignored, and the canvas does not apply a result for an outdated center/scale state.

## Tasks / Subtasks

- [x] Add workspace service API for view edits (AC: 2, 3)
  - [x] Persist `view.center` and `view.scale` by composition id.
  - [x] Preserve `view.rotation=0` and reject invalid center/scale through existing `ViewState` validation.
  - [x] Mark the composition `needs_revalidation=true` and clear ready/include/review_order after view edits.
  - [x] Preserve existing validation summary and layer state.
- [x] Add GIS canvas widget for Review/Edit (AC: 1-4)
  - [x] Use a Qt `QGraphicsView`-based widget owned by `editor/widgets/`.
  - [x] Display visible layers as deterministic raster placeholders until Epic 5 render core is available.
  - [x] Draw a fixed map frame overlay with stable aspect ratio and non-color-only state text.
  - [x] Show empty, loading, error, and ready/stale states in Vietnamese.
  - [x] Support mouse drag pan and wheel zoom, emitting edit-complete events only after interaction completion.
  - [x] Track render request generations and ignore stale results that do not match the latest view state.
- [x] Wire GIS canvas into `ReviewEditMode` (AC: 1-4)
  - [x] Replace the Story 3.1/3.3 GIS placeholder label with the canvas widget.
  - [x] Load selected composition view/layers into the canvas when tree selection changes.
  - [x] Persist pan/zoom edits through `WorkspaceService`.
  - [x] Refresh tree/filter state and selected composition after view edits.
  - [x] Surface save/render state errors through the existing warnings summary.
- [x] Add focused tests (AC: 1-4)
  - [x] Test service view persistence and stale-state reset.
  - [x] Test invalid view edits do not partially write state.
  - [x] Test GIS canvas state text, fixed-frame presence, visible-layer/empty handling, and stale result guard.
  - [x] Test Review/Edit UI saves pan/zoom view edits through the service and marks preview/view stale.

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `workspace/`: source of truth for persisted composition JSON; view edit methods belong here.
  - `models/`: `ViewState` already defines `[lon, lat]`, positive scale, and `rotation=0`; do not duplicate persisted schemas.
  - `editor/widgets/`: reusable Qt GIS canvas widget and interaction/state projection only.
  - `editor/modes/`: Review/Edit widget wiring and service calls only; no raw JSON reads/writes.
- Build on Stories 3.1-3.3:
  - `ReviewEditMode` already loads selected composition via `WorkspaceService.read_composition()`.
  - Layer visibility/order edits already mark composition stale and refresh the tree.
  - The tree exposes no-visible-layer as a non-color-only error before full Epic 4 validation exists.
- View edit rule:
  - Any pan/zoom edit must persist through `WorkspaceService`, set `needs_revalidation=true`, and clear `ready=false`, `include=false`, `review_order=None`.
  - Preserve `validation_summary`; stale state is inferred from `needs_revalidation`.
  - Rotation remains hard-fixed to `0`; do not add rotation UI.
- Rendering scope:
  - Full raster window math, CRS transforms, two-stage preview rendering, final PNG alignment, and render logs belong to Epic 5.
  - For this story, the canvas should render deterministic layer placeholders and expose loading/error/empty states so UI workflow and persistence are testable now.
  - The widget must still model stale render protection via request generation tokens so Epic 5 can attach real render jobs later.
- UX requirements:
  - Use a dark/neutral GIS canvas, fixed map frame overlay, state text, and stable layout.
  - Status must not rely only on color.
  - Mouse drag pans; wheel zoom changes scale; optional slider can be omitted if wheel zoom is covered.
  - No PyQGIS; use Qt Widgets only.
- Keep scope tight: do not implement grid override controls, slide preview render debounce, final render, metadata editor, warnings jump links, or review action transitions in this story.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.4]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#GIS Editor Canvas]
- [Source: _bmad-output/planning-artifacts/architecture.md#GIS / Spatial Architecture]
- [Source: _bmad-output/implementation-artifacts/3-3-implement-layer-stack-controls.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `pytest tests/unit/test_workspace_service.py tests/unit/test_review_edit_mode.py` - 33 passed.
- `ruff check .` - all checks passed.
- `pytest` - 94 passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.

### Completion Notes List

- Added `WorkspaceService.update_view_state()` so pan/zoom edits persist through the workspace source of truth.
- View edits validate through `ViewState`, force `rotation=0`, mark compositions stale, and clear ready/include/review_order while preserving validation summary and layers.
- Added `GisCanvasWidget`, a `QGraphicsView`-based Review/Edit canvas with deterministic visible-layer placeholders, fixed map frame overlay, Vietnamese state text, pan/zoom controls, and render generation tokens.
- Wired the canvas into `ReviewEditMode` and replaced the prior GIS placeholder.
- Review/Edit now loads target metadata `map_frame_aspect` or `map_frame.width/height` when available and falls back to the MVP 16:9 canvas frame.
- Added focused service and UI tests for view persistence, invalid view protection, canvas states, stale render result rejection, and Review/Edit pan/zoom saves.

### File List

- `_bmad-output/implementation-artifacts/3-4-implement-gis-editor-canvas-view-controls.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/workspace/service.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/widgets/gis_canvas.py`
- `tests/unit/test_workspace_service.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-25: Created story context for Epic 3 Story 3.4 and started implementation.
- 2026-05-25: Implemented workspace view persistence, GIS canvas widget, Review/Edit wiring, and focused tests.
- 2026-05-25: Completed internal review and marked story done after quality gates passed.

## Senior Developer Review (AI)

Outcome: Approve

### Findings

- Fixed before completion: the canvas initially supported a configurable frame aspect but Review/Edit only used the default 16:9 aspect. Added target metadata lookup for `map_frame_aspect` and `map_frame.width/height`, plus a Review/Edit test covering the 4:3 path.

### Verification

- `pytest` - 94 passed.
- `ruff check .` - all checks passed.
- `python -m thucthengay` headless smoke - app ready.
- `git diff --check` - clean.
