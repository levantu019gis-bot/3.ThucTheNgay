# Story 2.3: Copy Matched Imagery into Workspace Cache

Status: done

## Story

As an Operator,
I want matched imagery copied into the workspace cache,
so that the project can be reviewed from a stable app-owned workspace.

## Acceptance Criteria

1. Given imagery has been matched to one or more targets, when cache population runs, then the app copies matched files into `workspace/cache/` using a deterministic target/date-oriented structure and preserves source file path, cached file path, metadata source, capture metadata, and cloud percent where available in layer records.
2. Given the same source image is encountered again for the same target/date, when cache population runs, then the app avoids duplicate cache entries where file identity can be established and the resulting layer list remains deterministic across repeated ingestion runs.
3. Given a source file cannot be copied due to permission, missing file, or IO failure, when cache population attempts the copy, then ingestion records a warning with the source path and reason and the failed file is not included in composition layer records.
4. Given the workspace cache already contains prior app-owned imagery, when ingestion would clear or replace it, then the operation only proceeds after the explicit workspace clear confirmation defined in Epic 1 and the summary records that cache contents were recreated.

## Tasks / Subtasks

- [x] Add cache population contracts (AC: 1, 2, 3, 4)
  - [x] Return cached layer records grouped by target/date without writing composition JSON.
  - [x] Preserve metadata fields from Story 2.1 scan layer records.
- [x] Copy matched files into deterministic workspace cache structure (AC: 1, 2)
  - [x] Use `workspace/cache/<target_id>/<date_key>/` as the target/date-oriented folder.
  - [x] Use a stable source identity hash in cache filenames to avoid same-name collisions.
  - [x] Deduplicate repeated same source/target/date matches.
- [x] Handle failures and clear confirmation (AC: 3, 4)
  - [x] Emit warning `Issue` objects for copy failures and exclude failed files from cached layers.
  - [x] Require Epic 1 workspace clear confirmation before clearing existing app-owned data.
  - [x] Record whether cache contents were recreated.
- [x] Add focused tests and run quality gates (AC: 1, 2, 3, 4)
  - [x] Cover copy path/metadata preservation, duplicate dedupe, copy failure warning, and confirmed clear behavior.
  - [x] Run `pytest`, `ruff check .`, and app smoke through `ttn-env`.

## Dev Notes

### Scope Boundaries

- This story consumes `TargetMatchingResult` from Story 2.2 and `WorkspaceService` from Epic 1.
- Do not create composition JSON; Story 2.4 owns composition creation.
- Do not implement progress jobs or summary UI; Stories 2.5 and 2.6 own those.

### Architecture Requirements

- Owner module: `src/thucthengay/ingestion/cache_builder.py`.
- Workspace-owned writes must go under `WorkspaceService.paths.cache`; do not write app-owned data outside workspace.
- Use shared `ImageLayer` and `Issue` models.
- Core ingestion code must not import `PySide6` or `editor`.

### Implementation Guidance

- Date key should be `YYYYMMDD` when `capture_date` exists, otherwise a deterministic fallback such as `unknown_date`.
- Cache paths stored in layer records should be workspace-relative where possible, e.g. `cache/target_001/20260525/image__hash.tif`.
- Use `shutil.copy2` to preserve file metadata where the filesystem supports it.
- For duplicate detection, source identity may be the resolved source path; this is deterministic and sufficient for MVP.
- If `clear_existing=True`, call the existing Epic 1 workspace clear guard and require `clear_confirmed=True`.

### Previous Story Learnings

- Story 2.1 provides stable unique source layer IDs and metadata.
- Story 2.2 returns deterministic matches by enabled target order and scan result order.
- WorkspaceService already provides explicit clear confirmation and app-owned folder cleanup.

### Testing Requirements

- Tests should use `tmp_path` source files; no committed binary imagery is needed.
- Run full regression after implementation.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.3-Copy-Matched-Imagery-into-Workspace-Cache]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-3-Scan-and-match-GeoTIFF-imagery]
- [Source: _bmad-output/project-context.md#Module-Ownership-Rules]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Red test: `pytest tests/unit/test_ingestion_cache_builder.py` failed on missing `populate_workspace_cache` import before implementation.
- Focused green test: `pytest tests/unit/test_ingestion_cache_builder.py` -> 4 passed.
- Full regression: `pytest` -> 64 passed.
- Lint: `ruff check .` -> All checks passed.
- App smoke: `python -m thucthengay` with `DISPLAY`/`WAYLAND_DISPLAY` unset -> `3.ThucTheNgay app ready.`
- Review result: clean after internal review; no open findings.

### Completion Notes List

- Added `ingestion/cache_builder.py` for deterministic workspace cache population from target matches.
- Cache paths use `cache/<target_id>/<date_key>/<stem>__<hash><suffix>` and are stored workspace-relative on layer records.
- Repeated same source/target/date matches dedupe to one cached layer and one cache file.
- Copy failures produce warning `Issue` objects and failed files are excluded from returned layer records.
- Existing app-owned data clear requires `WorkspaceService` confirmation guard and records `cache_recreated=True`.

### File List

- `_bmad-output/implementation-artifacts/2-3-copy-matched-imagery-into-workspace-cache.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/ingestion/__init__.py`
- `src/thucthengay/ingestion/cache_builder.py`
- `tests/unit/test_ingestion_cache_builder.py`

### Change Log

- 2026-05-25: Created story context for Epic 2 Story 2.3.
- 2026-05-25: Implemented workspace cache population and marked story done after internal review.
