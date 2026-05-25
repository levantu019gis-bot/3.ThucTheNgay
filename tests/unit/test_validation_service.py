from __future__ import annotations

from datetime import date

from thucthengay.models import (
    Composition,
    Issue,
    IssueScope,
    IssueSeverity,
    ValidationSummary,
    ViewState,
)
from thucthengay.validation import (
    ValidationContext,
    ValidationResult,
    ValidationService,
    summarize_issues,
)


def composition() -> Composition:
    return Composition(
        composition_id="alpha__20260525",
        target_id="alpha",
        capture_date=date(2026, 5, 25),
        view=ViewState(center=[106.7, 10.8], scale=50000),
    )


def test_validation_result_aggregates_issue_counts_and_blocking_status() -> None:
    result = ValidationResult.from_issues(
        [
            Issue(
                issue_id="composition.note",
                severity=IssueSeverity.INFO,
                scope=IssueScope.COMPOSITION,
                message="Ghi chú kiểm tra.",
                remediation="Không cần thao tác.",
            ),
            Issue(
                issue_id="layer.metadata_warning",
                severity=IssueSeverity.WARNING,
                scope=IssueScope.LAYER,
                message="Metadata layer cần kiểm tra.",
                remediation="Mở metadata editor để xác nhận lại.",
            ),
            Issue(
                issue_id="composition.no_visible_layer",
                severity=IssueSeverity.ERROR,
                scope=IssueScope.COMPOSITION,
                composition_id="alpha__20260525",
                message="Composition không có layer nào đang bật.",
                remediation="Bật ít nhất một layer hợp lệ.",
            ),
        ]
    )

    assert result.summary == ValidationSummary(info_count=1, warning_count=1, error_count=1)
    assert result.blocking is True
    assert result.passed is False
    assert result.issues[2].blocking is True


def test_warning_can_block_only_when_explicitly_modeled() -> None:
    issue = Issue(
        issue_id="template.placeholder_optional",
        severity=IssueSeverity.WARNING,
        scope=IssueScope.TEMPLATE,
        message="Placeholder tùy chọn chưa có dữ liệu.",
        remediation="Có thể bổ sung nếu cần.",
        blocking=True,
    )

    result = ValidationResult.from_issues([issue])

    assert result.summary.warning_count == 1
    assert result.summary.error_count == 0
    assert result.blocking is True


def test_validation_result_normalizes_direct_instantiation() -> None:
    result = ValidationResult(
        issues=(
            Issue(
                issue_id="composition.invalid",
                severity=IssueSeverity.ERROR,
                scope=IssueScope.COMPOSITION,
                message="Composition không hợp lệ.",
                remediation="Sửa lỗi composition rồi chạy lại validation.",
            ),
        )
    )

    assert result.summary.error_count == 1
    assert result.blocking is True
    assert result.passed is False


def test_summarize_issues_keeps_detailed_issues_recomputable() -> None:
    first_summary = summarize_issues(
        [
            Issue(
                issue_id="composition.stale",
                severity=IssueSeverity.WARNING,
                scope=IssueScope.COMPOSITION,
                message="Composition cần revalidate.",
                remediation="Chạy Revalidate trước khi Include.",
            )
        ]
    )
    clean_summary = summarize_issues([])

    assert first_summary.warning_count == 1
    assert clean_summary == ValidationSummary()


def test_validation_service_runs_rule_callables_without_qt_dependencies() -> None:
    def no_visible_layer_rule(context: ValidationContext) -> list[Issue]:
        if context.composition is None or any(
            layer.visible for layer in context.composition.layers
        ):
            return []
        return [
            Issue(
                issue_id="composition.no_visible_layer",
                severity=IssueSeverity.ERROR,
                scope=IssueScope.COMPOSITION,
                target_id=context.composition.target_id,
                composition_id=context.composition.composition_id,
                message="Composition không có layer nào đang bật.",
                remediation="Bật ít nhất một layer hợp lệ trước khi Include.",
            )
        ]

    service = ValidationService([no_visible_layer_rule])

    result = service.validate(ValidationContext(composition=composition()))

    assert result.issues[0].issue_id == "composition.no_visible_layer"
    assert result.issues[0].message.startswith("Composition")
    assert "Bật ít nhất" in result.issues[0].remediation
    assert result.summary.error_count == 1
    assert result.blocking is True
