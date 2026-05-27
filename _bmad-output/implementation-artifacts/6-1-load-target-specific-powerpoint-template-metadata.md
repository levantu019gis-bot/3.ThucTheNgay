# Story 6.1: Load Target-Specific One-Slide PowerPoint Templates

Status: done

## Story

As an Operator,
I want each target to point directly to its own one-slide PowerPoint template,
So that report slides can follow target-specific layout rules and replace known PPTX elements by id while still exporting into one combined PPTX.

## Acceptance Criteria

1. Given a target config references a `template_pptx_file`, when export preparation loads the target, then it resolves the target-specific PPTX path relative to the config file, validates the PPTX contains exactly one template slide, and loads the configured PPTX element-id mapping for map frame and text/image placeholders from target export config.
2. Given target export config maps report fields to PowerPoint element ids, when placeholders are resolved, then element id lookup is the primary replacement mechanism and shape names may be recorded only as diagnostics for human troubleshooting.
3. Given the referenced PPTX is missing, has zero slides, has more than one slide, or lacks a required element id, when preflight validates the target, then it creates a blocking issue tied to the target/composition using that template and the Vietnamese remediation explains which PPTX path or element-id mapping must be fixed.
4. Given multiple targets use different template files, when export preflight checks compatibility, then it verifies the templates satisfy the documented compatible base/theme/master assumption where the implementation can detect it, and incompatibility or unknown compatibility is surfaced before export rather than failing silently during slide copy.

## Tasks / Subtasks

- [x] Update target export config schema for direct PPTX templates (AC: 1, 2)
  - [x] Replace `export.template_metadata_file` with `export.template_pptx_file` in persisted config models and examples.
  - [x] Add element-id based placeholder mapping fields for map image/text/image placeholders.
  - [x] Keep shape names diagnostic-only in model naming and validation behavior.
- [x] Load and validate one-slide PPTX templates from config (AC: 1, 3)
  - [x] Resolve `template_pptx_file` relative to the selected config file.
  - [x] Validate missing file and invalid PPTX as blocking target issues with Vietnamese remediation.
  - [x] Validate exactly one slide.
  - [x] Extract PPTX element ids from that single slide and verify required mappings exist.
- [x] Provide export-template metadata for downstream render/export code (AC: 1, 2)
  - [x] Derive map frame bounds from the configured map image element id.
  - [x] Preserve existing render/validation contracts where practical by adapting template metadata at load time.
  - [x] Ensure element id, not shape name, is the authoritative lookup key.
- [x] Surface template compatibility checks for multi-template preflight (AC: 4)
  - [x] Add a headless compatibility helper that can group/check loaded templates without UI imports.
  - [x] Return warnings/errors as shared `Issue` objects.
- [x] Update tests, examples, real-data config generation, and gates (AC: 1, 2, 3, 4)
  - [x] Update unit tests for config models/service and composition readiness.
  - [x] Add PPTX fixture tests using generated temporary PPTX files.
  - [x] Update `scripts/generate_config_from_geojson.py`, `examples/config.example.json`, and root `config.json`.
  - [x] Run focused tests, full `pytest`, `ruff check .`, and app smoke.

### Review Findings

- [x] [Review][Patch] Catch invalid derived map frame dimensions as structured template issues [`src/thucthengay/export/template_loader.py:94`]
- [x] [Review][Patch] Propagate derived PPTX template metadata into downstream validation contexts [`src/thucthengay/config/service.py:173`]
- [x] [Review][Patch] Run or surface multi-template compatibility checks from export preflight, not only config load [`src/thucthengay/validation/export_preflight.py:12`]
- [x] [Review][Patch] Surface unknown multi-template compatibility even when detectable signatures match [`src/thucthengay/export/template_loader.py:123`]
- [x] [Review][Patch] Reject duplicate placeholder element mappings before downstream replacement becomes ambiguous [`src/thucthengay/export/template_loader.py:82`]
- [x] [Review][Patch] Reject multiple required map image placeholders instead of silently using the first [`src/thucthengay/export/template_loader.py:170`]
- [x] [Review][Defer] Disabled target filtering treats string `"false"` as enabled before Pydantic coercion [`src/thucthengay/config/service.py:126`] — deferred, pre-existing

