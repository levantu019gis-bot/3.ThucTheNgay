from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from thucthengay.models import (
    Composition,
    ExportLog,
    GridConfig,
    GridInterval,
    ImageLayer,
    Issue,
    IssueScope,
    IssueSeverity,
    MapFrame,
    PersistedValidationState,
    ProjectConfig,
    RenderResult,
    TargetConfig,
    TemplateMetadata,
    TemplatePlaceholder,
    ValidationSummary,
    ViewState,
    WorkspaceManifest,
)


def valid_grid() -> GridConfig:
    return GridConfig(interval=GridInterval(minutes=1))


def valid_target_dict() -> dict[str, object]:
    return {
        "id": "target_001",
        "enabled": True,
        "sort_order": 1,
        "name": "Target 001",
        "alias": "T001",
        "title": "Target 001 Title",
        "geojson_file": "targets/target_001.geojson",
        "coordinate": [106.7, 10.8],
        "scale": 50000,
        "grid": {"interval": {"minutes": 1}},
        "export": {"template_metadata_file": "templates/target_001.template.json"},
    }


def test_project_config_supports_target_specific_template_metadata() -> None:
    config = ProjectConfig.model_validate({"targets": [valid_target_dict()]})

    target = config.targets[0]

    assert target.export.template_metadata_file == "templates/target_001.template.json"
    assert target.geojson_file == "targets/target_001.geojson"
    assert target.coordinate == [106.7, 10.8]
    assert target.scale == 50000
    assert target.grid.interval.minutes == 1


def test_project_config_validation_error_locations_are_specific() -> None:
    data = valid_target_dict()
    data["coordinate"] = [200, 10]

    with pytest.raises(ValidationError) as exc_info:
        ProjectConfig.model_validate({"targets": [data]})

    error_locations = {tuple(error["loc"]) for error in exc_info.value.errors()}

    assert ("targets", 0, "coordinate") in error_locations


def test_non_positive_scale_fails_on_target_field() -> None:
    data = valid_target_dict()
    data["scale"] = 0

    with pytest.raises(ValidationError) as exc_info:
        TargetConfig.model_validate(data)

    assert ("scale",) in {tuple(error["loc"]) for error in exc_info.value.errors()}


def test_zero_grid_interval_fails_on_interval_field() -> None:
    with pytest.raises(ValidationError) as exc_info:
        GridConfig.model_validate({"interval": {"degrees": 0, "minutes": 0, "seconds": 0}})

    assert ("interval",) in {tuple(error["loc"]) for error in exc_info.value.errors()}


def test_template_metadata_requires_template_path_and_map_frame() -> None:
    metadata = TemplateMetadata(
        template_pptx="templates/target_001.pptx",
        slide_index=0,
        map_frame=MapFrame(x=10, y=20, width=640, height=360),
        placeholders=[
            TemplatePlaceholder(name="MapFrame", kind="map_image"),
            TemplatePlaceholder(name="Title", kind="text", required=False),
        ],
    )

    dumped = metadata.model_dump(mode="json")

    assert dumped["template_pptx"] == "templates/target_001.pptx"
    assert dumped["placeholders"][0]["kind"] == "map_image"


def test_template_metadata_missing_required_field_has_field_location() -> None:
    with pytest.raises(ValidationError) as exc_info:
        TemplateMetadata.model_validate(
            {
                "slide_index": 0,
                "map_frame": {"x": 0, "y": 0, "width": 100, "height": 100},
            }
        )

    assert ("template_pptx",) in {tuple(error["loc"]) for error in exc_info.value.errors()}


def test_composition_defaults_and_round_trip_are_json_friendly() -> None:
    composition = Composition(
        composition_id="target_001__20260525",
        target_id="target_001",
        capture_date=date(2026, 5, 25),
        view=ViewState(center=[106.7, 10.8], scale=50000),
        layers=[
            ImageLayer(
                layer_id="layer_001",
                source_path="imagery/raw.tif",
                cache_path="cache/target_001/20260525/raw.tif",
                order=0,
                capture_date=date(2026, 5, 25),
                cloud_percent=12.5,
                metadata_status="valid",
                metadata_source="filename",
            )
        ],
    )

    dumped = composition.model_dump(mode="json")
    restored = Composition.model_validate(dumped)

    assert dumped["reviewed"] is False
    assert dumped["ready"] is False
    assert dumped["include"] is False
    assert dumped["needs_revalidation"] is True
    assert restored.layers[0].order == 0


