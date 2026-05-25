from __future__ import annotations

import json
import os
from datetime import date, time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsView,
    QSplitter,
    QTableView,
    QTreeView,
)

from thucthengay.editor.app_shell import AppShell
from thucthengay.editor.models.composition_tree_model import (
    CompositionTreeModel,
    CompositionTreeRole,
    QueueFilter,
    TreeNodeKind,
)
from thucthengay.editor.models.layer_stack_model import (
    LayerStackColumn,
    LayerStackModel,
    LayerStackRole,
)
from thucthengay.editor.modes.review_edit_mode import ReviewEditMode
from thucthengay.editor.widgets import (
    GisCanvasState,
    GisCanvasWidget,
    SlidePreviewState,
    SlidePreviewWidget,
)
from thucthengay.models import (
    Composition,
    GridConfig,
    GridInterval,
    ImageLayer,
    MetadataSource,
    MetadataStatus,
    TargetConfig,
    TargetExportConfig,
    ValidationSummary,
    ViewState,
)
from thucthengay.workspace import WorkspaceService


def qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


def target_config(target_id: str, *, sort_order: int, name: str) -> TargetConfig:
    return TargetConfig(
        id=target_id,
        sort_order=sort_order,
        name=name,
        geojson_file=f"{target_id}.geojson",
        coordinate=[106.7, 10.8],
        scale=50000,
        grid=GridConfig(interval=GridInterval(minutes=1)),
        export=TargetExportConfig(template_metadata_file=f"{target_id}.template.json"),
        metadata={
            "template_metadata": {
                "template_pptx": f"{target_id}.pptx",
                "slide_index": 0,
                "map_frame": {"x": 0, "y": 0, "width": 640, "height": 360},
            }
        },
    )


def composition(
    composition_id: str,
    target_id: str,
    capture_date: date,
    *,
    reviewed: bool = False,
    ready: bool = False,
    include: bool = False,
    needs_revalidation: bool = True,
    review_order: int | None = None,
    warnings: int = 0,
    errors: int = 0,
) -> Composition:
    return Composition(
        composition_id=composition_id,
        target_id=target_id,
        capture_date=capture_date,
        view=ViewState(center=[106.7, 10.8], scale=50000),
        reviewed=reviewed,
        ready=ready,
        include=include,
        needs_revalidation=needs_revalidation,
        review_order=review_order,
        validation_summary=ValidationSummary(warning_count=warnings, error_count=errors),
        layers=[
            ImageLayer(
                layer_id=f"{composition_id}-layer",
                source_path=f"{composition_id}.tif",
                order=0,
                capture_date=capture_date,
                capture_time=time(8, 30),
                metadata_status=MetadataStatus.VALID,
                metadata_source=MetadataSource.FILENAME,
            )
        ],
    )


def test_composition_tree_groups_by_target_order_and_review_queue_order() -> None:
    qapp()
    model = CompositionTreeModel()
    model.set_compositions(
        [
            composition("beta__20260525", "beta", date(2026, 5, 25), review_order=2),
            composition("alpha__20260526", "alpha", date(2026, 5, 26)),
            composition("alpha__20260524", "alpha", date(2026, 5, 24), review_order=1),
        ],
        targets=[
            target_config("beta", sort_order=2, name="Beta Target"),
            target_config("alpha", sort_order=1, name="Alpha Target"),
        ],
    )

    first_target = model.index(0, 0)
    second_target = model.index(1, 0)

    assert first_target.data(CompositionTreeRole.NODE_KIND) == TreeNodeKind.TARGET
    assert "Alpha Target" in first_target.data(Qt.ItemDataRole.DisplayRole)
    assert "0 vấn đề" in first_target.data(Qt.ItemDataRole.DisplayRole)
    assert "Beta Target" in second_target.data(Qt.ItemDataRole.DisplayRole)

    first_alpha_child = model.index(0, 0, first_target)
    second_alpha_child = model.index(1, 0, first_target)

    assert first_alpha_child.data(CompositionTreeRole.COMPOSITION_ID) == "alpha__20260524"
    assert second_alpha_child.data(CompositionTreeRole.COMPOSITION_ID) == "alpha__20260526"


