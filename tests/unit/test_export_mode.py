from __future__ import annotations

import os
from datetime import date, time
from pathlib import Path

import numpy as np

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from thucthengay.editor.app_shell import AppShell
from thucthengay.editor.models.export_plan_model import ExportPlanRole
from thucthengay.editor.modes.export_mode import ExportMode
from thucthengay.export import ensure_final_renders_for_export
from thucthengay.models import (
    Composition,
    CompositionArtifacts,
    GridConfig,
    GridInterval,
    ImageLayer,
    MapFrame,
    MetadataStatus,
    PlaceholderType,
    TargetConfig,
    TemplateMetadata,
    TemplatePlaceholder,
    ViewState,
)
from thucthengay.render import RasterRenderResult, RenderSpec
from thucthengay.workspace import WorkspaceService


def qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


def target_config() -> TargetConfig:
    return TargetConfig(
        id="alpha",
        name="Alpha Target",
        geojson_file="targets/alpha.geojson",
        coordinate=[106.7, 10.8],
        scale=50000,
        grid=GridConfig(interval=GridInterval(minutes=1)),
        export={
            "template_pptx_file": "templates/alpha.pptx",
            "txt_line_template": "{slide_number}|{target_id}|{time_label}",
            "placeholders": [
                {
                    "field": "map",
                    "element_id": 10,
                    "kind": PlaceholderType.MAP_IMAGE,
                    "required": True,
                }
            ],
        },
        metadata={
            "template_metadata": TemplateMetadata(
                template_pptx="templates/alpha.pptx",
                slide_index=0,
                map_frame=MapFrame(x=0, y=0, width=640, height=360),
                placeholders=[
                    TemplatePlaceholder(
                        field="map",
                        element_id=10,
                        kind=PlaceholderType.MAP_IMAGE,
                        required=True,
                    )
                ],
            ).model_dump(mode="json")
        },
    )


def composition(final_render_path: str | None = "renders/final/alpha.png") -> Composition:
    return Composition(
        composition_id="alpha__20260525",
        target_id="alpha",
        capture_date=date(2026, 5, 25),
        view=ViewState(center=[106.7, 10.8], scale=50000),
        reviewed=True,
        ready=True,
        include=True,
        needs_revalidation=False,
        review_order=1,
        artifacts=CompositionArtifacts(final_render_path=final_render_path),
        layers=[
            ImageLayer(
                layer_id="l1",
                source_path="l1.tif",
                order=0,
                visible=True,
                capture_date=date(2026, 5, 25),
                capture_time=time(8, 30),
                metadata_status=MetadataStatus.VALID,
            )
        ],
    )


def workspace(
    tmp_path: Path,
    final_render_path: str | None = "renders/final/alpha.png",
) -> WorkspaceService:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    render_dir = service.paths.root / "renders" / "final"
    render_dir.mkdir(parents=True, exist_ok=True)
    if final_render_path is not None:
        (render_dir / "alpha.png").write_bytes(b"png")
    service.write_composition(composition(final_render_path))
    return service


def success_render(spec: RenderSpec, is_cancelled=None) -> RasterRenderResult:
    return RasterRenderResult(
        canvas=np.zeros((spec.output_height, spec.output_width, 3), dtype=np.uint8),
        painted_layer_ids=tuple(layer.layer_id for layer in spec.visible_layers),
    )


def test_export_mode_runs_preflight_and_populates_plan(tmp_path: Path) -> None:
    qapp()
    mode = ExportMode()
    service = workspace(tmp_path, final_render_path=None)
    target = target_config()
    ensure_final_renders_for_export(service, [target], render=success_render)
    mode.load_workspace(service, targets=[target])

    mode.preflight_button.click()

    assert mode.plan_model.rowCount() == 1
    assert mode.summary.state_label.text() == "Preflight: ready"
    assert mode.export_button.isEnabled() is False
    index = mode.plan_model.index(0, 0)
    assert index.data(ExportPlanRole.COMPOSITION_ID) == "alpha__20260525"
    assert mode.plan_model.index(0, 4).data(Qt.ItemDataRole.DisplayRole) == "0 issues"


def test_export_mode_blocks_export_and_exposes_jump_signal(tmp_path: Path) -> None:
    qapp()
    mode = ExportMode()
    mode.load_workspace(workspace(tmp_path, final_render_path=None), targets=[target_config()])
    jumps: list[tuple[str, str, str]] = []
    mode.jumpRequested.connect(lambda target, comp, layer: jumps.append((target, comp, layer)))

    mode.preflight_button.click()
    mode._jump_from_index(mode.plan_model.index(0, 0))

    assert mode.summary.state_label.text() == "Preflight: blocked"
    assert "blocking" in mode.export_button.toolTip()
    assert jumps == [("alpha", "alpha__20260525", "")]


def test_app_shell_exposes_export_mode_and_jump_switches_to_review() -> None:
    qapp()
    shell = AppShell()

    assert shell.mode_tabs.count() == 3
    assert shell.mode_tabs.tabText(2) == "Export"

    shell.mode_tabs.setCurrentWidget(shell.export_mode)
    shell._jump_to_review_context("alpha", "", "")

    assert shell.mode_tabs.currentWidget() is shell.review_edit_mode
