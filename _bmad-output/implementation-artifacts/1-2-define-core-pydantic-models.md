# Story 1.2: Define Core Pydantic Models

Status: done

<!-- Context engine: created from epics, PRD, architecture, UX spec, and Story 1.1 learnings. -->

## Story

As a Developer,
I want typed Pydantic models for project config and workspace state,
so that application services share one validated data contract.

## Acceptance Criteria

1. **Given** config and workspace JSON data is loaded by services  
   **When** the data is parsed  
   **Then** Pydantic models validate target config, workspace manifest, composition, layer, template metadata, issue, render result, and export log structures  
   **And** validation errors identify the field path that failed.

2. **Given** a target config contains template metadata references  
   **When** the config model is parsed  
   **Then** each target supports target-specific template metadata fields  
   **And** the model can represent `template_metadata_file`, `geojson_file`, target identity, enabled state, `sort_order`, target `coordinate` `[lon, lat]`, target `scale` as a positive map scale denominator, and target grid interval.

3. **Given** a composition is represented in JSON  
   **When** it is parsed or serialized  
   **Then** the model includes target/date identity, layer list, view center/scale, grid override, status fields, validation summary, and workspace-relative artifact references where applicable  
   **And** defaults match the PRD: `reviewed=false`, `ready=false`, `include=false`, and newest layer ordering can be represented.

4. **Given** an issue is produced by validation  
   **When** it is serialized  
   **Then** it includes `issue_id`, `severity`, `scope`, target/composition/layer references, Vietnamese message/remediation, and `blocking`.

## Tasks / Subtasks

- [x] Define shared issue and status contracts (AC: 1, 4)
  - [x] Create `src/thucthengay/models/issue.py` with `IssueSeverity`, `IssueScope`, and `Issue`.
  - [x] Ensure `severity=error` can represent blocking validation errors via `blocking`.
  - [x] Keep `message` and `remediation` as plain strings; do not hardcode message catalogs in this story.

- [x] Define config and template metadata models (AC: 1, 2)
  - [x] Create `src/thucthengay/models/config.py` with project-level config and target config models.
  - [x] Represent enabled targets, `sort_order`, `geojson_file`, `coordinate`, positive `scale`, grid settings, export settings, and `template_metadata_file`.
  - [x] Validate `coordinate` as exactly `[lon, lat]` with lon in `[-180, 180]` and lat in `[-90, 90]`.
  - [x] Validate `scale` as a positive map scale denominator.
  - [x] Create `src/thucthengay/models/template.py` for template metadata: `template_pptx`, `slide_index`, map frame geometry, and placeholders.
  - [x] Keep path values JSON-friendly and config-relative; do not resolve filesystem paths here.

- [x] Define workspace, composition, layer, render, and export models (AC: 1, 3)
  - [x] Create `src/thucthengay/models/workspace.py` for workspace manifest/index state.
  - [x] Create `src/thucthengay/models/layer.py` for `ImageLayer`, metadata status/source, capture date/time, cloud percent, source/cache path refs, visibility, and order.
  - [x] Create `src/thucthengay/models/composition.py` for `Composition`, `ViewState`, grid override, status fields, validation summary, notes, artifact refs, and layer list.
  - [x] Create `src/thucthengay/models/render.py` for render result/log metadata needed by later render/export stories.
  - [x] Create `src/thucthengay/models/export.py` for export log/summary structures needed by later export stories.
  - [x] Ensure composition defaults are `reviewed=false`, `ready=false`, `include=false`, `needs_revalidation=true` for new/changed compositions unless a source document explicitly says otherwise.

- [x] Expose model API without leaking UI dependencies (AC: 1)
  - [x] Update `src/thucthengay/models/__init__.py` to export the public model classes/enums used by later stories.
  - [x] Do not import `PySide6` or any `thucthengay.editor` module from `models/`.
  - [x] Do not implement config loading, workspace persistence, validation rules, GIS math, rendering, or export services in this story.

