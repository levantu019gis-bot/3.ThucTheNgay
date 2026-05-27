from __future__ import annotations

import ast
from pathlib import Path

import numpy as np

from thucthengay.jobs import (
    JobState,
    PreviewRenderController,
    PreviewRenderQuality,
    run_preview_render_job,
)
from thucthengay.models import GridConfig, GridInterval, Issue
from thucthengay.models.template import MapFrame
from thucthengay.render.raster import RasterRenderResult, RenderError
from thucthengay.render.spec import GeoWindow, RenderBackground, RenderLayerRef, RenderSpec


def _spec(
    *,
    composition_id: str = "alpha__20260525",
    width: int = 1200,
    height: int = 800,
) -> RenderSpec:
    return RenderSpec(
        composition_id=composition_id,
        target_id="alpha",
        output_width=width,
        output_height=height,
        view_center=[106.7, 10.8],
        view_scale=50000,
        map_frame=MapFrame(x=0, y=0, width=640, height=360),
        map_frame_aspect=16 / 9,
        geo_window=GeoWindow(
            min_lon=106.5,
            min_lat=10.6,
            max_lon=106.9,
            max_lat=11.0,
        ),
        visible_layers=[
            RenderLayerRef(
                layer_id="L1",
                source_path="L1.tif",
                cache_path="cache/L1.tif",
                order=0,
            )
        ],
        grid=GridConfig(interval=GridInterval(minutes=1)),
        background=RenderBackground(color="#FFFFFF"),
        template_metadata_file="alpha.template.json",
        template_pptx="alpha.pptx",
        slide_index=0,
    )


def test_preview_controller_schedules_interactive_first_and_settled_after_debounce() -> None:
    controller = PreviewRenderController(
        debounce_ms=175,
        interactive_max_width=300,
        settled_max_width=900,
    )

    plan = controller.request_preview(_spec(width=1200, height=800))

    assert plan.settled_delay_ms == 175
    assert plan.interactive.quality == PreviewRenderQuality.INTERACTIVE_LOW_RES
    assert plan.settled.quality == PreviewRenderQuality.SETTLED_HIGH_RES
    assert plan.interactive.revision == plan.settled.revision == 1
    assert plan.interactive.spec.output_width == 300
    assert plan.interactive.spec.output_height == 200
    assert plan.settled.spec.output_width == 900
    assert plan.settled.spec.output_height == 600
    assert plan.interactive.spec.geo_window == plan.settled.spec.geo_window
    assert plan.interactive.spec.view_center == plan.settled.spec.view_center
    assert plan.interactive.spec.view_scale == plan.settled.spec.view_scale


def test_preview_controller_rejects_stale_results_after_new_revision() -> None:
    controller = PreviewRenderController(debounce_ms=10)
    first = controller.request_preview(_spec(composition_id="alpha__20260525"))
    second = controller.request_preview(_spec(composition_id="alpha__20260526"))

    old_result = run_preview_render_job(
        first.interactive,
        render=lambda spec, is_cancelled=None: RasterRenderResult(
            canvas=np.zeros((spec.output_height, spec.output_width, 3), dtype=np.uint8)
        ),
    )
    current_result = run_preview_render_job(
        second.interactive,
        render=lambda spec, is_cancelled=None: RasterRenderResult(
            canvas=np.ones((spec.output_height, spec.output_width, 3), dtype=np.uint8)
        ),
    )

    assert controller.accepts_result(old_result) is False
    assert controller.accepts_result(current_result) is True


def test_preview_controller_rejects_late_low_res_after_settled_result() -> None:
    controller = PreviewRenderController(debounce_ms=10)
    plan = controller.request_preview(_spec())
    settled_result = run_preview_render_job(
        plan.settled,
        render=lambda spec, is_cancelled=None: RasterRenderResult(
            canvas=np.ones((spec.output_height, spec.output_width, 3), dtype=np.uint8)
        ),
    )
    late_interactive_result = run_preview_render_job(
        plan.interactive,
        render=lambda spec, is_cancelled=None: RasterRenderResult(
            canvas=np.zeros((spec.output_height, spec.output_width, 3), dtype=np.uint8)
        ),
    )

    assert controller.accepts_result(settled_result) is True
    assert controller.accepts_result(late_interactive_result) is False


def test_preview_render_job_emits_progress_and_success_payload() -> None:
    events = []
    request = PreviewRenderController(debounce_ms=10).request_preview(_spec()).interactive

    result = run_preview_render_job(
        request,
        publish=events.append,
        render=lambda spec, is_cancelled=None: RasterRenderResult(
            canvas=np.full((spec.output_height, spec.output_width, 3), 7, dtype=np.uint8)
        ),
    )

    assert [event.state for event in events] == [JobState.RUNNING, JobState.SUCCESS]
    assert events[0].stage == "preview.interactive_low_res"
    assert result.state == JobState.SUCCESS
    assert result.job_id == request.job_id
    assert result.quality == PreviewRenderQuality.INTERACTIVE_LOW_RES
    assert result.canvas is not None
    assert result.output_width == request.spec.output_width
    assert result.output_height == request.spec.output_height


def test_preview_render_error_becomes_structured_failure_payload() -> None:
    request = PreviewRenderController(debounce_ms=10).request_preview(_spec()).settled
    def render_failure(_spec: RenderSpec, is_cancelled=None) -> RasterRenderResult:
        raise RenderError(
            [
                Issue.model_validate(
                    {
                        "issue_id": "render.raster.unreadable",
                        "severity": "error",
                        "scope": "render",
                        "message": "Khong doc duoc raster.",
                        "remediation": "Kiem tra file anh roi render lai.",
                    }
                )
            ]
        )

    result = run_preview_render_job(request, render=render_failure)

    assert result.state == JobState.ERROR
    assert result.canvas is None
    assert result.issues[0].issue_id == "render.raster.unreadable"
    assert "Kiem tra file anh" in result.message


def test_preview_job_contracts_do_not_import_qt_or_editor_modules() -> None:
    source = Path("src/thucthengay/jobs/render_job.py")
    tree = ast.parse(source.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    assert not any(name == "PySide6" or name.startswith("PySide6.") for name in imported)
    assert not any(
        name == "thucthengay.editor" or name.startswith("thucthengay.editor.")
        for name in imported
    )