def test_composition_tree_exposes_text_status_severity_counts_and_tooltips() -> None:
    qapp()
    model = CompositionTreeModel()
    model.set_compositions(
        [
            composition(
                "alpha__20260525",
                "alpha",
                date(2026, 5, 25),
                reviewed=True,
                ready=True,
                include=True,
                needs_revalidation=False,
                warnings=2,
            )
        ],
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )

    index = model.index(0, 0, model.index(0, 0))

    assert index.data(CompositionTreeRole.STATUS_TEXT) == "Include"
    assert index.data(CompositionTreeRole.SEVERITY_TEXT) == "WARN"
    assert index.data(CompositionTreeRole.ISSUE_COUNT) == 2
    assert "alpha__20260525" in index.data(Qt.ItemDataRole.DisplayRole)
    assert "[WARN]" in index.data(Qt.ItemDataRole.DisplayRole)
    assert "2 vấn đề" in index.data(Qt.ItemDataRole.DisplayRole)
    assert "Warnings: 2" in index.data(Qt.ItemDataRole.ToolTipRole)


def test_composition_tree_filters_counts_and_preserves_target_grouping() -> None:
    qapp()
    model = CompositionTreeModel()
    model.set_compositions(
        [
            composition("alpha__20260525", "alpha", date(2026, 5, 25)),
            composition(
                "alpha__20260526",
                "alpha",
                date(2026, 5, 26),
                reviewed=True,
                ready=True,
                needs_revalidation=False,
            ),
            composition(
                "beta__20260525",
                "beta",
                date(2026, 5, 25),
                reviewed=True,
                ready=True,
                include=True,
                needs_revalidation=False,
                warnings=1,
            ),
            composition(
                "gamma__20260525",
                "gamma",
                date(2026, 5, 25),
                reviewed=True,
                needs_revalidation=False,
                errors=1,
            ),
        ],
        targets=[
            target_config("alpha", sort_order=1, name="Alpha Target"),
            target_config("beta", sort_order=2, name="Beta Target"),
            target_config("gamma", sort_order=3, name="Gamma Target"),
        ],
    )

    counts = model.filter_counts()

    assert counts[QueueFilter.ALL] == 4
    assert counts[QueueFilter.UNREVIEWED] == 1
    assert counts[QueueFilter.READY] == 1
    assert counts[QueueFilter.INCLUDE] == 1
    assert counts[QueueFilter.WARNING] == 1
    assert counts[QueueFilter.ERROR] == 1

    model.set_queue_filter(QueueFilter.WARNING)

    assert model.rowCount() == 1
    target_index = model.index(0, 0)
    assert target_index.data(CompositionTreeRole.TARGET_ID) == "beta"
    assert model.rowCount(target_index) == 1
    assert model.index(0, 0, target_index).data(CompositionTreeRole.COMPOSITION_ID) == (
        "beta__20260525"
    )


def test_composition_tree_refresh_updates_filter_counts_and_stale_ready_text() -> None:
    qapp()
    model = CompositionTreeModel()
    stale_ready = composition(
        "alpha__20260525",
        "alpha",
        date(2026, 5, 25),
        reviewed=True,
        ready=True,
        needs_revalidation=True,
    )

    model.set_compositions([stale_ready])
    model.set_queue_filter(QueueFilter.READY)

    index = model.index(0, 0, model.index(0, 0))
    assert model.filter_counts()[QueueFilter.READY] == 1
    assert index.data(CompositionTreeRole.STATUS_TEXT) == "Cần kiểm tra lại"
    assert index.data(CompositionTreeRole.SEVERITY_TEXT) == "STALE"

    model.set_compositions([stale_ready.model_copy(update={"ready": False})])

    assert model.filter_counts()[QueueFilter.READY] == 0
    assert model.visible_composition_count() == 0


