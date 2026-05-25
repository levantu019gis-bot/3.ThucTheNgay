"""Core validation service contracts."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, model_validator

from thucthengay.models import (
    Composition,
    Issue,
    IssueSeverity,
    ProjectConfig,
    TargetConfig,
    TemplateMetadata,
    ValidationSummary,
)


@dataclass(frozen=True)
class ValidationContext:
    """Input context available to validation rules."""

    project_config: ProjectConfig | None = None
    target: TargetConfig | None = None
    composition: Composition | None = None
    template_metadata: TemplateMetadata | None = None
    template_metadata_error: str | None = None
    require_current_validation: bool = False


ValidationRule = Callable[[ValidationContext], Iterable[Issue]]


class ValidationResult(BaseModel):
    """Detailed issues plus compact summary returned by validation."""

    model_config = ConfigDict(extra="forbid")

    issues: tuple[Issue, ...] = Field(default_factory=tuple)
    summary: ValidationSummary = Field(default_factory=ValidationSummary)
    blocking: bool = False

    @property
    def passed(self) -> bool:
        """Return True when no blocking issue prevents the workflow."""
        return not self.blocking

    @model_validator(mode="after")
    def normalize_aggregates(self) -> ValidationResult:
        """Keep summary and blocking status derived from detailed issues."""
        self.summary = summarize_issues(self.issues)
        self.blocking = any(issue.blocking for issue in self.issues)
        return self

    @classmethod
    def from_issues(cls, issues: Iterable[Issue]) -> ValidationResult:
        return cls(issues=tuple(issues))


def summarize_issues(issues: Iterable[Issue]) -> ValidationSummary:
    """Aggregate detailed issues into persisted validation counts."""
    info_count = 0
    warning_count = 0
    error_count = 0

    for issue in issues:
        if issue.severity == IssueSeverity.INFO:
            info_count += 1
        elif issue.severity == IssueSeverity.WARNING:
            warning_count += 1
        elif issue.severity == IssueSeverity.ERROR:
            error_count += 1

    return ValidationSummary(
        info_count=info_count,
        warning_count=warning_count,
        error_count=error_count,
    )


class ValidationService:
    """Run core validation rules without mutating workspace state."""

    def __init__(self, rules: Iterable[ValidationRule] = ()) -> None:
        self._rules = tuple(rules)

    def validate(self, context: ValidationContext) -> ValidationResult:
        issues: list[Issue] = []
        for rule in self._rules:
            issues.extend(rule(context))
        return ValidationResult.from_issues(issues)
