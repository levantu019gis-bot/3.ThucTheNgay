"""Export preflight validation helpers."""

from __future__ import annotations

from collections.abc import Iterable

from thucthengay.models import Issue
from thucthengay.validation.composition_rules import validate_composition_readiness
from thucthengay.validation.service import ValidationContext, ValidationResult


def validate_export_preflight(
    contexts: Iterable[ValidationContext],
    template_issues: Iterable[Issue] = (),
) -> ValidationResult:
    """Recompute readiness validation for export candidate contexts."""
    issues: list[Issue] = list(template_issues)
    for context in contexts:
        issues.extend(validate_composition_readiness(context).issues)
    return ValidationResult.from_issues(issues)
