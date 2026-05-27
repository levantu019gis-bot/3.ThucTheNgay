"""Export summary and log models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from thucthengay.models.issue import Issue, IssueSeverity


class ExportedComposition(BaseModel):
    """Composition successfully written to report outputs."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    slide_number: int = Field(ge=1)
    render_path: str


class SkippedComposition(BaseModel):
    """Composition omitted from export."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    reason: str


class ExportCompletionState(StrEnum):
    """Final export completion state consumed by Export mode UI."""

    SUCCESS = "success"
    SUCCESS_WITH_WARNINGS = "success_with_warnings"
    FAILURE = "failure"


class ExportTraceStatus(StrEnum):
    """Per-composition trace status in the export log."""

    EXPORTED = "exported"
    SKIPPED = "skipped"
    FAILED = "failed"


class ExportTraceEntry(BaseModel):
    """Trace one composition across PPTX and TXT outputs."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    status: ExportTraceStatus
    pptx_slide_number: int | None = Field(default=None, ge=1)
    txt_line_number: int | None = Field(default=None, ge=1)
    skipped_reason: str | None = None


class ExportIssueSummary(BaseModel):
    """Grouped issue count written into the export log."""

    model_config = ConfigDict(extra="forbid")

    issue_id: str
    severity: IssueSeverity
    count: int = Field(ge=1)


class ExportCompletionSummary(BaseModel):
    """Summary metrics and artifact paths for a completed export attempt."""

    model_config = ConfigDict(extra="forbid")

    state: ExportCompletionState
    slide_count: int = Field(default=0, ge=0)
    txt_line_count: int = Field(default=0, ge=0)
    target_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    pptx_path: str | None = None
    txt_path: str | None = None
    log_path: str | None = None


class ExportLog(BaseModel):
    """Traceable export result for PPTX/TXT output."""

    model_config = ConfigDict(extra="forbid")

    pptx_path: str | None = None
    txt_path: str | None = None
    log_path: str | None = None
    slide_count: int = Field(default=0, ge=0)
    txt_line_count: int = Field(default=0, ge=0)
    target_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    exported: list[ExportedComposition] = Field(default_factory=list)
    skipped: list[SkippedComposition] = Field(default_factory=list)
    entries: list[ExportTraceEntry] = Field(default_factory=list)
    issue_summary: list[ExportIssueSummary] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)


class ExportLogWriteResult(BaseModel):
    """Result returned after writing export summary and trace log."""

    model_config = ConfigDict(extra="forbid")

    ok: bool = False
    summary: ExportCompletionSummary
    log: ExportLog | None = None
    issues: list[Issue] = Field(default_factory=list)


class ExportPreflightState(StrEnum):
    """Export preflight state shown in Export mode."""

    NOT_RUN = "not_run"
    RUNNING = "running"
    READY = "ready"
    BLOCKED = "blocked"
    WARNING = "warning"


class ExportFinalRenderStatus(StrEnum):
    """Per-composition state after export final-render preparation."""

    CURRENT = "current"
    RENDERED = "rendered"
    FAILED = "failed"
    SKIPPED = "skipped"


class ExportPlanRow(BaseModel):
    """One included composition row in the export plan."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    slide_number: int | None = Field(default=None, ge=1)
    review_order: int | None = Field(default=None, ge=1)
    target_label: str
    date_label: str
    time_label: str
    template_status: str
    final_render_path: str | None = None
    issues: list[Issue] = Field(default_factory=list)

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    @property
    def blocking(self) -> bool:
        return any(issue.blocking for issue in self.issues)


class ExportPreflightSummary(BaseModel):
    """Aggregate metrics for the Export mode dashboard."""

    model_config = ConfigDict(extra="forbid")

    included_slide_count: int = Field(default=0, ge=0)
    target_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    state: ExportPreflightState = ExportPreflightState.NOT_RUN


class ExportPreflightPlan(BaseModel):
    """Headless export preflight result consumed by UI and future exporters."""

    model_config = ConfigDict(extra="forbid")

    rows: list[ExportPlanRow] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
    summary: ExportPreflightSummary = Field(default_factory=ExportPreflightSummary)


class ExportFinalRenderRow(BaseModel):
    """Final-render preparation result for one included composition."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    review_order: int | None = Field(default=None, ge=1)
    status: ExportFinalRenderStatus
    final_render_path: str | None = None
    render_log_path: str | None = None
    render_spec_hash: str | None = None
    issues: list[Issue] = Field(default_factory=list)

    @property
    def ready(self) -> bool:
        return self.status in {
            ExportFinalRenderStatus.CURRENT,
            ExportFinalRenderStatus.RENDERED,
        }


class ExportFinalRenderSummary(BaseModel):
    """Aggregate export final-render preparation metrics."""

    model_config = ConfigDict(extra="forbid")

    included_count: int = Field(default=0, ge=0)
    current_count: int = Field(default=0, ge=0)
    rendered_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)

    @property
    def ready_count(self) -> int:
        return self.current_count + self.rendered_count


class ExportFinalRenderResult(BaseModel):
    """Headless result returned before PPTX export consumes final PNG paths."""

    model_config = ConfigDict(extra="forbid")

    rows: list[ExportFinalRenderRow] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
    summary: ExportFinalRenderSummary = Field(default_factory=ExportFinalRenderSummary)


class ExportPptxSummary(BaseModel):
    """Aggregate metrics for a combined PPTX export run."""

    model_config = ConfigDict(extra="forbid")

    slide_count: int = Field(default=0, ge=0)
    target_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)


class ExportPptxResult(BaseModel):
    """Result returned by the headless combined PPTX exporter."""

    model_config = ConfigDict(extra="forbid")

    ok: bool = False
    pptx_path: str | None = None
    exported: list[ExportedComposition] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
    summary: ExportPptxSummary = Field(default_factory=ExportPptxSummary)


class ExportedTxtLine(BaseModel):
    """Composition successfully written to one TXT report line."""

    model_config = ConfigDict(extra="forbid")

    composition_id: str
    target_id: str
    line_number: int = Field(ge=1)
    text: str


class ExportTxtSummary(BaseModel):
    """Aggregate metrics for a TXT export run."""

    model_config = ConfigDict(extra="forbid")

    line_count: int = Field(default=0, ge=0)
    target_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)


class ExportTxtResult(BaseModel):
    """Result returned by the headless TXT exporter."""

    model_config = ConfigDict(extra="forbid")

    ok: bool = False
    txt_path: str | None = None
    exported: list[ExportedTxtLine] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
    summary: ExportTxtSummary = Field(default_factory=ExportTxtSummary)