def test_issue_contract_serializes_vietnamese_message_and_blocking_flag() -> None:
    issue = Issue(
        issue_id="layer.file_missing",
        severity=IssueSeverity.ERROR,
        scope=IssueScope.LAYER,
        target_id="target_001",
        composition_id="target_001__20260525",
        layer_id="layer_001",
        message="Không tìm thấy file ảnh.",
        remediation="Kiểm tra lại cache hoặc chạy ingest lại.",
        blocking=True,
    )

    dumped = issue.model_dump(mode="json")

    assert dumped["severity"] == "error"
    assert dumped["message"].startswith("Không")
    assert dumped["blocking"] is True


def test_error_issue_is_always_blocking() -> None:
    issue = Issue(
        issue_id="composition.invalid",
        severity=IssueSeverity.ERROR,
        scope=IssueScope.COMPOSITION,
        message="Composition không hợp lệ.",
    )

    assert issue.blocking is True


def test_invalid_issue_severity_reports_severity_field() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Issue.model_validate(
            {
                "issue_id": "bad",
                "severity": "fatal",
                "scope": "layer",
                "message": "Lỗi.",
            }
        )

    assert ("severity",) in {tuple(error["loc"]) for error in exc_info.value.errors()}


def test_render_result_center_validates_lon_lat_range() -> None:
    with pytest.raises(ValidationError) as exc_info:
        RenderResult(
            composition_id="target_001__20260525",
            output_path="renders/target_001__20260525.png",
            width=1920,
            height=1080,
            center=[999, 10.8],
            scale=50000,
        )

    assert ("center",) in {tuple(error["loc"]) for error in exc_info.value.errors()}


def test_workspace_render_and_export_models_round_trip() -> None:
    manifest = WorkspaceManifest(
        config_path="config.json",
        imagery_input_path="imagery",
        composition_ids=["target_001__20260525"],
    )
    render_result = RenderResult(
        composition_id="target_001__20260525",
        output_path="renders/target_001__20260525.png",
        width=1920,
        height=1080,
        center=[106.7, 10.8],
        scale=50000,
        layer_ids=["layer_001"],
    )
    export_log = ExportLog(
        pptx_path="exports/report.pptx",
        txt_path="exports/report.txt",
        slide_count=1,
        target_count=1,
    )

    restored_manifest = WorkspaceManifest.model_validate(manifest.model_dump(mode="json"))

    assert restored_manifest.config_path == "config.json"
    assert RenderResult.model_validate(render_result.model_dump(mode="json")).width == 1920
    assert ExportLog.model_validate(export_log.model_dump(mode="json")).slide_count == 1


def test_persisted_validation_state_distinguishes_stale_clean_warning_error() -> None:
    stale = Composition(
        composition_id="target_001__20260525",
        target_id="target_001",
        capture_date=date(2026, 5, 25),
        view=ViewState(center=[106.7, 10.8], scale=50000),
    )
    clean = stale.model_copy(update={"needs_revalidation": False})
    warning = stale.model_copy(
        update={
            "needs_revalidation": False,
            "validation_summary": ValidationSummary(warning_count=1),
        }
    )
    error = stale.model_copy(
        update={
            "needs_revalidation": False,
            "validation_summary": ValidationSummary(error_count=1, warning_count=1),
        }
    )

    assert stale.persisted_validation_state == PersistedValidationState.STALE
    assert clean.persisted_validation_state == PersistedValidationState.CLEAN
    assert warning.persisted_validation_state == PersistedValidationState.WARNING
    assert error.persisted_validation_state == PersistedValidationState.ERROR
