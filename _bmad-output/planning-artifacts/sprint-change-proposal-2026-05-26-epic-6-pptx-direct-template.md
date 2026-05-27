# Sprint Change Proposal: Epic 6 Direct PPTX Template Export

Date: 2026-05-26
Project: 3.ThucTheNgay
Scope: Moderate planning adjustment before Epic 6 starts

## 1. Issue Summary

Epic 6 originally assumed each target points to a separate template metadata JSON file, and that metadata points to a target-specific PPTX plus `slide_index`, map frame, and placeholder definitions.

The updated requirement is simpler and closer to the real data workflow:

- Each target in `config.json` points directly to its own PowerPoint template file.
- Each PowerPoint template contains exactly one slide.
- The application replaces map/text/image elements by known PPTX element ids.
- Shape names are optional diagnostics only, not the primary replacement key.

## 2. Impact Analysis

Epic impact:

- Epic 6 remains valid and keeps the same story count.
- Story 6.1 changes from loading template metadata JSON to loading direct one-slide PPTX templates and element-id mappings from target config.
- Stories 6.2 and 6.4 now validate/use element-id mappings instead of metadata placeholders.

Artifact impact:

- PRD FR-20/FR-21 updated to direct `export.template_pptx_file`.
- Architecture export flow updated to load one-slide PPTX templates and replace by element id.
- Epics/story acceptance criteria updated for Story 6.1, 6.2, and 6.4.
- Sprint status does not need story ID changes because Epic 6 has not started.

Technical impact:

- Config schema must replace or supersede `export.template_metadata_file` with `export.template_pptx_file`.
- Target export config needs a structured element-id mapping for map image and text/image placeholders.
- Export preflight must reject missing PPTX, zero/multiple-slide PPTX, and missing required element ids.
- Existing helper script that extracts PPTX metadata can still be useful for discovering ids, but generated metadata JSON is no longer the primary runtime contract.

## 3. Recommended Approach

Use direct adjustment within the existing Epic 6 plan.

Rationale:

- No completed Epic 6 story needs rollback.
- The change reduces runtime indirection and removes the need for a required metadata JSON file.
- The export implementation becomes more deterministic because element ids are authoritative.
- The main remaining design work is the target export mapping schema in Story 6.1.

## 4. Detailed Change Proposals

Story 6.1:

- Old: target config references `template_metadata_file`; metadata includes `template_pptx`, `slide_index`, map frame, placeholders.
- New: target config references `template_pptx_file`; the PPTX must have exactly one slide; target export config stores map/text/image replacement mappings by PPTX element id.

Story 6.2:

- Old: preflight validates target-specific template metadata.
- New: preflight validates target-specific PPTX templates and required element-id mappings.

Story 6.4:

- Old: exporter copies configured `slide_index`.
- New: exporter copies the only slide from each target PPTX and replaces elements by id.

## 5. Implementation Handoff

Next story remains Story 6.1.

Developer handoff:

- Define the new config model fields for direct PPTX template export.
- Decide the exact JSON shape for element-id mapping.
- Update config loading/validation and tests.
- Keep PPTX manipulation in `export/`; keep UI out of core export logic.

Success criteria:

- Enabled target config validates `export.template_pptx_file`.
- PPTX path resolves relative to `config.json`.
- Preflight can detect missing PPTX, zero/multiple-slide PPTX, and missing required element ids.
- Story 6.2/6.4 can consume the same resolved export template contract without reading raw config directly.
