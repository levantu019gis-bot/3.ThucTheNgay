# Session Handoff - 3.ThucTheNgay

Date: 2026-05-24
Status: Planning artifacts in progress; epics and stories completed, final epics validation not yet run.

## Project Summary

3.ThucTheNgay is a desktop Python/PySide6 application for generating PPTX and TXT reports from optical satellite GeoTIFF imagery.

Core workflow:
1. Setup: load project config, select imagery input folder and workspace folder.
2. Ingest: scan GeoTIFFs, extract metadata, match imagery to target GeoJSON boundaries, copy matches into workspace cache, create one composition per target-date.
3. Review/Edit: inspect each composition, manage layers, pan/zoom target-centered map view, edit grid/metadata, validate, include/skip.
4. Export: preflight included compositions, render final PNG maps, export one combined PPTX plus TXT report, write summary/log.

Important product decision: each target has its own PowerPoint template metadata and template reference in config. Export still produces one combined PPTX; target templates must be compatible enough for slide-copy/export.

## Key Architecture Decisions

- Desktop app: PySide6 Qt Widgets.
- Project scaffold: custom Python package via `uv init --app`.
- Layered package modules: `models`, `config`, `workspace`, `ingestion`, `gis`, `render`, `validation`, `export`, `jobs`, `editor`, `utils`.
- Pydantic models for config, workspace, composition, layer, template metadata, issue, render result, export log.
- Workspace JSON is source of truth; only `WorkspaceService` reads/writes workspace JSON.
- JSON writes must be atomic using temp file and replace.
- Core services must not depend on Qt widgets.
- Long-running ingestion/render/export use job/progress model and safe Qt main-thread updates.
- GIS uses rasterio/GDAL, shapely, pyproj. Target config stores a geographic target coordinate plus scale denominator; composition view stores center `[lon, lat]` plus scale, and render derives the geographic/raster read window from that state.
- Renderer uses shared render spec for preview/final alignment.
- Export isolates risky PPTX slide copy in `export/pptx_slide_copy.py`.

## Project Data Layout Decision

User project data lives outside app source tree:

```text
project_data/
  config.json
  targets/
    target_001.geojson
    target_002.geojson
  templates/
    target_001.pptx
    target_001.template.json
    target_002.pptx
    target_002.template.json
  imagery/
    raw_geotiff_files/
  workspace/
    manifest.json
    cache/
    compositions/
    renders/
    exports/
```

Rules:
- `config.json` is selected in Setup.
- `targets/*.geojson` is referenced by `config.json` via `geojson_file`.
- Each target has `template_metadata_file` in config.
- Template metadata references its own `template_pptx` and resolves paths relative to the metadata file.
- Config paths resolve relative to config file.
- Workspace stores runtime state and should prefer workspace-relative paths where possible.
- `imagery/` is read-only source data.
- Existing workspace/cache clear requires explicit confirmation.

## Important GeoTIFF Metadata Decision

For ingestion Story 2.1:
- If filename or sidecar metadata is available, parse capture date/time, cloud percent, and source identifiers from it.
- If no usable sidecar metadata exists, use `rasterio` to read CRS, bounds/transform, width/height, band count, nodata, and embedded tags directly from the GeoTIFF.
- If capture date/time or cloud percent cannot be derived, mark metadata as needing manual correction and create a warning; do not fail the whole ingestion run if a valid footprint exists.

## Artifacts Created

Brainstorming source:
- `_bmad-output/brainstorming/brainstorming-session-2026-05-23-163752.md`

Product brief:
- `_bmad-output/planning-artifacts/briefs/brief-3.ThucTheNgay-2026-05-23/brief.md`
- `_bmad-output/planning-artifacts/briefs/brief-3.ThucTheNgay-2026-05-23/addendum.md`
- `_bmad-output/planning-artifacts/briefs/brief-3.ThucTheNgay-2026-05-23/.decision-log.md`

PRD:
- `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md`
- `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/addendum.md`
- `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/.decision-log.md`
- `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/review-rubric.md`
- `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/validation-report.md`
- `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/validation-report.html`

UX specification:
- `_bmad-output/planning-artifacts/ux-design-specification.md`
- `_bmad-output/planning-artifacts/ux-design-directions.html`

Architecture:
- `_bmad-output/planning-artifacts/architecture.md`
- Architecture validation result: READY FOR IMPLEMENTATION.

Epics and stories:
- `_bmad-output/planning-artifacts/epics.md`
- Current frontmatter: `stepsCompleted: [1, 2, 3]`.
- Contains 6 epics and 38 stories.
- No placeholders remain.
- FR1-FR23 and UX-DR1-UX-DR16 are represented.

## Epics Summary

Epic 1: Project Setup, Schemas, and Workspace Foundation
- 7 stories: scaffold/tooling, Pydantic models, config loading, Setup path UI, workspace service, composition status, validation summary/revalidation state.

Epic 2: Data Ingestion to Composition Workspace
- 6 stories: scan/extract GeoTIFF metadata, match to targets, cache matched imagery, create target-date compositions, ingestion progress job, ingestion summary/warnings.

Epic 3: Review/Edit Workstation Core
- 7 stories: Review/Edit layout/tree, queue filters, layer stack, GIS editor pan/zoom, grid override, slide preview, review action bar/keyboard workflow.

Epic 4: Validation, Warnings, and Metadata Correction
- 6 stories: validation engine/schema, readiness rules, validation timing, issue UI/navigation, metadata editor, confirmed cache move/regroup when date changes.

Epic 5: Rendering Pipeline and Map Output Fidelity
- 6 stories: shared render spec, raster window/CRS transform core, grid/background rendering, two-stage preview jobs, final PNG/render log, preview/final fixture tests.

Epic 6: Report Export and Completion Evidence
- 6 stories: target-specific PPTX metadata, export preflight/plan UI, final renders for included compositions, combined PPTX export, TXT export, summary/trace log.

## Current Workflow State

The active BMad workflow is `bmad-create-epics-and-stories`.

Completed:
- Step 1: Validate prerequisites and collect requirements inventory.
- Step 2: Design and approve epics.
- Step 3: Generate stories for all epics.

Not completed yet:
- Step 4: Final validation of epics/stories.

The previous assistant had just presented the Step 3 final menu:
`[A] Advanced Elicitation [P] Party Mode [C] Continue`

User ended the session before choosing. In the next session, continue with `[C]` equivalent: read and follow:
- `.agents/skills/bmad-create-epics-and-stories/steps/step-04-final-validation.md`

Expected next action:
1. Open the `bmad-create-epics-and-stories` skill instructions if needed.
2. Read Step 4 final validation file completely.
3. Validate `epics.md` against the required structure and coverage.
4. Fix any formatting/order/coverage issues in `epics.md`.
5. Update frontmatter to include Step 4 when validation passes.
6. Present the next BMad menu or recommendation.

## Notes For Next Session

- User prefers continuing workflow with short confirmations like `[C]`.
- Communicate in Vietnamese.
- Be concise and pragmatic.
- Do not restart discovery from scratch; use this handoff plus the artifacts above.
- The file `_bmad-output/planning-artifacts/epics.md` currently has the Epic List section first, followed by detailed `## Epic N` sections appended later. Step 4 may require checking whether this exact ordering satisfies the template.
- If editing files via shell is needed, sandbox may require escalated execution. Previous session used escalated `python3` writes because sandboxed commands failed.
