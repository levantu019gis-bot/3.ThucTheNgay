"""Shared validation and workflow issue contracts."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, model_validator


class IssueSeverity(StrEnum):
    """Severity levels shown in validation, UI indicators, and export logs."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class IssueScope(StrEnum):
    """Domain object an issue belongs to."""

    PROJECT = "project"
    CONFIG = "config"
    TARGET = "target"
    WORKSPACE = "workspace"
    COMPOSITION = "composition"
    LAYER = "layer"
    TEMPLATE = "template"
    RENDER = "render"
    EXPORT = "export"


class Issue(BaseModel):
    """User-facing issue returned by validation and workflow services."""

    model_config = ConfigDict(extra="forbid")

    issue_id: str
    severity: IssueSeverity
    scope: IssueScope
    target_id: str | None = None
    composition_id: str | None = None
    layer_id: str | None = None
    message: str
    remediation: str | None = None
    blocking: bool = False

    @model_validator(mode="after")
    def error_issues_are_blocking(self) -> Issue:
        if self.severity == IssueSeverity.ERROR:
            self.blocking = True
        return self