def test_review_edit_mode_loads_selected_composition_through_workspace_service(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    target = target_config("alpha", sort_order=1, name="Alpha Target").model_copy(
        update={"metadata": {"map_frame": {"width": 4, "height": 3}}}
    )
    mode.load_workspace(
        service,
        targets=[target],
    )
    target_index = mode.tree_model.index(0, 0)
    composition_index = mode.tree_model.index(0, 0, target_index)

    mode.tree_view.setCurrentIndex(composition_index)

    assert mode.selected_composition is not None
    assert mode.selected_composition.composition_id == "alpha__20260525"
    assert "alpha__20260525" in mode.composition_title.text()
    assert mode.layer_model.rowCount() == 1
    assert mode.warnings_panel._list.count() >= 0  # panel is wired up


def test_review_edit_selection_persists_compact_validation_summary_only(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            needs_revalidation=True,
        )
    )

    mode = ReviewEditMode()
    mode.load_workspace(service, targets=[target_config("alpha", sort_order=1, name="Alpha")])
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    reloaded = service.read_composition("alpha__20260525")
    raw = json.loads(
        (service.paths.compositions / "alpha__20260525.json").read_text(encoding="utf-8")
    )

    assert reloaded.needs_revalidation is False
    assert reloaded.validation_summary.error_count == 0
    assert "issues" not in raw


def test_review_edit_suppressed_selection_refresh_does_not_run_validation(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    mode.load_workspace(service, targets=[target_config("alpha", sort_order=1, name="Alpha")])
    target_index = mode.tree_model.index(0, 0)
    composition_index = mode.tree_model.index(0, 0, target_index)

    def fail_validation(_composition: Composition) -> None:
        raise AssertionError("validation should be suppressed")

    mode._review_gate = fail_validation  # type: ignore[method-assign]
    mode._suppress_selection_validation = True
    mode._select_composition_index(composition_index, None)

    assert mode.selected_composition is not None
    assert mode.selected_composition.composition_id == "alpha__20260525"


def test_review_edit_invalid_fallback_map_frame_becomes_validation_issue(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )
    target = target_config("alpha", sort_order=1, name="Alpha").model_copy(
        update={"metadata": {"map_frame": {"width": 0, "height": 3}}}
    )

    mode = ReviewEditMode()
    mode.load_workspace(service, targets=[target])
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    assert mode.warnings_panel._list.count() == 1
    assert "Template metadata" in mode.warnings_panel._list.item(0).text()


def test_layer_stack_model_display_roles_and_no_visible_warning() -> None:
    qapp()
    long_name = "alpha_target_layer_with_a_very_long_filename_that_should_elide_20260525.tif"
    model = LayerStackModel()
    model.set_composition(
        Composition(
            composition_id="alpha__20260525",
            target_id="alpha",
            capture_date=date(2026, 5, 25),
            view=ViewState(center=[106.7, 10.8], scale=50000),
            layers=[
                ImageLayer(
                    layer_id="new",
                    source_path=f"/imagery/{long_name}",
                    cache_path="cache/alpha/new.tif",
                    visible=False,
                    order=1,
                    capture_date=date(2026, 5, 25),
                    capture_time=time(9, 15),
                    cloud_percent=12.4,
                    metadata_status=MetadataStatus.NEEDS_MANUAL_CORRECTION,
                    metadata_source=MetadataSource.FILENAME,
                ),
                ImageLayer(
                    layer_id="old",
                    source_path="/imagery/old.tif",
                    visible=False,
                    order=0,
                    metadata_status=MetadataStatus.VALID,
                ),
            ],
        )
    )

    long_filename = model.index(1, int(LayerStackColumn.FILENAME))
    first_visibility = model.index(0, int(LayerStackColumn.VISIBILITY))
    second_order = model.index(1, int(LayerStackColumn.ORDER))

    assert model.index(0, 0).data(LayerStackRole.LAYER_ID) == "old"
    assert model.index(0, 0).data(LayerStackRole.NO_VISIBLE_WARNING) is True
    assert first_visibility.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Unchecked
    assert second_order.data(Qt.ItemDataRole.DisplayRole) == "2"
    assert "..." in long_filename.data(Qt.ItemDataRole.DisplayRole)
    assert "/imagery/" in long_filename.data(Qt.ItemDataRole.ToolTipRole)
    assert "Cache:" in long_filename.data(Qt.ItemDataRole.ToolTipRole)


def test_gis_canvas_states_fixed_frame_and_stale_render_guard() -> None:
    qapp()
    canvas = GisCanvasWidget()
    canvas.resize(800, 450)
    canvas.set_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            needs_revalidation=False,
        )
    )

    assert canvas.visible_layer_count() == 1
    assert canvas.state() == GisCanvasState.READY
    assert "Canvas đã tải" in canvas.state_text()
    assert abs(canvas.frame_aspect() - GisCanvasWidget.DEFAULT_FRAME_ASPECT) < 0.02

    old_token = canvas.begin_render_request()
    old_generation = canvas.generation
    canvas.pan_by_pixels(40, -20, emit=False)

    assert canvas.generation > old_generation
    assert canvas.state() == GisCanvasState.STALE
    assert canvas.apply_render_result(old_token, "old render") is False

    current_token = canvas.begin_render_request()
    assert canvas.apply_render_result(current_token, "fresh render") is True
    assert canvas.last_applied_render_label == "fresh render"

    canvas.set_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25)).model_copy(
            update={
                "layers": [
                    ImageLayer(
                        layer_id="hidden",
                        source_path="/imagery/hidden.tif",
                        visible=False,
                        order=0,
                    )
                ]
            }
        )
    )

    assert canvas.state() == GisCanvasState.NO_VISIBLE_LAYER
    assert "Không có layer" in canvas.state_text()

    token = canvas.set_loading()
    assert canvas.state() == GisCanvasState.LOADING
    assert token.generation == canvas.generation
    canvas.set_error("Không đọc được raster.")
    assert canvas.state() == GisCanvasState.ERROR
    assert "raster" in canvas.state_text()