## Dev Notes

- Owner modules:
  - `models/` owns persisted config schema and shared template metadata/result models.
  - `config/` owns config-relative path resolution and target reference validation.
  - `export/` should own PPTX template loading/compatibility helpers; it must not import UI.
  - `validation/` returns shared `Issue` objects and does not mutate workspace.
- Epic 6 planning change supersedes the old template metadata JSON runtime path. Runtime config must point directly to a one-slide PPTX via `target.export.template_pptx_file`.
- PPTX element id means the PowerPoint shape id exposed by `python-pptx` as `shape.shape_id` / cNvPr id. Shape names may be captured in diagnostics but must not be used as fallback lookup keys.
- For Story 6.1, deriving `TemplateMetadata` from the PPTX is acceptable so Epic 5 render code can continue to receive a `map_frame`; do not require a separate metadata JSON at runtime.
- Scope boundary: do not implement combined PPTX slide copy or placeholder replacement in this story. Those belong to Story 6.4.
- Use `python-pptx>=1.0`; no new dependency is needed.
- Tests should generate small temporary PPTX files; they must not require real operator PPTX files.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.1]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md#FR-20]
- [Source: _bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/addendum.md#Template and Export Direction]
- [Source: _bmad-output/planning-artifacts/architecture.md#User Project Data Layout]
- [Source: _bmad-output/project-context.md#Module Ownership Rules]
- [Source: _bmad-output/implementation-artifacts/5-6-verify-preview-final-alignment-with-fixtures.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `$env:PYTHONPATH='src'; conda run -n ttn-env pytest tests\unit\test_models.py tests\unit\test_config_service.py -q` - passed (`22 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; $env:TEMP="$PWD\.tmp"; $env:TMP="$PWD\.tmp"; conda run -n ttn-env pytest -q` - passed (`249 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - passed.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest tests/unit/test_config_service.py tests/unit/test_composition_readiness_validation.py -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`24 passed`).
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - passed after review fixes.
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env pytest -q -p no:cacheprovider --basetemp=.tmp/pytest` - passed (`254 passed`).
- `$env:PYTHONPATH='src'; $env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env python -m thucthengay --smoke` - app ready after review fixes.

### Completion Notes List

- Added direct `export.template_pptx_file` config support with element-id placeholder mappings and compatibility accessors for the old field during migration.
- Added `export/template_loader.py` to load one-slide PPTX templates, derive map frame bounds from the configured map image element id, verify required element ids, and surface compatibility warnings.
- Updated config loading to resolve PPTX templates relative to `config.json` and expose derived `TemplateMetadata` for existing render/validation code.
- Regenerated root `config.json` for 70 real targets using `examples/templates/target_001.template.pptx` and map element id `1026`.
- Resolved code review findings by adding structured map-frame errors, duplicate/ambiguous placeholder guards, runtime propagation of derived template metadata, and export-preflight compatibility issue surfacing.

### File List

- `README.md`
- `_bmad-output/implementation-artifacts/6-1-load-target-specific-powerpoint-template-metadata.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `config.json`
- `examples/config.example.json`
- `examples/templates/target_001.template.json`
- `scripts/generate_config_from_geojson.py`
- `scripts/generate_template_metadata.py`
- `src/thucthengay/config/service.py`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/export/template_loader.py`
- `src/thucthengay/models/config.py`
- `src/thucthengay/models/template.py`
- `src/thucthengay/validation/composition_rules.py`
- `src/thucthengay/validation/export_preflight.py`
- `tests/unit/test_composition_readiness_validation.py`
- `tests/unit/test_config_service.py`
- `tests/unit/test_models.py`
- `tests/unit/test_review_edit_mode.py`

## Change Log

- 2026-05-26: Created Story 6.1 artifact and moved status to ready-for-dev.
- 2026-05-26: Started implementation and moved status to in-progress.
- 2026-05-26: Implemented direct one-slide PPTX template loading and moved status to review.
- 2026-05-26: Applied all code review patch findings, reran gates, and moved status to done.
