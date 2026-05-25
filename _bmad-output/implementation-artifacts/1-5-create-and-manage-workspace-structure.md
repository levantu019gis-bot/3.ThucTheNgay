# Story 1.5: Create and Manage Workspace Structure

Status: done

## Story

As an Operator,
I want the app to create and manage a predictable workspace folder,
So that project state and generated artifacts are inspectable and recoverable.

## Requirement References

- FR2
- FR6
- AR4
- AR5
- AR11
- AR12
- NFR2
- NFR3
- NFR9

## Acceptance Criteria

1. Given the Operator selects a valid workspace folder, when workspace initialization runs, then `WorkspaceService` creates or verifies `manifest.json`, `cache/`, `compositions/`, `renders/`, and `exports/`, and all workspace reads and writes go through `WorkspaceService`.
2. Given a workspace already contains app-owned data, when the Operator starts an operation that would clear cache, compositions, renders, or exports, then the app shows an explicit confirmation dialog, the safe/default action avoids destructive clearing, and destructive action labels name what will be cleared.
3. Given the app writes manifest or composition JSON, when a write succeeds, then the file is written atomically using a temporary file and replace operation, and failed writes do not leave partial invalid JSON at the final path.
4. Given a workspace path is later reopened, when `WorkspaceService` loads it, then the manifest and known subfolders are detected, and recoverable missing folders are recreated without changing composition state.

## Implementation Context

- Prior stories completed the scaffold, models, config loading, and Setup path picker.
- `workspace/` is the only package that reads/writes `manifest.json` and `compositions/*.json`.
- Other domains should request workspace state through `WorkspaceService`.
- Runtime user project layout includes `workspace/manifest.json`, `workspace/cache/`, `workspace/compositions/`, `workspace/renders/`, and `workspace/exports/`.
- Workspace JSON should use workspace-relative paths where possible.
- Destructive clearing is app-owned data only: cache, compositions, renders, exports. It must require explicit confirmation.
- Do not implement ingestion, composition creation from GeoTIFFs, review state editing, rendering, or export in this story.

## Tasks

- [x] Add workspace path/layout helpers.
- [x] Add atomic JSON writer for manifest and composition files.
- [x] Add `WorkspaceService` for initialize/load/read/write/clear operations.
- [x] Add UI confirmation helper for destructive workspace clearing.
- [x] Add unit tests covering initialization, reopen recovery, atomic writes, composition IO, and clear confirmation guard.
- [x] Run quality gates.

## Dev Agent Record

### Debug Log

- 2026-05-25: Confirmed Story 1.5 is the next backlog story after 1.4 completion.
- 2026-05-25: Reviewed epics and architecture workspace layout/boundary notes.
- 2026-05-25: Implemented `WorkspaceService`, atomic writes, clear confirmation guard, and Setup confirmation hook.
- 2026-05-25: Ran `pytest`, `ruff check .`, and `python -m thucthengay --smoke`; all passed.

### Completion Notes

- `WorkspaceService` now creates/verifies `manifest.json`, `cache/`, `compositions/`, `renders/`, and `exports/`.
- Manifest and composition JSON writes are atomic through a temp file plus replace operation.
- Reopening a workspace recreates missing known folders while preserving manifest composition state.
- Destructive clearing requires explicit confirmation at the service layer and Setup mode asks through a confirmation dialog before emitting ingest intent when app-owned data exists.

### File List

- `_bmad-output/implementation-artifacts/1-5-create-and-manage-workspace-structure.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/workspace/__init__.py`
- `src/thucthengay/workspace/atomic_write.py`
- `src/thucthengay/workspace/paths.py`
- `src/thucthengay/workspace/service.py`
- `src/thucthengay/editor/widgets/workspace_confirmation.py`
- `tests/unit/test_workspace_service.py`

### Change Log

- 2026-05-25: Added story context and started implementation.
- 2026-05-25: Completed workspace structure management and tests.
