"""Progress-reporting ingestion job orchestration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from thucthengay.config.service import ConfigLoadResult
from thucthengay.ingestion import (
    CompositionCreationResult,
    TargetMatchingResult,
    create_target_date_compositions,
    match_imagery_to_targets,
    populate_workspace_cache,
    scan_imagery_folder,
)
from thucthengay.jobs.progress import JobState, ProgressEvent
from thucthengay.models import Issue, IssueScope, IssueSeverity, TargetConfig
from thucthengay.workspace import WorkspaceError, WorkspaceService

ProgressPublisher = Callable[[ProgressEvent], None]


@dataclass(frozen=True)
class IngestionJobResult:
    """Final result returned by an ingestion job run."""

    job_id: str
    state: JobState
    issues: list[Issue]
    scanned_image_count: int
    matched_image_count: int
    targets_with_images_count: int
    composition_ids: list[str]


def run_ingestion_job(
    *,
    job_id: str,
    config_result: ConfigLoadResult,
    imagery_folder: str | Path,
    workspace_service: WorkspaceService,
    clear_existing: bool = False,
    clear_confirmed: bool = False,
    publish: ProgressPublisher | None = None,
) -> IngestionJobResult:
    """Run the ingestion pipeline and emit progress after every major phase."""
    progress = _ProgressBuilder(job_id=job_id, publish=publish)
    progress.emit(stage="setup", message="Đang chuẩn bị lấy dữ liệu.")

    fatal_issues = _fatal_setup_issues(config_result.issues)
    if fatal_issues:
        return _finish_with_error(
            progress,
            job_id=job_id,
            issues=fatal_issues,
            message="Không thể bắt đầu lấy dữ liệu vì cấu hình chưa hợp lệ.",
        )

    try:
        workspace_service.initialize(
            config_path=config_result.config_path,
            imagery_input_path=imagery_folder,
        )
        scan_result = scan_imagery_folder(imagery_folder)
    except (NotADirectoryError, OSError, WorkspaceError) as error:
        return _finish_with_error(
            progress,
            job_id=job_id,
            issues=[_setup_error_issue(error)],
            message="Không thể bắt đầu lấy dữ liệu vì lỗi đường dẫn hoặc workspace.",
        )

    issues: list[Issue] = list(scan_result.warnings)
    progress.update(scanned_image_count=len(scan_result.rasters), issues=issues)
    progress.emit(
        stage="scan",
        current=len(scan_result.rasters),
        total=len(scan_result.rasters),
        message=f"Đã quét {len(scan_result.rasters)} ảnh GeoTIFF hợp lệ.",
    )

    matching_result = match_imagery_to_targets(scan_result.rasters, config_result)
    issues.extend(matching_result.issues)
    _emit_target_match_progress(progress, config_result.enabled_targets, matching_result, issues)

    try:
        cache_result = populate_workspace_cache(
            matching_result,
            workspace_service,
            clear_existing=clear_existing,
            clear_confirmed=clear_confirmed,
        )
        issues.extend(cache_result.issues)
        progress.update(issues=issues)
        progress.emit(stage="cache", message="Đã copy ảnh phù hợp vào workspace cache.")

        composition_result = create_target_date_compositions(
            cache_result,
            _targets_by_id(config_result.enabled_targets),
            workspace_service,
        )
    except (OSError, WorkspaceError) as error:
        issues.append(_workspace_error_issue(error))
        return _finish_with_error(
            progress,
            job_id=job_id,
            issues=issues,
            message="Không thể hoàn tất lấy dữ liệu vì lỗi workspace.",
        )

    issues.extend(composition_result.issues)
    progress.update(
        issues=issues,
        created_composition_count=len(composition_result.composition_ids),
    )

    state = JobState.WARNING if issues else JobState.SUCCESS
    progress.emit(
        stage="complete",
        state=state,
        message=_completion_message(state, composition_result),
    )
    return IngestionJobResult(
        job_id=job_id,
        state=state,
        issues=issues,
        scanned_image_count=progress.scanned_image_count,
        matched_image_count=progress.matched_image_count,
        targets_with_images_count=progress.targets_with_images_count,
        composition_ids=composition_result.composition_ids,
    )


@dataclass
class _ProgressBuilder:
    job_id: str
    publish: ProgressPublisher | None = None
    scanned_image_count: int = 0
    matched_image_count: int = 0
    targets_with_images_count: int = 0
    warning_count: int = 0
    issues: list[Issue] | None = None
    created_composition_count: int = 0

    def update(
        self,
        *,
        scanned_image_count: int | None = None,
        matched_image_count: int | None = None,
        targets_with_images_count: int | None = None,
        issues: list[Issue] | None = None,
        created_composition_count: int | None = None,
    ) -> None:
        if scanned_image_count is not None:
            self.scanned_image_count = scanned_image_count
        if matched_image_count is not None:
            self.matched_image_count = matched_image_count
        if targets_with_images_count is not None:
            self.targets_with_images_count = targets_with_images_count
        if issues is not None:
            self.issues = list(issues)
            self.warning_count = len(issues)
        if created_composition_count is not None:
            self.created_composition_count = created_composition_count

    def emit(
        self,
        *,
        stage: str,
        message: str,
        state: JobState = JobState.RUNNING,
        current: int | None = None,
        total: int | None = None,
        current_target: TargetConfig | None = None,
        current_target_matched_count: int = 0,
    ) -> ProgressEvent:
        event = ProgressEvent(
            job_id=self.job_id,
            stage=stage,
            state=state,
            current=current,
            total=total,
            message=message,
            issues=list(self.issues or []),
            scanned_image_count=self.scanned_image_count,
            matched_image_count=self.matched_image_count,
            targets_with_images_count=self.targets_with_images_count,
            warning_count=self.warning_count,
            current_target_id=current_target.id if current_target else None,
            current_target_name=current_target.name if current_target else None,
            current_target_matched_count=current_target_matched_count,
            created_composition_count=self.created_composition_count,
        )
        if self.publish is not None:
            self.publish(event)
        return event


def _emit_target_match_progress(
    progress: _ProgressBuilder,
    targets: list[TargetConfig],
    matching_result: TargetMatchingResult,
    issues: list[Issue],
) -> None:
    matched_image_count = sum(len(matches) for matches in matching_result.matches.values())
    targets_with_images_count = sum(
        1 for matches in matching_result.matches.values() if matches
    )
    progress.update(
        matched_image_count=matched_image_count,
        targets_with_images_count=targets_with_images_count,
        issues=issues,
    )

    total = len(targets)
    for index, target in enumerate(targets, start=1):
        current_matches = len(matching_result.matches.get(target.id, []))
        progress.emit(
            stage="match",
            current=index,
            total=total,
            message=f"Target `{target.name}` có {current_matches} ảnh phù hợp.",
            current_target=target,
            current_target_matched_count=current_matches,
        )

    if not targets:
        progress.emit(stage="match", current=0, total=0, message="Không có target bật.")


def _finish_with_error(
    progress: _ProgressBuilder,
    *,
    job_id: str,
    issues: list[Issue],
    message: str,
) -> IngestionJobResult:
    progress.update(issues=issues)
    progress.emit(stage="error", state=JobState.ERROR, message=message)
    return IngestionJobResult(
        job_id=job_id,
        state=JobState.ERROR,
        issues=issues,
        scanned_image_count=progress.scanned_image_count,
        matched_image_count=progress.matched_image_count,
        targets_with_images_count=progress.targets_with_images_count,
        composition_ids=[],
    )


def _fatal_setup_issues(issues: list[Issue]) -> list[Issue]:
    fatal_scopes = {IssueScope.CONFIG, IssueScope.PROJECT, IssueScope.WORKSPACE}
    return [issue for issue in issues if issue.scope in fatal_scopes]


def _targets_by_id(targets: list[TargetConfig]) -> dict[str, TargetConfig]:
    return {target.id: target for target in targets}


def _completion_message(
    state: JobState,
    composition_result: CompositionCreationResult,
) -> str:
    created_count = len(composition_result.composition_ids)
    if state == JobState.WARNING:
        return f"Lấy dữ liệu hoàn tất với cảnh báo; đã tạo {created_count} composition."
    return f"Lấy dữ liệu hoàn tất; đã tạo {created_count} composition."


def _setup_error_issue(error: Exception) -> Issue:
    return Issue(
        issue_id="ingestion.setup_failed",
        severity=IssueSeverity.ERROR,
        scope=IssueScope.PROJECT,
        message=f"Không thể chuẩn bị dữ liệu đầu vào: {error}",
        remediation="Kiểm tra lại config, thư mục ảnh và workspace rồi chạy lại.",
    )


def _workspace_error_issue(error: Exception) -> Issue:
    return Issue(
        issue_id="ingestion.workspace_failed",
        severity=IssueSeverity.ERROR,
        scope=IssueScope.WORKSPACE,
        message=f"Không thể ghi workspace trong quá trình lấy dữ liệu: {error}",
        remediation="Kiểm tra quyền ghi workspace và xác nhận xóa dữ liệu cũ nếu cần.",
    )
