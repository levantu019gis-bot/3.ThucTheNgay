"""Project configuration loading and reference validation service."""

from __future__ import annotations

from dataclasses import dataclass, field
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from thucthengay.config.loader import load_json_file
from thucthengay.config.path_resolver import resolve_relative_to_file
from thucthengay.models import (
    Issue,
    IssueScope,
    IssueSeverity,
    ProjectConfig,
    TargetConfig,
    TemplateMetadata,
)


@dataclass(frozen=True)
class ResolvedTargetPaths:
    """Filesystem paths resolved from one enabled target config."""

    target_id: str
    geojson_file: Path
    template_metadata_file: Path
    template_pptx: Path | None = None


@dataclass
class ConfigLoadResult:
    """Structured result for expected config loading outcomes."""

    config_path: Path
    config: ProjectConfig | None = None
    enabled_targets: list[TargetConfig] = field(default_factory=list)
    target_paths: dict[str, ResolvedTargetPaths] = field(default_factory=dict)
    template_metadata: dict[str, TemplateMetadata] = field(default_factory=dict)
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(issue.blocking for issue in self.issues)


def load_project_config(config_path: str | Path) -> ConfigLoadResult:
    """Load config JSON, enabled target references, and template metadata."""
    config_file = Path(config_path).resolve()
    result = ConfigLoadResult(config_path=config_file)

    try:
        raw_config = load_json_file(config_file)
        result.config = ProjectConfig.model_validate(_enabled_targets_only(raw_config))
    except FileNotFoundError:
        result.issues.append(
            _config_issue(
                "config.file_missing",
                f"Không tìm thấy file config: {config_file}",
                "Chọn lại file config.json hợp lệ.",
            )
        )
        return result
    except PermissionError:
        result.issues.append(
            _config_issue(
                "config.file_unreadable",
                f"Không thể đọc file config: {config_file}",
                "Kiểm tra quyền truy cập file hoặc chọn file khác.",
            )
        )
        return result
    except OSError as error:
        result.issues.append(
            _config_issue(
                "config.file_unreadable",
                f"Không thể đọc file config: {config_file}",
                f"Kiểm tra lại đường dẫn và quyền truy cập. Chi tiết kỹ thuật: {error}",
            )
        )
        return result
    except JSONDecodeError as error:
        result.issues.append(
            _config_issue(
                "config.invalid_json",
                f"File config không phải JSON hợp lệ tại dòng {error.lineno}, cột {error.colno}.",
                "Sửa cú pháp JSON rồi tải lại config.",
            )
        )
        return result
    except (ValueError, ValidationError) as error:
        result.issues.extend(_validation_issues(error))
        return result

    result.enabled_targets = sorted(
        (target for target in result.config.targets if target.enabled),
        key=lambda target: target.sort_order,
    )

    for target in result.enabled_targets:
        _validate_target_references(config_file, target, result)

    return result


def _enabled_targets_only(raw_config: dict[str, Any]) -> dict[str, Any]:
    raw_targets = raw_config.get("targets")
    if not isinstance(raw_targets, list):
        return raw_config

    filtered_config = dict(raw_config)
    filtered_config["targets"] = [
        target
        for target in raw_targets
        if not isinstance(target, dict) or target.get("enabled", True)
    ]
    return filtered_config