- [x] Add focused model tests (AC: 1, 2, 3, 4)
  - [x] Add unit tests under `tests/unit/` for valid config/template/composition/issue round trips.
  - [x] Add tests proving validation errors include useful Pydantic field locations for invalid coordinate, negative/zero scale, invalid issue severity, and missing required template metadata.
  - [x] Add tests for default composition status fields.
  - [x] Keep tests independent of network, real GeoTIFF files, real PPTX files, or Qt event loops.
  - [x] Keep existing import-boundary tests passing.

- [x] Run quality gates and update story record (AC: 1)
  - [x] Run `uv run pytest` or the documented conda fallback equivalent.
  - [x] Run `uv run ruff check .` or the documented conda fallback equivalent.
  - [x] Run `uv run python -m thucthengay` or the documented conda fallback equivalent.
  - [x] Update Dev Agent Record, File List, and Change Log.

### Review Findings

- [x] [Review][Patch] Ensure `severity=error` issues are always blocking [src/thucthengay/models/issue.py:42]
- [x] [Review][Patch] Validate render result center as `[lon, lat]` range, not just length [src/thucthengay/models/render.py:22]

## Dev Notes

### Scope Boundaries

This story creates typed data contracts only. It must not implement:

- config file loading/path resolution beyond Pydantic field validation;
- checking whether referenced files exist;
- `WorkspaceService` or atomic JSON writes;
- ingestion, GeoTIFF metadata extraction, GIS intersection, render math, validation rules, or export logic;
- any PySide6 UI models/widgets.

Story 1.3 loads and validates config files. Story 1.5 owns workspace persistence. Epic 4 owns full validation rule behavior.

### Required Source Files

Create or update these source files:

```text
src/thucthengay/models/__init__.py
src/thucthengay/models/config.py
src/thucthengay/models/workspace.py
src/thucthengay/models/composition.py
src/thucthengay/models/layer.py
src/thucthengay/models/template.py
src/thucthengay/models/issue.py
src/thucthengay/models/render.py
src/thucthengay/models/export.py
tests/unit/test_models_*.py
```

### Model Guidance

- Use Pydantic v2 (`pydantic.BaseModel`, `Field`, validators as needed).
- Use JSON field names in `snake_case`.
- Prefer JSON-safe fields (`str`, `int`, `float`, `bool`, `list`, `dict`, `date`, `time`, `datetime`) over `Path` in persisted models.
- Use `model_config = ConfigDict(extra="forbid")` unless a model explicitly needs extension metadata.
- Use stable enums where later UI/validation/export code must branch: issue severity/scope, metadata status/source, placeholder type if useful.
- Keep domain naming aligned with PRD glossary: `Target`, `ImageLayer`, `Composition`, `Workspace`, `TemplateMetadata`, `Issue`.
- Architecture names `ViewExtent`, but the latest PRD/architecture decisions use `view.center` and `view.scale`; implement `ViewState`, not bbox extent, unless a compatibility alias is explicitly needed.
- `scale` means map scale denominator: `50000` means 1:50,000.
- Composition id format is `target_id__YYYYMMDD`; the model may validate the format if practical, but do not overbuild id generation.

### Minimum Suggested Model Shapes

The exact field names may be adjusted if tests and architecture remain consistent, but the implementation should cover at least:

- `Issue`: `issue_id`, `severity`, `scope`, optional `target_id`, optional `composition_id`, optional `layer_id`, `message`, optional `remediation`, `blocking`.
- `TargetConfig`: `id`, `enabled`, `sort_order`, name/title/alias fields, `geojson_file`, `coordinate`, `scale`, `grid`, `export`, optional metadata.
- `GridConfig`: interval and label/style settings; enough to represent target grid interval and future per-composition override.
- `TemplateMetadata`: `template_pptx`, `slide_index`, map frame rectangle, placeholders.
- `ImageLayer`: stable layer id, file refs, visibility, order, capture date/time, cloud percent, metadata status/source.
- `Composition`: `composition_id`, `target_id`, date identity, status fields, `review_order`, `notes`, `view`, grid override, layers, validation summary, artifact refs.
- `WorkspaceManifest`: workspace schema/version plus references/indexes needed for later workspace service.
- `RenderResult`: composition id, output path, image width/height, center/scale, visible layer ids/order, issue list.
- `ExportLog`/summary: output paths, slide count, target count, skipped count, warning/error counts, exported/skipped composition refs, issue summary.

