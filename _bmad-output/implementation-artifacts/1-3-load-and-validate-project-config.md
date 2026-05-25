# Story 1.3: Load and Validate Project Config

Status: done

## Story

As an Operator,
I want the app to load a project config file and validate target references,
so that only usable enabled targets enter the workflow.

## Acceptance Criteria

1. **Given** the Operator selects a readable `config.json`  
   **When** the app loads the config  
   **Then** it resolves config-relative paths for target GeoJSON and template metadata files  
   **And** it includes only targets where `enabled=true`  
   **And** it sorts enabled targets by `sort_order`.

2. **Given** a config file is missing a required field or contains invalid data  
   **When** the app attempts to load it  
   **Then** the load fails with a structured issue or validation result  
   **And** the message explains the required correction in Vietnamese.

3. **Given** an enabled target omits `coordinate`, `scale`, or `grid.interval`, or provides invalid values  
   **When** the config is validated  
   **Then** the load fails with a structured issue tied to the target field path  
   **And** the Vietnamese remediation explains that `coordinate` must be `[lon, lat]`, `scale` must be a positive map scale denominator, and grid interval must be valid DMS-compatible configuration.

4. **Given** an enabled target references a missing GeoJSON or template metadata file  
   **When** the config is validated  
   **Then** the target receives a blocking validation issue  
   **And** ingestion/export cannot proceed for that target until the reference is fixed.

5. **Given** a template metadata file references a PPTX template path  
   **When** template metadata is loaded  
   **Then** paths inside the metadata resolve relative to the metadata file  
   **And** missing or invalid template metadata is treated as a blocking error.

## Tasks / Subtasks

- [x] Build config loader service (AC: 1, 2)
  - [x] Create `src/thucthengay/config/loader.py` for JSON file reading and decode errors.
  - [x] Create `src/thucthengay/config/path_resolver.py` for config-relative and metadata-relative path resolution.
  - [x] Create `src/thucthengay/config/service.py` with `load_project_config(config_path)`.
  - [x] Return a typed result containing parsed config, enabled targets sorted by `sort_order`, loaded template metadata, resolved reference paths, and issues.

- [x] Convert failures into structured Vietnamese issues (AC: 2, 3, 4, 5)
  - [x] Convert unreadable/malformed JSON into blocking `Issue` objects.
  - [x] Convert Pydantic `ValidationError.errors()` into field-path-aware blocking config issues.
  - [x] Include Vietnamese remediation for `coordinate`, `scale`, and `grid.interval`.
  - [x] Add blocking target issues for missing GeoJSON and missing template metadata files.
  - [x] Add blocking template issues for invalid template metadata or missing referenced PPTX.

- [x] Add focused unit tests (AC: 1, 2, 3, 4, 5)
  - [x] Test enabled target filtering, `sort_order`, and config-relative path resolution.
  - [x] Test invalid required fields produce Vietnamese structured issues with field paths.
  - [x] Test missing GeoJSON/template metadata references produce blocking target issues.
  - [x] Test template `template_pptx` resolves relative to the metadata file.
  - [x] Keep tests independent of real project data, network, GeoTIFF, PPTX content, or Qt.

- [x] Run quality gates and update story record
  - [x] Run documented `ttn-env` pytest command.
  - [x] Run documented `ttn-env` ruff command.
  - [x] Run documented `ttn-env` app entrypoint command.
  - [x] Update Dev Agent Record, File List, Change Log, and sprint status.

### Review Findings

- [x] [Review][Patch] Disabled targets must not block config load via schema/reference validation [src/thucthengay/config/service.py:48]
- [x] [Review][Patch] Directory or other unreadable config paths should return structured issues instead of escaping `OSError` [src/thucthengay/config/service.py:49]

## Dev Notes

### Scope Boundaries

- This story loads and validates project config references only.
- Do not implement Setup UI path picker; Story 1.4 owns UI.
- Do not implement workspace creation/persistence; Story 1.5 owns workspace.
- Do not inspect GeoTIFFs or run ingestion.
- Do not mutate config files.

### Implementation Guidance

- Use models from `src/thucthengay/models/`; do not create duplicate dataclasses for config/template/issue.
- Path existence checks belong in config service, not Pydantic model validators.
- Config target paths resolve relative to the selected `config.json`.
- Paths inside template metadata, especially `template_pptx`, resolve relative to the metadata JSON file.
- Disabled targets do not enter `enabled_targets` and should not get filesystem reference checks in this story.
- Return structured issues rather than raw exceptions for expected user/config problems.
- Messages and remediation shown to users must be Vietnamese.
- Keep services headless; no `PySide6` or `editor` imports.

### Previous Story Learnings

- Story 1.2 is done and provides shared Pydantic models.
- `IssueSeverity.ERROR` normalizes to `blocking=True`.
- `TargetConfig` validates `coordinate`, positive `scale`, and `grid.interval`.
- Use conda env `ttn-env` and `UV_PROJECT_ENVIRONMENT` with `uv run --no-sync`.
- Existing import-boundary tests guard against UI imports in core packages.

### References

- [Epics: Story 1.3] `_bmad-output/planning-artifacts/epics.md`
- [Architecture: Validation Strategy] `_bmad-output/planning-artifacts/architecture.md`
- [PRD: FR1 and FR20] `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md`
- [Project Context] `_bmad-output/project-context.md`
- [Previous story] `_bmad-output/implementation-artifacts/1-2-define-core-pydantic-models.md`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` passed: 22 tests collected, 22 passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` passed: all checks passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay` passed and printed the minimal scaffold message.
- 2026-05-25: Code review found disabled-target filtering and unreadable-path handling issues; both were patched.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` passed: 24 tests collected, 24 passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` passed: all checks passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay` passed and printed the minimal scaffold message.

### Completion Notes List

- Added config JSON loader, relative path resolver, and `load_project_config`.
- Added structured `ConfigLoadResult` with sorted enabled targets, resolved target paths, loaded template metadata, and blocking issues.
- Converts JSON/Pydantic/reference/template failures into Vietnamese `Issue` objects.
- Added tests for enabled filtering, path resolution, invalid field issues, missing references, metadata-relative PPTX resolution, and invalid template metadata.
- Review patch: disabled targets are filtered before schema/reference validation so they do not block config load.
- Review patch: unreadable config paths covered by `OSError` now return blocking config issues.

### File List

- `_bmad-output/implementation-artifacts/1-3-load-and-validate-project-config.md`
- `src/thucthengay/config/__init__.py`
- `src/thucthengay/config/loader.py`
- `src/thucthengay/config/path_resolver.py`
- `src/thucthengay/config/service.py`
- `tests/unit/test_config_service.py`

### Change Log

- 2026-05-25: Addressed code review findings and completed Story 1.3.
- 2026-05-25: Implemented Story 1.3 config loading and reference validation service.
- 2026-05-25: Created Story 1.3 with config loading, reference validation, and Vietnamese issue requirements.
