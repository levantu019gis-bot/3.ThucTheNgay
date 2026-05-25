# Story 4.2: Validate Composition Readiness Rules

Status: done

<!-- Note: Created from Epic 4 backlog context and started immediately per project autonomous execution mandate. -->

## Story

As an Operator,
I want the app to check whether a composition is actually ready,
so that invalid slides cannot be marked ready or exported by accident.

## Acceptance Criteria

1. Given a composition has no visible layers, when readiness validation runs, then it produces a blocking error tied to the composition/layer stack, and the remediation tells the Operator to enable at least one valid layer.
2. Given visible layers cannot produce a valid time label because required capture date/time is missing or invalid, when readiness validation runs, then it produces a blocking error tied to the affected layer(s), and the remediation points to metadata correction.
3. Given grid override, view center/scale, or map frame settings are invalid, when readiness validation runs, then it produces blocking issues where the invalid state would affect render/export correctness, and the issue references the composition and field area where the fix is needed.
4. Given target-specific template metadata is missing or invalid for the composition target, when readiness or export validation checks template readiness, then it produces a blocking error, and the issue explains that the target template metadata or PPTX reference must be fixed.
5. Given a composition has `needs_revalidation=true`, when readiness status is evaluated, then the app does not treat previous validation summary as proof of readiness, and revalidation is required before ready/include/export decisions.

## Tasks / Subtasks

- [x] Add composition readiness rule module (AC: 1-5)
  - [x] Validate visible layer presence.
  - [x] Validate visible layer capture date/time and metadata correction state.
  - [x] Validate view center/scale and grid override values defensively.
  - [x] Validate target/template metadata context and map frame shape.
  - [x] Flag stale `needs_revalidation` as blocking for readiness decisions.
- [x] Wire readiness rules into validation service contract (AC: 1-5)
  - [x] Extend `ValidationContext` only as needed for template metadata inputs.
  - [x] Provide a public helper for composition readiness validation.
  - [x] Export readiness helper/rule through `thucthengay.validation`.
- [x] Add focused tests (AC: 1-5)
  - [x] Test each blocking readiness issue and Vietnamese remediation text.
  - [x] Test passing composition readiness returns no blocking issues.
  - [x] Test invalid/stale persisted summary cannot prove readiness while `needs_revalidation=true`.

### Review Findings

- [x] [Review][Patch] Avoid a stale-validation deadlock by making `needs_revalidation` blocking only for persisted-readiness evaluation, not default recompute validation [`src/thucthengay/validation/composition_rules.py`]

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `validation/composition_rules.py`: readiness rule functions only; no Qt, no workspace mutation.
  - `validation/service.py`: shared context/result contract; may add template metadata fields.
  - `models/*`: do not duplicate schemas; use existing `Composition`, `ImageLayer`, `TargetConfig`, `TemplateMetadata`, and `Issue`.
- Scope guard:
  - Do not wire selection/include/export timing yet; Story 4.3 owns when validation runs and persistence.
  - Do not implement metadata editor or correction workflow; Story 4.5 owns that UI.
  - Do not load template files from disk in this story. Accept parsed `TemplateMetadata` or explicit template metadata error in context so future callers own file loading.
  - Validation service must return `Issue` objects and compact summary only; it must not write workspace state.
- Previous story learnings from 4.1:
  - `ValidationResult.summary` and `blocking` are derived from detailed issues for every construction path.
  - Detailed issues are recomputed from current context; persisted `ValidationSummary` is not a source of truth when `needs_revalidation=true`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.2]
- [Source: _bmad-output/planning-artifacts/architecture.md#Validation boundary]
- [Source: _bmad-output/planning-artifacts/architecture.md#Review status transitions]
- [Source: _bmad-output/implementation-artifacts/4-1-define-validation-engine-and-issue-schema.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests/unit/test_composition_readiness_validation.py tests/unit/test_validation_service.py` - 15 passed.
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check src/thucthengay/validation tests/unit/test_composition_readiness_validation.py` - all checks passed.
- `conda run -n ttn-env pytest` - 121 passed.
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - all checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.
- Review found and resolved stale-validation deadlock risk before marking done.

### Completion Notes List

- Added composition readiness validation rules for visible layers, layer timestamp/metadata status, view/grid state, template metadata/map frame, and stale revalidation state.
- Extended `ValidationContext` with parsed template metadata and template metadata error fields so validation stays pure and file loading remains outside the rule layer.
- Exported readiness helpers through `thucthengay.validation`.
- Added focused unit tests for passing and blocking readiness scenarios.
- Resolved review finding by adding `ValidationContext.require_current_validation`; recompute validation can pass stale compositions so Story 4.3 can save a fresh summary, while persisted-readiness evaluation still blocks stale state.

### File List

- `_bmad-output/implementation-artifacts/4-2-validate-composition-readiness-rules.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/validation/__init__.py`
- `src/thucthengay/validation/composition_rules.py`
- `src/thucthengay/validation/service.py`
- `tests/unit/test_composition_readiness_validation.py`

## Change Log

- 2026-05-25: Created story context from Epic 4 backlog and started implementation.
- 2026-05-25: Implemented composition readiness rules and focused tests; marked ready for review.
- 2026-05-25: Resolved code review finding for stale persisted-readiness gating.