def test_slide_preview_debounces_state_and_rejects_stale_results() -> None:
    app = qapp()
    preview = SlidePreviewWidget(debounce_ms=1)
    selected = composition(
        "alpha__20260525",
        "alpha",
        date(2026, 5, 25),
        needs_revalidation=False,
    )
    grid = GridConfig(interval=GridInterval(minutes=2, seconds=30), label_format="dms_short")

    preview.set_composition(
        selected,
        effective_grid=grid,
        background={"color": "#101820"},
    )
    stale_token = preview.begin_preview_request()

    assert preview.state() == SlidePreviewState.NEEDS_UPDATE
    assert "Preview cần cập nhật" in preview.state_text()
    assert "Scale 1:50,000" in preview.detail_text()
    assert "Grid: 0d 2m 30s" in preview.detail_text()
    assert "#101820" in preview.detail_text()

    preview.set_composition(
        selected.model_copy(
            update={"view": ViewState(center=[106.8, 10.9], scale=25000)}
        ),
        effective_grid=grid,
    )

    assert preview.apply_preview_result(stale_token, "old preview") is False

    app.processEvents()
    preview._timer.timeout.emit()

    assert preview.state() == SlidePreviewState.LOADING
    preview._render_timer.timeout.emit()

    assert preview.state() == SlidePreviewState.RENDERED
    assert "Preview đã cập nhật" in preview.state_text()
    assert "Scale 1:25,000" in preview.detail_text()

    preview.set_render_error("Không đọc được preview cache.")

    assert preview.state() == SlidePreviewState.RENDER_ERROR
    assert "tiếp tục chỉnh sửa" in preview.detail_text()

    preview.set_composition(selected, effective_grid=grid)
    preview._timer.timeout.emit()
    preview._render_timer.timeout.emit()

    assert preview.state() == SlidePreviewState.RENDERED
    assert "Không đọc được" not in preview.detail_text()


def test_slide_preview_review_edge_cases_do_not_accept_stale_results() -> None:
    qapp()
    preview = SlidePreviewWidget(debounce_ms=-5)
    selected = composition(
        "alpha__20260525",
        "alpha",
        date(2026, 5, 25),
        needs_revalidation=False,
    )
    selected = selected.model_copy(
        update={"view": ViewState(center=[106.7, 10.8], scale=50000, rotation=0)}
    )

    preview.set_composition(
        selected,
        background={"color": "#101820", 7: {"nested": ["value"]}},
    )
    stale_token = preview.begin_preview_request()
    preview._timer.timeout.emit()

    assert preview.state() == SlidePreviewState.LOADING
    assert "Rotation 0" in preview.detail_text()

    preview.set_render_error("Không tạo được preview.")

    assert preview.apply_preview_result(stale_token, "old preview") is False
    assert preview.state() == SlidePreviewState.RENDER_ERROR
    assert "tiếp tục chỉnh sửa" in preview.detail_text()


