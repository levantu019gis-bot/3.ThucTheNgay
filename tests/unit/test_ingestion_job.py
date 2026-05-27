from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from thucthengay.config.service import ConfigLoadResult, ResolvedTargetPaths
from thucthengay.jobs import (
    ActiveJobProgressModel,
    JobControl,
    JobState,
    ProgressEvent,
    QueuedProgressDispatcher,
    run_ingestion_job,
)
from thucthengay.models import (
    GridConfig,
    GridInterval,
    Issue,
    IssueScope,
    IssueSeverity,
    ProjectConfig,
    TargetConfig,
    TargetExportConfig,
)
from thucthengay.workspace import WorkspaceService


def target_config(target_id: str = "target_001") -> TargetConfig:
    return TargetConfig(
        id=target_id,
        enabled=True,
        sort_order=1,
        name="Target 001",
        geojson_file=f"{target_id}.geojson",
        coordinate=[106.0, 11.0],
        scale=50000,
        grid=GridConfig(interval=GridInterval(minutes=1)),
        export=TargetExportConfig(template_metadata_file=f"{target_id}.template.json"),
    )


def config_result_for(target: TargetConfig, geojson_path: Path) -> ConfigLoadResult:
    return ConfigLoadResult(
        config_path=geojson_path.parent / "config.json",
        config=ProjectConfig(targets=[target]),
        enabled_targets=[target],
        target_paths={
            target.id: ResolvedTargetPaths(
                target_id=target.id,
                geojson_file=geojson_path,
                template_metadata_file=geojson_path.parent / f"{target.id}.template.json",
            )
        },
    )


def write_geotiff(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=2,
        width=2,
        count=1,
        dtype="uint8",
        crs="EPSG:4326",
        transform=from_origin(106.0, 11.0, 0.1, 0.1),
    ) as dataset:
        dataset.write(np.ones((1, 2, 2), dtype="uint8"))


def write_geojson(path: Path) -> None:
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [106.05, 10.85],
                            [106.08, 10.85],
                            [106.08, 10.88],
                            [106.05, 10.88],
                            [106.05, 10.85],
                        ]
                    ],
                },
            }
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def test_progress_model_ignores_stale_job_updates_and_marks_active_completion() -> None:
    progress_model = ActiveJobProgressModel()
    progress_model.start("active")

    stale_event = ProgressEvent(
        job_id="old",
        stage="complete",
        state=JobState.SUCCESS,
        message="old done",
    )
    active_event = ProgressEvent(
        job_id="active",
        stage="complete",
        state=JobState.SUCCESS,
        message="active done",
    )

    assert progress_model.apply(stale_event) is False
    assert progress_model.complete is False
    assert progress_model.latest is None

    assert progress_model.apply(active_event) is True
    assert progress_model.complete is True
    assert progress_model.completed_job_id == "active"


def test_queued_dispatcher_hands_off_events_for_main_thread_drain() -> None:
    dispatcher = QueuedProgressDispatcher()
    first = ProgressEvent(job_id="job", stage="scan", message="scanning")
    second = ProgressEvent(job_id="job", stage="complete", message="done")

    dispatcher.publish(first)
    dispatcher.publish(second)

    assert dispatcher.drain() == [first, second]
    assert dispatcher.drain() == []


