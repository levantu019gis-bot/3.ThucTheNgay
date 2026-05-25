# Story 2.4: Create Target-Date Composition JSON Files

Status: done

## Story

As an Operator,
I want matched imagery grouped into target-date compositions,
so that each report slide can be reviewed as a separate unit of work.

## Acceptance Criteria

1. Given matched cached imagery exists for a target across one or more capture dates, when composition creation runs, then the app creates one composition JSON per target-date and multi-date imagery for the same target is split into separate compositions.
2. Given a new composition is created, when its default state is initialized, then `reviewed=false`, `ready=false`, `include=false`, `needs_revalidation=true`, `review_order` is unset, `view.center` is initialized from target config coordinate, and `view.scale` is initialized from target scale denominator.
3. Given multiple layers exist in a composition, when the layer stack is initialized, then newest valid capture time appears on top by default and layers with missing required capture time are retained but marked for metadata correction and validation warnings.
4. Given composition JSON is written to the workspace, when the write completes, then it is saved through `WorkspaceService` using atomic write behavior and paths inside the composition prefer workspace-relative references where possible.

## Tasks / Subtasks

- [x] Add composition creation contracts (AC: 1, 2, 3, 4)
  - [x] Consume cached layers grouped by `(target_id, date_key)`.
  - [x] Return created composition IDs and non-blocking issues.
- [x] Create and persist target-date compositions (AC: 1, 2, 4)
  - [x] Build composition IDs as `target_id__YYYYMMDD`.
  - [x] Initialize view state from target coordinate and scale.
  - [x] Persist through `WorkspaceService.write_composition`.
- [x] Initialize layer stack deterministically (AC: 3)
  - [x] Sort newest valid capture time first.
  - [x] Retain layers with missing capture time and mark them for manual correction.
  - [x] Assign sequential layer order values.
- [x] Add focused tests and run quality gates (AC: 1, 2, 3, 4)

## Dev Notes

- Owner module: `src/thucthengay/ingestion/composition_builder.py`.
- Do not implement ingestion progress or warning UI in this story.
- Do not run detailed validation rules; Epic 4 owns validation engine. Persist `needs_revalidation=true` defaults.
- Use `WorkspaceService` as the only composition JSON writer.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.4-Create-Target-Date-Composition-JSON-Files]
- [Source: _bmad-output/project-context.md#Data-State-Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Red test: `pytest tests/unit/test_ingestion_composition_builder.py` failed on missing `create_target_date_compositions` import before implementation.
- Focused green test: `pytest tests/unit/test_ingestion_composition_builder.py` -> 4 passed.
- Full regression: `pytest` -> 68 passed.
- Lint: `ruff check .` -> All checks passed.
- App smoke: `python -m thucthengay` with `DISPLAY`/`WAYLAND_DISPLAY` unset -> `3.ThucTheNgay app ready.`
- Review result: clean after internal review; no open findings.

### Completion Notes List

- Added `ingestion/composition_builder.py` for creating one persisted composition per target/date group.
- Composition defaults come from the existing `Composition` model and view initializes from target coordinate/scale.
- Layer stack initializes with newest valid capture time on top and missing-time layers retained with `needs_manual_correction`.
- Composition JSON is written through `WorkspaceService.write_composition`, preserving atomic write and manifest registration behavior.

### File List

- `_bmad-output/implementation-artifacts/2-4-create-target-date-composition-json-files.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/ingestion/__init__.py`
- `src/thucthengay/ingestion/composition_builder.py`
- `tests/unit/test_ingestion_composition_builder.py`

### Change Log

- 2026-05-25: Created story context for Epic 2 Story 2.4.
- 2026-05-25: Implemented target-date composition creation and marked story done after internal review.