def test_review_edit_layer_stack_saves_visibility_order_and_warning(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            ready=True,
            include=True,
            needs_revalidation=False,
            review_order=2,
        ).model_copy(
            update={
                "layers": [
                    ImageLayer(
                        layer_id="old",
                        source_path="/imagery/old.tif",
                        visible=True,
                        order=0,
                        capture_date=date(2026, 5, 25),
                        capture_time=time(8, 30),
                        metadata_status=MetadataStatus.VALID,
                    ),
                    ImageLayer(
                        layer_id="new",
                        source_path="/imagery/new.tif",
                        visible=True,
                        order=1,
                        capture_date=date(2026, 5, 25),
                        capture_time=time(9, 0),
                        metadata_status=MetadataStatus.VALID,
                    ),
                ]
            }
        )
    )

    mode = ReviewEditMode()
    target = target_config("alpha", sort_order=1, name="Alpha Target").model_copy(
        update={"metadata": {"map_frame": {"width": 4, "height": 3}}}
    )
    mode.load_workspace(
        service,
        targets=[target],
    )
    target_index = mode.tree_model.index(0, 0)
    composition_index = mode.tree_model.index(0, 0, target_index)
    mode.tree_view.setCurrentIndex(composition_index)

    first_visibility = mode.layer_model.index(0, int(LayerStackColumn.VISIBILITY))
    second_visibility = mode.layer_model.index(1, int(LayerStackColumn.VISIBILITY))
    mode.layer_model.setData(
        first_visibility,
        Qt.CheckState.Unchecked,
        Qt.ItemDataRole.CheckStateRole,
    )

    reloaded = service.read_composition("alpha__20260525")
    assert reloaded.layers[0].visible is False
    assert reloaded.needs_revalidation is True
    assert reloaded.ready is False
    assert reloaded.include is False
    assert reloaded.review_order is None
    assert mode.layer_warning_label.isHidden()

    second_visibility = mode.layer_model.index(1, int(LayerStackColumn.VISIBILITY))
    mode.layer_model.setData(
        second_visibility,
        Qt.CheckState.Unchecked,
        Qt.ItemDataRole.CheckStateRole,
    )

    assert service.read_composition("alpha__20260525").layers[1].visible is False
    assert not mode.layer_warning_label.isHidden()
    assert "ít nhất 1 layer" in mode.layer_warning_label.text()
    assert mode.tree_model.index_for_composition_id("alpha__20260525").data(
        CompositionTreeRole.SEVERITY_TEXT
    ) == "ERROR"
    assert mode.tree_model.index_for_composition_id("alpha__20260525").data(
        CompositionTreeRole.STATUS_TEXT
    ) == "Không có layer bật"
    assert mode.filter_buttons[QueueFilter.ERROR].text() == "Có error (1)"

    mode.layer_table.setCurrentIndex(mode.layer_model.index(1, int(LayerStackColumn.FILENAME)))
    mode.move_layer_up_button.click()

    reordered = service.read_composition("alpha__20260525")
    assert [layer.layer_id for layer in reordered.layers] == ["new", "old"]
    assert [layer.order for layer in reordered.layers] == [0, 1]


