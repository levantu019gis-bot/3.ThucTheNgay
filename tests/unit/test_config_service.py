from __future__ import annotations

import json
from pathlib import Path

from thucthengay.config import load_project_config


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def target_config(
    target_id: str,
    sort_order: int,
    *,
    enabled: bool = True,
    template_metadata_file: str | None = None,
) -> dict[str, object]:
    return {
        "id": target_id,
        "enabled": enabled,
        "sort_order": sort_order,
        "name": target_id,
        "geojson_file": f"targets/{target_id}.geojson",
        "coordinate": [106.7, 10.8],
        "scale": 50000,
        "grid": {"interval": {"minutes": 1}},
        "export": {
            "template_metadata_file": template_metadata_file
            or f"templates/{target_id}.template.json"
        },
    }


def template_metadata(template_pptx: str = "target.pptx") -> dict[str, object]:
    return {
        "template_pptx": template_pptx,
        "slide_index": 0,
        "map_frame": {"x": 0, "y": 0, "width": 100, "height": 80},
        "placeholders": [{"name": "MapFrame", "kind": "map_image"}],
    }


def prepare_target_files(root: Path, target_id: str, template_pptx: str = "target.pptx") -> None:
    (root / "targets").mkdir(parents=True, exist_ok=True)
    (root / "targets" / f"{target_id}.geojson").write_text("{}", encoding="utf-8")
    write_json(root / "templates" / f"{target_id}.template.json", template_metadata(template_pptx))
    (root / "templates" / template_pptx).write_text("pptx placeholder", encoding="utf-8")


def test_load_project_config_filters_enabled_targets_and_resolves_paths(tmp_path: Path) -> None:
    prepare_target_files(tmp_path, "target_b")
    prepare_target_files(tmp_path, "target_a")
    write_json(
        tmp_path / "config.json",
        {
            "targets": [
                target_config("target_b", 2),
                target_config("disabled", 0, enabled=False),
                target_config("target_a", 1),
            ]
        },
    )

    result = load_project_config(tmp_path / "config.json")

    assert result.ok is True
    assert [target.id for target in result.enabled_targets] == ["target_a", "target_b"]
    assert result.target_paths["target_a"].geojson_file == (
        tmp_path / "targets" / "target_a.geojson"
    ).resolve()


def test_disabled_targets_are_not_schema_or_reference_blockers(tmp_path: Path) -> None:
    prepare_target_files(tmp_path, "target_a")
    disabled_invalid_target = {
        "id": "disabled",
        "enabled": False,
        "sort_order": 0,
        "name": "Disabled",
    }
    write_json(
        tmp_path / "config.json",
        {"targets": [disabled_invalid_target, target_config("target_a", 1)]},
    )

    result = load_project_config(tmp_path / "config.json")

    assert result.ok is True
    assert [target.id for target in result.enabled_targets] == ["target_a"]
    assert "disabled" not in result.target_paths


def test_invalid_config_returns_vietnamese_field_path_issue(tmp_path: Path) -> None:
    data = target_config("target_a", 1)
    data["coordinate"] = [999, 10]
    write_json(tmp_path / "config.json", {"targets": [data]})

    result = load_project_config(tmp_path / "config.json")

    assert result.ok is False
    assert result.issues[0].blocking is True
    assert "`targets.0.coordinate`" in result.issues[0].message
    assert "[lon, lat]" in (result.issues[0].remediation or "")


def test_missing_references_create_blocking_target_issues(tmp_path: Path) -> None:
    write_json(tmp_path / "config.json", {"targets": [target_config("target_a", 1)]})

    result = load_project_config(tmp_path / "config.json")
    issue_ids = {issue.issue_id for issue in result.issues}

    assert result.ok is False
    assert "target.geojson_missing" in issue_ids
    assert "target.template_metadata_missing" in issue_ids
    assert all(issue.blocking for issue in result.issues)


def test_config_directory_path_returns_structured_issue(tmp_path: Path) -> None:
    result = load_project_config(tmp_path)

    assert result.ok is False
    assert result.issues[0].issue_id == "config.file_unreadable"
    assert result.issues[0].blocking is True


def test_template_pptx_resolves_relative_to_metadata_file(tmp_path: Path) -> None:
    (tmp_path / "targets").mkdir(parents=True)
    (tmp_path / "targets" / "target_a.geojson").write_text("{}", encoding="utf-8")
    write_json(
        tmp_path / "templates" / "nested" / "target_a.template.json",
        template_metadata("../target_a.pptx"),
    )
    (tmp_path / "templates" / "target_a.pptx").write_text("pptx placeholder", encoding="utf-8")
    write_json(
        tmp_path / "config.json",
        {
            "targets": [
                target_config(
                    "target_a",
                    1,
                    template_metadata_file="templates/nested/target_a.template.json",
                )
            ]
        },
    )

    result = load_project_config(tmp_path / "config.json")

    assert result.ok is True
    assert result.target_paths["target_a"].template_pptx == (
        tmp_path / "templates" / "target_a.pptx"
    ).resolve()
    assert result.template_metadata["target_a"].template_pptx == str(
        (tmp_path / "templates" / "target_a.pptx").resolve()
    )


def test_invalid_template_metadata_is_blocking(tmp_path: Path) -> None:
    (tmp_path / "targets").mkdir(parents=True)
    (tmp_path / "targets" / "target_a.geojson").write_text("{}", encoding="utf-8")
    write_json(tmp_path / "templates" / "target_a.template.json", {"slide_index": 0})
    write_json(tmp_path / "config.json", {"targets": [target_config("target_a", 1)]})

    result = load_project_config(tmp_path / "config.json")

    assert result.ok is False
    assert {issue.issue_id for issue in result.issues} == {"target.template_metadata_invalid"}