def test_ingestion_job_emits_progress_counters_and_success_state(tmp_path: Path) -> None:
    imagery = tmp_path / "imagery"
    geotiff = imagery / "20260525_101112_scene_cloud12.tif"
    boundary = tmp_path / "target_001.geojson"
    write_geotiff(geotiff)
    write_geojson(boundary)
    workspace = WorkspaceService(tmp_path / "workspace")
    events: list[ProgressEvent] = []

    result = run_ingestion_job(
        job_id="job-1",
        config_result=config_result_for(target_config(), boundary),
        imagery_folder=imagery,
        workspace_service=workspace,
        publish=events.append,
    )

    assert result.state == JobState.SUCCESS
    assert result.issues == []
    assert result.scanned_image_count == 1
    assert result.matched_image_count == 1
    assert result.targets_with_images_count == 1
    assert result.composition_ids == ["target_001__20260525"]
    assert workspace.load_manifest().composition_ids == ["target_001__20260525"]
    assert events[0].stage == "setup"
    assert events[-1].stage == "complete"
    scan_events = [event for event in events if event.stage == "scan"]
    assert scan_events[0].scanned_file_count == 0
    assert scan_events[0].total_image_count == 1
    assert scan_events[-1].scanned_file_count == 1
    assert scan_events[-1].total_image_count == 1
    assert scan_events[-1].scanned_image_count == 1
    match_events = [event for event in events if event.stage == "match"]
    match_event = match_events[0]
    assert match_event.processed_target_count == 1
    assert match_event.total_target_count == 1
    assert match_event.current_target_id == "target_001"
    assert match_event.current_target_matched_count == 1
    assert match_events[-1].matched_image_count == 1
    assert events[-1].state == JobState.SUCCESS
    assert events[-1].warning_count == 0


def test_ingestion_job_preserves_nonfatal_warnings_for_summary(tmp_path: Path) -> None:
    imagery = tmp_path / "imagery"
    geotiff = imagery / "20260525_101112_scene.tif"
    boundary = tmp_path / "target_001.geojson"
    write_geotiff(geotiff)
    write_geojson(boundary)
    events: list[ProgressEvent] = []

    result = run_ingestion_job(
        job_id="job-warning",
        config_result=config_result_for(target_config(), boundary),
        imagery_folder=imagery,
        workspace_service=WorkspaceService(tmp_path / "workspace"),
        publish=events.append,
    )

    assert result.state == JobState.WARNING
    assert result.composition_ids == ["target_001__20260525"]
    assert [issue.issue_id for issue in result.issues] == ["imagery.metadata_missing"]
    assert events[-1].state == JobState.WARNING
    assert events[-1].warning_count == 1
    assert events[-1].issues == result.issues


def test_ingestion_job_reports_fatal_setup_error_without_workspace_completion(
    tmp_path: Path,
) -> None:
    fatal_issue = Issue(
        issue_id="config.invalid",
        severity=IssueSeverity.ERROR,
        scope=IssueScope.CONFIG,
        message="Config không hợp lệ.",
    )
    config_result = ConfigLoadResult(
        config_path=tmp_path / "config.json",
        issues=[fatal_issue],
    )
    workspace = WorkspaceService(tmp_path / "workspace")
    events: list[ProgressEvent] = []

    result = run_ingestion_job(
        job_id="job-error",
        config_result=config_result,
        imagery_folder=tmp_path / "missing-imagery",
        workspace_service=workspace,
        publish=events.append,
    )

    assert result.state == JobState.ERROR
    assert result.composition_ids == []
    assert result.issues == [fatal_issue]
    assert events[-1].state == JobState.ERROR
    assert events[-1].scanned_image_count == 0
    assert workspace.paths.manifest.exists() is False


def test_ingestion_job_can_be_cancelled_before_scan(tmp_path: Path) -> None:
    imagery = tmp_path / "imagery"
    imagery.mkdir()
    boundary = tmp_path / "target_001.geojson"
    write_geojson(boundary)
    events: list[ProgressEvent] = []
    control = JobControl()
    control.request_cancel()

    result = run_ingestion_job(
        job_id="job-cancelled",
        config_result=config_result_for(target_config(), boundary),
        imagery_folder=imagery,
        workspace_service=WorkspaceService(tmp_path / "workspace"),
        control=control,
        publish=events.append,
    )

    assert result.state == JobState.CANCELLED
    assert result.composition_ids == []
    assert events[-1].state == JobState.CANCELLED
    assert events[-1].stage == "cancelled"