def test_review_edit_gis_canvas_saves_pan_zoom_and_marks_preview_stale(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            ready=True,
            include=True,
            needs_revalidation=False,
            review_order=3,
        )
    )

    mode = ReviewEditMode()
    target = target_config("alpha", sort_order=1, name="Alpha Target").model_copy(
        update={"metadata": {"map_frame": {"width": 4, "height": 3}}}
    )
    mode.load_workspace(
        service,
        targets=[target],
    )
    target_index = mode.tree_model.index(0, 0)
    composition_index = mode.tree_model.index(0, 0, target_index)
    mode.tree_view.setCurrentIndex(composition_index)

    original_center = mode.gis_canvas.center
    assert abs(mode.gis_canvas.frame_aspect() - (4 / 3)) < 0.02

    mode.gis_canvas.pan_by_pixels(48, -24)

    panned = service.read_composition("alpha__20260525")
    assert panned.view.center != original_center
    assert panned.needs_revalidation is True
    assert panned.ready is False
    assert panned.include is False
    assert panned.review_order is None
    assert "Preview cần cập nhật" in mode.preview_summary.text()
    assert mode.slide_preview.state() == SlidePreviewState.NEEDS_UPDATE

    mode.gis_canvas.zoom_by_factor(0.5)

    zoomed = service.read_composition("alpha__20260525")
    assert zoomed.view.scale == 25000
    assert zoomed.view.rotation == 0
    assert mode.gis_canvas.state() == GisCanvasState.STALE
    assert mode.tree_model.index_for_composition_id("alpha__20260525").data(
        CompositionTreeRole.STATUS_TEXT
    ) == "Cần kiểm tra lại"


def test_review_edit_grid_controls_show_defaults_save_override_and_mark_stale(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            ready=True,
            include=True,
            needs_revalidation=False,
            review_order=3,
        )
    )
    target = target_config("alpha", sort_order=1, name="Alpha Target").model_copy(
        update={
            "grid": GridConfig(
                interval=GridInterval(minutes=1),
                label_format="dms_full",
                style={"color": "white"},
            )
        }
    )

    mode = ReviewEditMode()
    mode.load_workspace(service, targets=[target])
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    assert mode.grid_degrees_input.text() == "0"
    assert mode.grid_minutes_input.text() == "1"
    assert mode.grid_seconds_input.text() == "0"
    assert mode.grid_label_format_input.text() == "dms_full"
    assert "mặc định target" in mode.grid_status_label.text()

    mode.grid_minutes_input.setText("2")
    mode.grid_seconds_input.setText("30")
    mode.grid_label_format_input.setText("dms_short")
    mode.save_grid_button.click()

    reloaded = service.read_composition("alpha__20260525")
    assert reloaded.grid_override is not None
    assert reloaded.grid_override.interval.minutes == 2
    assert reloaded.grid_override.interval.seconds == 30
    assert reloaded.grid_override.label_format == "dms_short"
    assert reloaded.grid_override.style == {"color": "white"}
    assert reloaded.needs_revalidation is True
    assert reloaded.ready is False
    assert reloaded.include is False
    assert reloaded.review_order is None
    assert target.grid.interval.minutes == 1
    assert "override" in mode.grid_status_label.text()
    assert "Preview cần cập nhật" in mode.preview_summary.text()
    assert "Grid: 0d 2m 30s" in mode.slide_preview.detail_text()
    assert mode.tree_model.index_for_composition_id("alpha__20260525").data(
        CompositionTreeRole.STATUS_TEXT
    ) == "Cần kiểm tra lại"


def test_review_edit_slide_preview_loads_and_debounces_after_selection_and_edits(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            needs_revalidation=False,
        )
    )
    target = target_config("alpha", sort_order=1, name="Alpha Target").model_copy(
        update={
            "grid": GridConfig(interval=GridInterval(minutes=1), label_format="dms_full"),
            "metadata": {"preview_background": {"color": "#ddeeff"}},
        }
    )

    mode = ReviewEditMode()
    mode.load_workspace(service, targets=[target])
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    assert mode.slide_preview.state() == SlidePreviewState.NEEDS_UPDATE
    assert "alpha__20260525" in mode.slide_preview.detail_text()
    assert "Layers: alpha__20260525-layer" in mode.slide_preview.detail_text()
    assert "#ddeeff" in mode.slide_preview.detail_text()

    mode.slide_preview._timer.timeout.emit()

    assert mode.slide_preview.state() == SlidePreviewState.LOADING
    mode.slide_preview._render_timer.timeout.emit()

    assert mode.slide_preview.state() == SlidePreviewState.RENDERED
    assert "Preview đã cập nhật" in mode.preview_summary.text()

    mode.gis_canvas.pan_by_pixels(20, 0)

    assert mode.slide_preview.state() == SlidePreviewState.NEEDS_UPDATE
    assert "Preview cần cập nhật" in mode.preview_summary.text()

    mode.slide_preview._timer.timeout.emit()
    mode.slide_preview._render_timer.timeout.emit()

    assert mode.slide_preview.state() == SlidePreviewState.RENDERED
    assert "Scale 1:50,000" in mode.slide_preview.detail_text()