### Previous Story Learnings

Story 1.1 is done. It established:

- Python baseline is `>=3.11,<3.12`.
- Runtime dependencies include PySide6, Pydantic, rasterio, shapely, pyproj, numpy, Pillow, python-pptx.
- Conda fallback keeps native GIS packages under conda-forge and uses `UV_PROJECT_ENVIRONMENT` plus `uv run --no-sync`.
- Core import-boundary tests forbid `PySide6` and `thucthengay.editor` imports from non-UI core packages, including static imports and constant-string dynamic imports.
- Current scaffold has only package placeholders; no model schemas exist yet.

### Testing Requirements

- Add unit tests for model parse/serialize round trip using small inline dicts.
- Assert Pydantic `ValidationError.errors()` locations contain the relevant field paths, e.g. `("targets", 0, "coordinate")` or equivalent local structure.
- Assert invalid coordinate length/range and non-positive scale fail.
- Assert invalid enum values fail.
- Assert composition status defaults match PRD.
- Run existing tests to keep Story 1.1 guardrails green.

### Project Structure Notes

- `models/` is the shared contract layer for config/workspace/validation/render/export.
- UI code under `editor/` may import these models later; models must never import UI code.
- Later services should import these models instead of redefining dataclasses or untyped dictionaries.

### References

- [Epics: Story 1.2] `_bmad-output/planning-artifacts/epics.md`
- [Architecture: Ownership rules and source layout] `_bmad-output/planning-artifacts/architecture.md`
- [Architecture: Issue format and service result patterns] `_bmad-output/planning-artifacts/architecture.md`
- [Architecture: Scale semantics] `_bmad-output/planning-artifacts/architecture.md`
- [PRD: Glossary and FR1/FR4/FR6/FR8/FR17/FR20] `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md`
- [UX: Review/Edit status, validation and issue surfacing] `_bmad-output/planning-artifacts/ux-design-specification.md`
- [Previous story] `_bmad-output/implementation-artifacts/1-1-initialize-application-scaffold-and-quality-tooling.md`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` passed: 15 tests collected, 15 passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` passed: all checks passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay` passed and printed the minimal scaffold message.
- 2026-05-25: Code review found two model-contract tightening patches; both were applied.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` passed: 17 tests collected, 17 passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` passed: all checks passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay` passed and printed the minimal scaffold message.

### Completion Notes List

- Added Pydantic v2 models for config targets/grid/export refs, workspace manifest, composition/view/status/validation summary, image layers, template metadata, issues, render results, and export logs.
- Added public exports from `thucthengay.models` while keeping the package free of PySide6/editor imports.
- Added unit coverage for model round trips, invalid field locations, coordinate/scale/grid validation, enum validation, template required fields, and composition status defaults.
- Review patch: `Issue` now normalizes all `severity=error` instances to `blocking=True`.
- Review patch: `RenderResult.center` now validates lon/lat range consistently with `ViewState.center`.

### File List

- `_bmad-output/implementation-artifacts/1-2-define-core-pydantic-models.md`
- `_bmad-output/implementation-artifacts/1-2-define-core-pydantic-models.validation-report.md`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/models/config.py`
- `src/thucthengay/models/workspace.py`
- `src/thucthengay/models/composition.py`
- `src/thucthengay/models/layer.py`
- `src/thucthengay/models/template.py`
- `src/thucthengay/models/issue.py`
- `src/thucthengay/models/render.py`
- `src/thucthengay/models/export.py`
- `tests/unit/test_models.py`

### Change Log

- 2026-05-25: Addressed code review findings and completed Story 1.2.
- 2026-05-25: Implemented Story 1.2 core Pydantic models and unit coverage.
- 2026-05-25: Created Story 1.2 with model scope, architecture constraints, tests, and previous-story learnings.