def _validate_target_references(
    config_file: Path,
    target: TargetConfig,
    result: ConfigLoadResult,
) -> None:
    geojson_file = resolve_relative_to_file(config_file, target.geojson_file)
    template_metadata_file = resolve_relative_to_file(
        config_file,
        target.export.template_metadata_file,
    )

    target_paths = ResolvedTargetPaths(
        target_id=target.id,
        geojson_file=geojson_file,
        template_metadata_file=template_metadata_file,
    )

    if not geojson_file.is_file():
        result.issues.append(
            _target_issue(
                "target.geojson_missing",
                target.id,
                f"Không tìm thấy GeoJSON của target `{target.id}`: {geojson_file}",
                "Kiểm tra lại `geojson_file` trong config; "
                "đường dẫn được tính tương đối từ config.json.",
            )
        )

    if not template_metadata_file.is_file():
        result.issues.append(
            _target_issue(
                "target.template_metadata_missing",
                target.id,
                "Không tìm thấy template metadata của target "
                f"`{target.id}`: {template_metadata_file}",
                "Kiểm tra lại `export.template_metadata_file` trong config.",
            )
        )
        result.target_paths[target.id] = target_paths
        return

    try:
        raw_template = load_json_file(template_metadata_file)
        template_metadata = TemplateMetadata.model_validate(raw_template)
    except (OSError, JSONDecodeError, ValueError, ValidationError) as error:
        result.issues.append(_template_load_issue(target.id, template_metadata_file, error))
        result.target_paths[target.id] = target_paths
        return

    template_pptx = resolve_relative_to_file(
        template_metadata_file,
        template_metadata.template_pptx,
    )
    target_paths = ResolvedTargetPaths(
        target_id=target.id,
        geojson_file=geojson_file,
        template_metadata_file=template_metadata_file,
        template_pptx=template_pptx,
    )
    result.template_metadata[target.id] = template_metadata.model_copy(
        update={"template_pptx": str(template_pptx)}
    )

    if not template_pptx.is_file():
        result.issues.append(
            _target_issue(
                "target.template_pptx_missing",
                target.id,
                f"Không tìm thấy PPTX template của target `{target.id}`: {template_pptx}",
                "Kiểm tra `template_pptx` trong template metadata; "
                "đường dẫn tính từ metadata file.",
            )
        )

    result.target_paths[target.id] = target_paths


def _config_issue(issue_id: str, message: str, remediation: str) -> Issue:
    return Issue(
        issue_id=issue_id,
        severity=IssueSeverity.ERROR,
        scope=IssueScope.CONFIG,
        message=message,
        remediation=remediation,
    )


def _target_issue(issue_id: str, target_id: str, message: str, remediation: str) -> Issue:
    return Issue(
        issue_id=issue_id,
        severity=IssueSeverity.ERROR,
        scope=IssueScope.TARGET,
        target_id=target_id,
        message=message,
        remediation=remediation,
    )


def _validation_issues(error: ValueError | ValidationError) -> list[Issue]:
    if not isinstance(error, ValidationError):
        return [
            _config_issue(
                "config.invalid",
                f"Config không hợp lệ: {error}",
                "Kiểm tra cấu trúc config JSON và các trường bắt buộc.",
            )
        ]

    issues: list[Issue] = []
    for item in error.errors():
        field_path = ".".join(str(part) for part in item["loc"])
        issues.append(
            _config_issue(
                "config.field_invalid",
                f"Trường config `{field_path}` không hợp lệ: {item['msg']}",
                _remediation_for_field_path(field_path),
            )
        )
    return issues


def _remediation_for_field_path(field_path: str) -> str:
    if "coordinate" in field_path:
        return "Khai báo `coordinate` dạng `[lon, lat]`, ví dụ `[106.7, 10.8]`."
    if "scale" in field_path:
        return "`scale` phải là mẫu số tỷ lệ bản đồ dương, ví dụ `50000`."
    if "grid.interval" in field_path:
        return "`grid.interval` phải là cấu hình DMS hợp lệ và lớn hơn 0."
    if "template_metadata_file" in field_path:
        return "Khai báo `export.template_metadata_file` trỏ tới file metadata JSON của target."
    return "Kiểm tra giá trị và kiểu dữ liệu của trường này trong config JSON."


def _template_load_issue(target_id: str, template_metadata_file: Path, error: Any) -> Issue:
    return _target_issue(
        "target.template_metadata_invalid",
        target_id,
        f"Template metadata của target `{target_id}` không hợp lệ: {template_metadata_file}",
        f"Sửa file template metadata. Chi tiết kỹ thuật: {error}",
    )