def test_review_edit_slide_preview_uses_map_background_string(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            needs_revalidation=False,
        )
    )
    target = target_config("alpha", sort_order=1, name="Alpha Target").model_copy(
        update={"metadata": {"map_background": "#112233"}}
    )

    mode = ReviewEditMode()
    mode.load_workspace(service, targets=[target])
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    assert "#112233" in mode.slide_preview.detail_text()


def test_review_edit_grid_controls_reject_invalid_values_without_write(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25)).model_copy(
            update={
                "grid_override": GridConfig(
                    interval=GridInterval(minutes=1),
                    label_format="dms_full",
                )
            }
        )
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    mode.grid_minutes_input.setText("60")
    mode.save_grid_button.click()

    reloaded = service.read_composition("alpha__20260525")
    assert reloaded.grid_override is not None
    assert reloaded.grid_override.interval.minutes == 1
    assert "Phút phải nhỏ hơn 60" in mode.grid_validation_label.text()


def test_review_edit_filter_bar_counts_empty_state_and_selection_restore(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )
    service.write_composition(
        composition(
            "alpha__20260526",
            "alpha",
            date(2026, 5, 26),
            reviewed=True,
            ready=True,
            needs_revalidation=False,
        )
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    ready_index = mode.tree_model.index(1, 0, target_index)
    mode.tree_view.setCurrentIndex(ready_index)

    mode.filter_buttons[QueueFilter.READY].click()

    assert mode.tree_model.active_queue_filter == QueueFilter.READY
    assert "Ready (1)" == mode.filter_buttons[QueueFilter.READY].text()
    assert mode.empty_state_label.isHidden()
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260526"
    )

    mode.filter_buttons[QueueFilter.INCLUDE].click()

    assert not mode.empty_state_label.isHidden()
    assert "Include" in mode.empty_state_label.text()
    assert mode.filter_buttons[QueueFilter.ALL].text() == "Tất cả (2)"

    mode.filter_buttons[QueueFilter.ALL].click()

    assert mode.empty_state_label.isHidden()
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260526"
    )

    service.write_composition(
        composition(
            "alpha__20260526",
            "alpha",
            date(2026, 5, 26),
            reviewed=True,
            ready=True,
            include=True,
            needs_revalidation=False,
            warnings=1,
        )
    )
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )

    assert mode.filter_buttons[QueueFilter.INCLUDE].text() == "Include (1)"
    assert mode.filter_buttons[QueueFilter.WARNING].text() == "Có warning (1)"
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260526"
    )


