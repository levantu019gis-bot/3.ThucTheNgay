"""Create workspace compositions from cached target/date imagery."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time

from thucthengay.ingestion.cache_builder import UNKNOWN_DATE_KEY, CachePopulationResult
from thucthengay.models import (
    Composition,
    ImageLayer,
    Issue,
    IssueScope,
    IssueSeverity,
    MetadataStatus,
    TargetConfig,
    ViewState,
)
from thucthengay.workspace import WorkspaceService


@dataclass(frozen=True)
class CompositionCreationResult:
    """Composition creation output."""

    composition_ids: list[str]
    issues: list[Issue]


def create_target_date_compositions(
    cache_result: CachePopulationResult,
    targets_by_id: dict[str, TargetConfig],
    workspace_service: WorkspaceService,
) -> CompositionCreationResult:
    """Create one workspace composition per target/date group."""
    composition_ids: list[str] = []
    issues: list[Issue] = []

    for (target_id, date_key), layers in cache_result.layers_by_target_date.items():
        target = targets_by_id.get(target_id)
        if target is None:
            issues.append(
                _composition_issue(
                    "composition.target_missing",
                    target_id,
                    f"Không tìm thấy target config cho nhóm ảnh `{target_id}`.",
                    "Tải lại config và chạy lại bước match trước khi tạo composition.",
                )
            )
            continue

        capture_date = _capture_date_from_key(target_id, date_key, issues)
        if capture_date is None:
            continue

        composition = Composition(
            composition_id=_composition_id(target_id, date_key),
            target_id=target_id,
            capture_date=capture_date,
            layers=_initial_layers(layers),
            view=ViewState(center=target.coordinate, scale=target.scale),
            grid_override=None,
        )
        workspace_service.write_composition(composition)
        composition_ids.append(composition.composition_id)

    return CompositionCreationResult(composition_ids=composition_ids, issues=issues)


def _initial_layers(layers: list[ImageLayer]) -> list[ImageLayer]:
    sorted_layers = sorted(
        layers,
        key=lambda layer: (
            layer.capture_time is not None,
            layer.capture_time or time.min,
            layer.layer_id,
        ),
        reverse=True,
    )
    return [
        _layer_with_initial_order(layer, order)
        for order, layer in enumerate(sorted_layers)
    ]


def _layer_with_initial_order(layer: ImageLayer, order: int) -> ImageLayer:
    metadata_status = layer.metadata_status
    if layer.capture_time is None:
        metadata_status = MetadataStatus.NEEDS_MANUAL_CORRECTION
    return layer.model_copy(update={"order": order, "metadata_status": metadata_status})


def _capture_date_from_key(
    target_id: str,
    date_key: str,
    issues: list[Issue],
) -> date | None:
    if date_key == UNKNOWN_DATE_KEY:
        issues.append(
            _composition_issue(
                "composition.capture_date_missing",
                target_id,
                f"Không thể tạo composition cho target `{target_id}` vì thiếu ngày chụp.",
                "Sửa metadata ngày chụp trước khi tạo composition target-date.",
            )
        )
        return None

    try:
        return date.fromisoformat(f"{date_key[:4]}-{date_key[4:6]}-{date_key[6:8]}")
    except ValueError:
        issues.append(
            _composition_issue(
                "composition.capture_date_invalid",
                target_id,
                f"Ngày chụp `{date_key}` của target `{target_id}` không hợp lệ.",
                "Kiểm tra metadata ngày chụp và chạy lại ingest.",
            )
        )
        return None


def _composition_id(target_id: str, date_key: str) -> str:
    return f"{target_id}__{date_key}"


def _composition_issue(
    issue_id: str,
    target_id: str,
    message: str,
    remediation: str,
) -> Issue:
    return Issue(
        issue_id=issue_id,
        severity=IssueSeverity.WARNING,
        scope=IssueScope.COMPOSITION,
        target_id=target_id,
        message=message,
        remediation=remediation,
    )
