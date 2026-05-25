from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from thucthengay.editor.modes.setup_mode import SetupMode
from thucthengay.editor.widgets import IngestionSummaryWidget
from thucthengay.jobs import IngestionJobResult, IngestionSummary, JobState
from thucthengay.models import Issue, IssueScope, IssueSeverity


def qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


def job_result(
    *,
    state: JobState = JobState.WARNING,
    matched_image_count: int = 0,
    issues: list[Issue] | None = None,
    composition_ids: list[str] | None = None,
) -> IngestionJobResult:
    return IngestionJobResult(
        job_id="job-summary",
        state=state,
        issues=issues or [],
        scanned_image_count=3,
        matched_image_count=matched_image_count,
        targets_with_images_count=1 if matched_image_count else 0,
        composition_ids=composition_ids or [],
    )


def layer_warning() -> Issue:
    return Issue(
        issue_id="imagery.metadata_missing",
        severity=IssueSeverity.WARNING,
        scope=IssueScope.LAYER,
        layer_id="/imagery/raw.tif",
        message="GeoTIFF thiếu metadata nghiệp vụ.",
        remediation="Bổ sung metadata trước khi export.",
    )


def test_summary_distinguishes_warning_state_and_normalizes_warning_rows(
    tmp_path: Path,
) -> None:
    summary = IngestionSummary.from_job_result(
        job_result(
            issues=[layer_warning()],
            matched_image_count=2,
            composition_ids=["target_001__20260525"],
        ),
        workspace_path=tmp_path / "workspace",
    )

    assert summary.success_with_warnings is True
    assert summary.hard_failure is False
    assert summary.warning_count == 1
    assert summary.created_composition_count == 1
    assert summary.composition_ids == ["target_001__20260525"]
    assert summary.empty is False
    warning = summary.warnings[0]
    assert warning.scope == IssueScope.LAYER
    assert warning.affected_object == "/imagery/raw.tif"
    assert warning.review_surfaceable is True
    assert "Bổ sung metadata" in (warning.remediation or "")


def test_summary_empty_state_explains_no_matching_imagery(tmp_path: Path) -> None:
    summary = IngestionSummary.from_job_result(
        job_result(state=JobState.SUCCESS, matched_image_count=0),
        workspace_path=tmp_path / "workspace",
    )

    assert summary.empty is True
    assert summary.empty_state_message is not None
    assert "thư mục ảnh" in summary.empty_state_message
    assert "target" in summary.empty_state_message
    assert "GeoTIFF" in summary.empty_state_message


def test_summary_widget_renders_counters_workspace_empty_state_and_warnings(
    tmp_path: Path,
) -> None:
    qapp()
    summary = IngestionSummary.from_job_result(
        job_result(issues=[layer_warning()], matched_image_count=0),
        workspace_path=tmp_path / "workspace",
    )
    widget = IngestionSummaryWidget()

    widget.show_summary(summary)

    assert widget.status_label.text() == "Lấy dữ liệu hoàn tất với cảnh báo"
    assert widget.scanned_label.text() == "3"
    assert widget.matched_label.text() == "0"
    assert widget.targets_label.text() == "0"
    assert widget.compositions_label.text() == "0"
    assert widget.warnings_label.text() == "1"
    assert str(tmp_path / "workspace") in widget.workspace_label.text()
    assert "boundary target" in widget.empty_state_label.text()
    assert widget.warning_list.count() == 1
    assert "layer: /imagery/raw.tif" in widget.warning_list.item(0).text()
    assert "Cách xử lý" in widget.warning_list.item(0).text()


def test_setup_mode_can_show_latest_ingestion_summary(tmp_path: Path) -> None:
    qapp()
    setup = SetupMode()
    summary = IngestionSummary.from_job_result(
        job_result(state=JobState.SUCCESS, matched_image_count=1),
        workspace_path=tmp_path / "workspace",
    )

    setup.show_ingestion_summary(summary)

    assert setup.summary_widget.status_label.text() == "Lấy dữ liệu thành công"
    assert setup.summary_widget.matched_label.text() == "1"
