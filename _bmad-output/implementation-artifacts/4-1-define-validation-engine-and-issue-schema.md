# Story 4.1: Define Validation Engine and Issue Schema

Status: done

<!-- Note: Created from Epic 4 backlog context and started immediately per project autonomous execution mandate. -->

## Story

As an Operator,
I want validation results to be structured and actionable,
so that every warning or error clearly explains what is wrong and how to fix it.

## Acceptance Criteria

1. Given validation detects a problem in project, target, composition, or layer data, when an issue is created, then it includes `issue_id`, `severity`, `scope`, target/composition/layer references where applicable, Vietnamese message, Vietnamese remediation, and `blocking`, and `severity=error` maps to blocking behavior unless explicitly modeled otherwise.
2. Given an issue is serialized or passed to UI components, when it is consumed by tree, layer, warning panel, or export preflight, then the same issue schema is used across modules, and UI components do not invent independent issue shapes.
3. Given validation logic runs in core services, when tests instantiate the validation service, then the service can run without Qt widget dependencies, and fixtures can assert issue IDs, severity, blocking flag, and Vietnamese remediation text.
4. Given multiple issues are produced for one composition, when a validation summary is computed, then it includes aggregate warning/error counts and blocking status, and the detailed issue list can be recomputed later from current state.

## Tasks / Subtasks

- [x] Extend shared validation contracts (AC: 1, 2, 4)
  - [x] Keep `Issue` as the single shared schema in `models/issue.py`.
  - [x] Add a core validation result/gate contract that carries `Issue` details and compact summary state.
  - [x] Ensure error severity maps to blocking, while non-error severities only block when explicitly set.
- [x] Add validation service shell without Qt dependencies (AC: 2, 3, 4)
  - [x] Implement a `validation` service module that accepts rule callables and returns stable validation results.
  - [x] Provide helper aggregation from detailed issues to `ValidationSummary` and blocking status.
  - [x] Export the service/contract through `thucthengay.validation`.
- [x] Add focused tests (AC: 1-4)
  - [x] Test issue serialization and blocking semantics.
  - [x] Test validation result aggregation for info/warning/error counts and blocking status.
  - [x] Test validation service runs without Qt imports and recomputes detailed issues from current composition state.

### Review Findings

- [x] [Review][Patch] Normalize `ValidationResult.summary` and `blocking` for direct model construction, not only `from_issues()` [`src/thucthengay/validation/service.py`]

## Dev Notes

- Follow `_bmad-output/project-context.md` before implementation.
- Owner modules:
  - `models/issue.py`: shared `Issue`, `IssueSeverity`, and `IssueScope` only; keep persisted JSON schema strict.
  - `models/composition.py`: existing `ValidationSummary` is the compact persisted summary; avoid duplicating it.
  - `validation/`: core validation service and rule contract; must not import PySide6 or `editor`.
  - `editor/`: may consume `Issue`/validation result later, but this story should not build full UI warnings.
- Existing baseline:
  - `Issue` already exists with `issue_id`, `severity`, `scope`, target/composition/layer refs, Vietnamese message/remediation, and `blocking`.
  - `ValidationSummary` already persists compact counts on `Composition`.
  - Story 3.7 added a temporary `ReviewGateResult` inside `ReviewEditMode`; Epic 4 should move shared validation contracts into `validation/` so UI does not invent future issue shapes.
- Scope guard:
  - Do not implement Story 4.2 readiness rules beyond minimal test rules needed to prove the engine contract.
  - Do not mutate workspace from validation service.
  - Do not add new dependencies.
  - Core validation must import models/services only as needed and must run without Qt widget dependencies.
- Previous story learnings from 3.7:
  - Stale summaries are compact persisted state, not detailed issues; detailed issues must be recomputable from current state.
  - Include/ready transitions remain owned by `WorkspaceService`; validation only returns issues and summary/gate information.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.1]
- [Source: _bmad-output/planning-artifacts/architecture.md#Issue format]
- [Source: _bmad-output/planning-artifacts/architecture.md#Validation boundary]
- [Source: _bmad-output/implementation-artifacts/3-7-implement-review-action-bar-and-keyboard-workflow.md]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `conda run -n ttn-env pytest tests/unit/test_validation_service.py tests/unit/test_review_edit_mode.py` - 25 passed.
- `conda run -n ttn-env pytest tests/unit/test_models.py` - 13 passed.
- `conda run -n ttn-env pytest` - 110 passed.
- `$env:PYTHONIOENCODING='utf-8'; conda run -n ttn-env ruff check .` - all checks passed.
- `$env:PYTHONPATH='src'; conda run -n ttn-env python -m thucthengay --smoke` - app ready.
- Review found and resolved inconsistent direct `ValidationResult(...)` aggregate state.

### Completion Notes List

- Added `ValidationContext`, `ValidationResult`, `ValidationRule`, `ValidationService`, and `summarize_issues` in the core `validation` package.
- Preserved `Issue` as the single shared issue schema and used `ValidationSummary` as the compact persisted summary.
- Replaced Story 3.7's local review gate dataclass with shared `ValidationResult`.
- Added focused unit tests for aggregation, blocking semantics, Vietnamese remediation text, and rule recomputation without Qt dependencies.
- Resolved review finding by deriving `ValidationResult.summary` and `blocking` from `issues` for every construction path.

### File List

- `_bmad-output/implementation-artifacts/4-1-define-validation-engine-and-issue-schema.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/editor/modes/review_edit_mode.py`
- `src/thucthengay/validation/__init__.py`
- `src/thucthengay/validation/service.py`
- `tests/unit/test_validation_service.py`

## Change Log

- 2026-05-25: Created story context from Epic 4 backlog.
- 2026-05-25: Implemented validation service contract, aggregation helpers, shared review gate result, and focused tests; marked ready for review.
- 2026-05-25: Resolved code review finding for aggregate normalization.
