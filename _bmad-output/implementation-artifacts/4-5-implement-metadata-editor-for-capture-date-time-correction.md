# Story 4.5: Implement Metadata Editor for Capture Date/Time Correction

Status: review

<!-- Created from Epic 4 backlog context per project autonomous execution mandate. -->

## Story

As an Operator,
I want to correct layer capture metadata manually,
so that imagery without complete metadata can still produce valid slide time labels.

## Acceptance Criteria

1. Given a selected layer has parsed or missing metadata, when the Metadata Editor opens, then it shows capture date/time fields, parsed source display, cloud percent, metadata source/status, and save/cancel actions, and the UI distinguishes parsed, manually corrected, and needs-manual-correction states.
2. Given the Operator enters a valid capture date/time, when the change is saved, then the layer metadata is persisted through `WorkspaceService`, and `metadata_status` and metadata source reflect manual correction.
3. Given the Operator enters an invalid date/time or required metadata remains missing, when they attempt to save, then the editor shows a Vietnamese validation message, and invalid metadata is not persisted as valid corrected metadata.
4. Given layer metadata changes, when the composition is saved, then the composition is marked `needs_revalidation=true`, and preview/time label state is refreshed or marked stale as appropriate.

## Tasks / Subtasks

- [x] Add `WorkspaceService.update_layer_metadata()` (AC: 2, 4)
  - [x] Method signature: `update_layer_metadata(composition_id, layer_id, *, capture_date, capture_time, cloud_percent, metadata_source, metadata_status) -> Composition`.
  - [x] Read composition, find layer by id (raise WorkspaceError if not found), model_copy with new fields.
  - [x] Apply `_mark_composition_edit_stale` to flag `needs_revalidation=true`.
  - [x] Write composition atomically through existing `write_composition`.
  - [x] Tests: persists each field correctly; composition becomes stale; missing layer raises; invalid combinations rejected via Pydantic.

- [x] Build MetadataEditorDialog (AC: 1, 3)
  - [x] Create `src/thucthengay/editor/widgets/metadata_editor.py` exposing `MetadataEditorDialog(QDialog)`.
  - [x] Constructor takes the current `ImageLayer` and shows its values as initial form state.
  - [x] Fields: capture date (`QDateEdit` allowing empty/null), capture time (`QTimeEdit` allowing empty/null), cloud percent (`QDoubleSpinBox` 0–100), source path (read-only label), original parsed source (read-only label showing `metadata_source.value`), state pill (read-only label showing `metadata_status.value` localized).
  - [x] Save and Cancel buttons; Save validates inputs and emits `metadataSaved(layer_id, payload_dict)`; Cancel closes without emit.
  - [x] Inline Vietnamese validation message label: "Cần nhập ngày chụp", "Cần nhập giờ chụp", "Giá trị mây phải trong 0–100".
  - [x] State pill text distinguishes: "Đã parse" (VALID), "Đã sửa thủ công" (MANUAL source), "Cần nhập tay" (NEEDS_MANUAL_CORRECTION), "Chưa rõ" (UNKNOWN).
  - [x] Export `MetadataEditorDialog` from `editor/widgets/__init__.py`.
  - [x] Tests: dialog populates with layer values; valid save emits signal with correct payload; invalid save shows Vietnamese message and does not emit.

- [x] Wire MetadataEditorDialog into ReviewEditMode (AC: 1, 2, 4)
  - [x] Add "Sửa metadata" button to layer panel toolbar (next to up/down move buttons).
  - [x] Clicking opens `MetadataEditorDialog` for the currently selected layer in `layer_table`.
  - [x] On `metadataSaved`, call `WorkspaceService.update_layer_metadata(...)` with returned payload.
  - [x] After save: refresh `selected_composition`, update detail panels, layer model, preview, warnings panel (revalidate on next selection).
  - [x] If save fails (WorkspaceError), set `action_summary` with Vietnamese error message.
  - [x] Tests: button enabled only with a layer selected; save persists; composition `needs_revalidation` becomes true; preview marked stale (existing behavior via `_mark_composition_edit_stale`).

- [x] Add focused integration tests (AC: 1-4)
  - [x] WorkspaceService unit tests: 3+ scenarios.
  - [x] MetadataEditorDialog widget tests (offscreen): 4+ scenarios.
  - [x] ReviewEditMode integration: open editor + save updates workspace.
  - [x] Run full pytest + ruff check + smoke test.

## Dev Notes

- Follow `_bmad-output/project-context.md` for env/quality rules.
- Owner modules:
  - `workspace/service.py`: add `update_layer_metadata()` — single source of truth for layer metadata writes.
  - `editor/widgets/metadata_editor.py`: new dialog (NEW FILE).
  - `editor/widgets/__init__.py`: export `MetadataEditorDialog`.
  - `editor/modes/review_edit_mode.py`: add edit button and integration.
- Scope guard:
  - Story 4.6 owns the cache-move confirmation when capture_date crosses target-date grouping. Story 4.5 saves whatever valid date the user enters within the existing composition; composition_id and target-date grouping are NOT changed here.
  - No new Pydantic field on `ImageLayer` — use existing `capture_date`/`capture_time`/`cloud_percent`/`metadata_status`/`metadata_source`.
  - On manual save, set `metadata_source = MANUAL` and `metadata_status = VALID` if all required fields present; otherwise keep `NEEDS_MANUAL_CORRECTION`.
- After implementation: pytest + ruff + smoke.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.5]
- [Source: src/thucthengay/models/layer.py]
- [Source: src/thucthengay/workspace/service.py — pattern: `set_layer_visibility`]
- [Source: src/thucthengay/editor/widgets/warnings_panel.py — widget pattern]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6 (continued in plan mode)

### Debug Log References

- `conda run -n ttn-env pytest` — 157 passed.
- `conda run -n ttn-env ruff check .` — All checks passed.
- `PYTHONPATH=src conda run -n ttn-env python -m thucthengay --smoke` — App ready.

### Completion Notes List

- Added `WorkspaceService.update_layer_metadata()` — atomic write + `_mark_composition_edit_stale`.
- Created `MetadataEditorDialog` (QDialog): date/time/cloud fields with nullable checkboxes, Vietnamese validation, state pill.
- On save: `metadata_source` set to MANUAL; `metadata_status` becomes VALID iff both date+time present, else NEEDS_MANUAL_CORRECTION.
- Wired "Sửa metadata" button into ReviewEditMode layer panel; opens dialog for current layer.
- 12 new tests in `test_metadata_editor.py` covering workspace persistence + dialog UI behavior.
- Scope guard respected: composition_id and target-date grouping unchanged in this story; Story 4.6 will add cache-move confirmation when date crosses target-date boundary.

### File List

- `_bmad-output/implementation-artifacts/4-5-implement-metadata-editor-for-capture-date-time-correction.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/workspace/service.py`
- `src/thucthengay/editor/widgets/metadata_editor.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `tests/unit/test_metadata_editor.py`

## Change Log

- 2026-05-25: Created story context from Epic 4 backlog and started implementation.
- 2026-05-25: Implemented WorkspaceService method + MetadataEditorDialog + ReviewEditMode integration + 12 tests. All gates pass.