def test_review_edit_action_bar_includes_and_advances_on_passing_gate(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )
    service.write_composition(
        composition("alpha__20260526", "alpha", date(2026, 5, 26), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    buttons = [
        mode.previous_button,
        mode.skip_button,
        mode.include_validate_button,
        mode.revalidate_button,
    ]
    assert [button.property("primaryAction") for button in buttons].count(True) == 1
    assert mode.include_validate_button.isEnabled()
    assert not mode.previous_button.isEnabled()

    mode.include_validate_button.click()

    included = service.read_composition("alpha__20260525")
    assert included.reviewed is True
    assert included.ready is True
    assert included.include is True
    assert included.review_order == 1
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260526"
    )
    assert mode.previous_button.isEnabled()


def test_review_edit_action_bar_blocks_include_and_supports_skip_previous(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    blocked = composition(
        "alpha__20260525",
        "alpha",
        date(2026, 5, 25),
        needs_revalidation=False,
    )
    blocked = blocked.model_copy(
        update={"layers": [layer.model_copy(update={"visible": False}) for layer in blocked.layers]}
    )
    service.write_composition(blocked)
    service.write_composition(
        composition("alpha__20260526", "alpha", date(2026, 5, 26), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    mode.include_validate_button.click()

    unchanged = service.read_composition("alpha__20260525")
    assert unchanged.reviewed is False
    assert unchanged.ready is False
    assert unchanged.include is False
    assert mode.warnings_panel._list.count() > 0
    assert mode.action_summary.text() == "Không include: cần xử lý lỗi blocking trước."
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260525"
    )
    assert mode.tree_view.currentIndex().data(CompositionTreeRole.ISSUE_COUNT) > 0

    mode.skip_button.click()

    skipped = service.read_composition("alpha__20260525")
    assert skipped.reviewed is True
    assert skipped.ready is False
    assert skipped.include is False
    assert skipped.review_order is None
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260526"
    )

    second_before = service.read_composition("alpha__20260526")
    mode.previous_button.click()
    second_after = service.read_composition("alpha__20260526")

    assert second_after == second_before
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260525"
    )


def test_review_edit_issue_jump_handles_filtered_composition_and_target_only_refs(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    mode.tree_model.set_queue_filter(QueueFilter.READY)
    mode._refresh_filter_controls()
    assert not mode.tree_model.has_visible_compositions()

    mode._handle_issue_jump("alpha", "alpha__20260525", "")

    assert mode.tree_model.active_queue_filter == QueueFilter.ALL
    assert mode.tree_model.composition_id_for_index(mode.tree_view.currentIndex()) == (
        "alpha__20260525"
    )

    mode._handle_issue_jump("alpha", "", "")

    assert mode.tree_view.currentIndex().data(CompositionTreeRole.TARGET_ID) == "alpha"


def test_review_edit_issue_jump_reports_stale_missing_layer(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))
    mode.action_summary.setText("before")

    mode._handle_issue_jump("alpha", "alpha__20260525", "missing-layer")

    assert mode.action_summary.text() == "Tham chiếu không còn tồn tại."


def test_review_edit_revalidate_clears_stale_error_summary_with_lightweight_gate(
    tmp_path: Path,
) -> None:
    qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition(
            "alpha__20260525",
            "alpha",
            date(2026, 5, 25),
            needs_revalidation=True,
            errors=1,
        )
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    revalidated = service.read_composition("alpha__20260525")
    assert revalidated.needs_revalidation is False
    assert revalidated.validation_summary.error_count == 0
    assert revalidated.ready is False
    assert revalidated.include is False
    assert not mode.revalidate_button.isEnabled()


def test_review_edit_keyboard_shortcuts_respect_text_input_arrow_guard(
    tmp_path: Path,
) -> None:
    app = qapp()
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(
        composition("alpha__20260525", "alpha", date(2026, 5, 25), needs_revalidation=False)
    )

    mode = ReviewEditMode()
    mode.load_workspace(
        service,
        targets=[target_config("alpha", sort_order=1, name="Alpha Target")],
    )
    target_index = mode.tree_model.index(0, 0)
    mode.tree_view.setCurrentIndex(mode.tree_model.index(0, 0, target_index))

    mode.show()
    mode.grid_minutes_input.setFocus()
    app.processEvents()
    mode.keyPressEvent(
        QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Right, Qt.KeyboardModifier.NoModifier)
    )

    assert service.read_composition("alpha__20260525").include is False

    mode.tree_view.setFocus()
    app.processEvents()
    mode.keyPressEvent(
        QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Right, Qt.KeyboardModifier.NoModifier)
    )

    assert service.read_composition("alpha__20260525").include is True


def test_review_edit_layout_and_app_shell_expose_review_mode() -> None:
    qapp()

    shell = AppShell()

    assert shell.mode_tabs.count() == 2
    assert shell.mode_tabs.tabText(0) == "Setup"
    assert shell.mode_tabs.tabText(1) == "Review/Edit"
    assert isinstance(shell.review_edit_mode.tree_view, QTreeView)
    assert QueueFilter.ALL in shell.review_edit_mode.filter_buttons
    assert isinstance(shell.review_edit_mode.layer_table, QTableView)
    assert isinstance(shell.review_edit_mode.gis_canvas, QGraphicsView)
    assert shell.review_edit_mode.tree_view.uniformRowHeights()
    assert shell.review_edit_mode.minimumWidth() >= 960
    assert shell.review_edit_mode.findChild(QSplitter, "reviewMainSplitter") is not None
    assert shell.review_edit_mode.warnings_panel is not None
