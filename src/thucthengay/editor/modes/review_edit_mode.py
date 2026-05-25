"""Review/Edit workstation mode."""

from __future__ import annotations

from pydantic import ValidationError
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSplitter,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from thucthengay.editor.models.composition_tree_model import (
    CompositionTreeModel,
    QueueFilter,
    queue_filter_label,
)
from thucthengay.editor.models.layer_stack_model import LayerStackColumn, LayerStackModel
from thucthengay.editor.widgets import GisCanvasWidget
from thucthengay.models import Composition, TargetConfig
from thucthengay.workspace import WorkspaceError, WorkspaceService


class ReviewEditMode(QWidget):
    """Desktop Review/Edit layout and target-composition navigator."""

    compositionSelected = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("reviewEditMode")
        self.setMinimumSize(960, 560)
        self._workspace_service: WorkspaceService | None = None
        self._targets: list[TargetConfig] | None = None
        self.selected_composition: Composition | None = None

        self.tree_model = CompositionTreeModel(self)
        self.tree_view = QTreeView()
        self.tree_view.setObjectName("reviewCompositionTree")
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.setMinimumWidth(280)
        self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.filter_button_group = QButtonGroup(self)
        self.filter_button_group.setExclusive(True)
        self.filter_buttons: dict[QueueFilter, QPushButton] = {}
        for queue_filter in QueueFilter:
            button = QPushButton(queue_filter_label(queue_filter))
            button.setObjectName(f"queueFilter_{queue_filter.value}")
            button.setCheckable(True)
            button.clicked.connect(
                lambda _checked=False, selected_filter=queue_filter: self._apply_queue_filter(
                    selected_filter
                )
            )
            self.filter_button_group.addButton(button)
            self.filter_buttons[queue_filter] = button
        self.filter_buttons[QueueFilter.ALL].setChecked(True)

        self.empty_state_label = QLabel("Không có composition khớp bộ lọc hiện tại.")
        self.empty_state_label.setObjectName("reviewQueueEmptyState")
        self.empty_state_label.setWordWrap(True)
        self.empty_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state_label.setVisible(False)

        self.composition_title = QLabel("Chưa chọn composition")
        self.composition_title.setObjectName("reviewCompositionTitle")
        self.composition_title.setWordWrap(True)

        self.layer_model = LayerStackModel(self)
        self.layer_table = QTableView()
        self.layer_table.setObjectName("reviewLayerStackTable")
        self.layer_table.setModel(self.layer_model)
        self.layer_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.layer_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.layer_table.setAlternatingRowColors(True)
        self.layer_table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.layer_table.verticalHeader().setVisible(False)
        self.layer_table.verticalHeader().setDefaultSectionSize(28)
        self.layer_table.setMinimumHeight(156)
        layer_header = self.layer_table.horizontalHeader()
        layer_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layer_header.setSectionResizeMode(
            int(LayerStackColumn.FILENAME),
            QHeaderView.ResizeMode.Stretch,
        )

        self.move_layer_up_button = QPushButton("Lên")
        self.move_layer_up_button.setObjectName("reviewLayerMoveUp")
        self.move_layer_up_button.clicked.connect(lambda: self._move_selected_layer(-1))
        self.move_layer_down_button = QPushButton("Xuống")
        self.move_layer_down_button.setObjectName("reviewLayerMoveDown")
        self.move_layer_down_button.clicked.connect(lambda: self._move_selected_layer(1))

        self.layer_warning_label = QLabel("Không còn layer nào đang bật. Cần bật ít nhất 1 layer.")
        self.layer_warning_label.setObjectName("reviewLayerStackWarning")
        self.layer_warning_label.setWordWrap(True)
        self.layer_warning_label.setVisible(False)

        self.preview_summary = QLabel("Slide preview sẽ hiển thị ở story 3.6.")
        self.preview_summary.setObjectName("reviewPreviewSummary")
        self.preview_summary.setWordWrap(True)

        self.gis_canvas = GisCanvasWidget()
        self.gis_canvas.viewEditCompleted.connect(self._persist_canvas_view)

        self.action_summary = QLabel("Review actions: Trước | Skip | Include/Validate")
        self.action_summary.setObjectName("reviewActionSummary")
        self.action_summary.setWordWrap(True)

        self.warnings_summary = QLabel("Warnings panel sẽ hiển thị validation issue.")
        self.warnings_summary.setObjectName("reviewWarningsSummary")
        self.warnings_summary.setWordWrap(True)

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setObjectName("reviewMainSplitter")
        self.main_splitter.addWidget(left_panel)
        self.main_splitter.addWidget(right_panel)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, False)
        self.main_splitter.setSizes([360, 920])

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        layout.addWidget(self.main_splitter)

        selection_model = self.tree_view.selectionModel()
        if selection_model is not None:
            selection_model.currentChanged.connect(self._select_composition_index)
        self.layer_model.dataChanged.connect(self._persist_layer_visibility)

    def load_workspace(
        self,
        workspace_service: WorkspaceService,
        *,
        targets: list[TargetConfig] | None = None,
    ) -> None:
        """Load composition navigation from a workspace service."""
        selected_id = self._current_or_selected_composition_id()
        self._workspace_service = workspace_service
        self._targets = list(targets) if targets is not None else None
        compositions = workspace_service.list_compositions()
        self.tree_model.set_compositions(compositions, targets=targets)
        self.tree_view.expandAll()
        self._refresh_filter_controls()
        self._restore_selection(selected_id)

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setMinimumWidth(320)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(8)
        layout.addWidget(QLabel("Composition queue"))
        layout.addLayout(self._filter_bar_layout())
        layout.addWidget(self.tree_view, 3)
        layout.addWidget(self.empty_state_label)
        layout.addWidget(self._build_layer_panel(), 2)
        layout.addWidget(self._panel_frame("Slide preview", self.preview_summary), 1)
        return panel

    def _filter_bar_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(4)
        for queue_filter in QueueFilter:
            layout.addWidget(self.filter_buttons[queue_filter])
        layout.addStretch(1)
        return layout

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setMinimumWidth(580)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(self.composition_title)
        layout.addWidget(self._panel_frame("GIS editor", self.gis_canvas), 4)
        layout.addLayout(self._review_action_layout())
        layout.addWidget(self._panel_frame("Warnings", self.warnings_summary), 1)
        return panel

    def _review_action_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        for label in ("Trước", "Skip", "Include/Validate"):
            button = QPushButton(label)
            button.setEnabled(False)
            layout.addWidget(button)
        layout.addStretch(1)
        layout.addWidget(self.action_summary)
        return layout

    def _panel_frame(self, title: str, content: QWidget) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setMinimumHeight(104)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        layout.addWidget(QLabel(title))
        layout.addWidget(content, 1)
        return frame

    def _build_layer_panel(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setMinimumHeight(220)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Layers"))
        toolbar.addStretch(1)
        toolbar.addWidget(self.move_layer_up_button)
        toolbar.addWidget(self.move_layer_down_button)

        layout.addLayout(toolbar)
        layout.addWidget(self.layer_table, 1)
        layout.addWidget(self.layer_warning_label)
        return frame

    def _apply_queue_filter(self, queue_filter: QueueFilter) -> None:
        selected_id = self._current_or_selected_composition_id()
        self.tree_model.set_queue_filter(queue_filter)
        self.tree_view.expandAll()
        self._refresh_filter_controls()
        self._restore_selection(selected_id)

    def _refresh_filter_controls(self) -> None:
        counts = self.tree_model.filter_counts()
        for queue_filter, button in self.filter_buttons.items():
            button.setText(f"{queue_filter_label(queue_filter)} ({counts[queue_filter]})")
            button.setChecked(queue_filter == self.tree_model.active_queue_filter)

        has_visible_rows = self.tree_model.has_visible_compositions()
        active_label = queue_filter_label(self.tree_model.active_queue_filter)
        self.empty_state_label.setText(
            f"Không có composition khớp bộ lọc \"{active_label}\"."
        )
        self.empty_state_label.setVisible(not has_visible_rows)

    def _current_or_selected_composition_id(self) -> str | None:
        composition_id = self.tree_model.composition_id_for_index(self.tree_view.currentIndex())
        if composition_id is not None:
            return composition_id
        if self.selected_composition is None:
            return None
        return self.selected_composition.composition_id

    def _restore_selection(self, composition_id: str | None) -> None:
        if composition_id is None:
            return

        index = self.tree_model.index_for_composition_id(composition_id)
        if index.isValid():
            self.tree_view.setCurrentIndex(index)
        else:
            self.tree_view.clearSelection()

    def _select_composition_index(self, current, _previous) -> None:  # noqa: ANN001
        composition_id = self.tree_model.composition_id_for_index(current)
        if composition_id is None or self._workspace_service is None:
            return

        try:
            composition = self._workspace_service.read_composition(composition_id)
        except WorkspaceError as error:
            self.warnings_summary.setText(f"Không tải được composition: {error}")
            return

        self.selected_composition = composition
        self._update_detail_panels(composition)
        self.compositionSelected.emit(composition)

    def _persist_layer_visibility(self, top_left, bottom_right, roles) -> None:  # noqa: ANN001
        if (
            top_left.column() != int(LayerStackColumn.VISIBILITY)
            or bottom_right.column() != int(LayerStackColumn.VISIBILITY)
            or self._workspace_service is None
            or self.layer_model.composition_id is None
        ):
            return

        layer_id = self.layer_model.layer_id_for_index(top_left)
        if layer_id is None:
            return

        try:
            updated = self._workspace_service.set_layer_visibility(
                self.layer_model.composition_id,
                layer_id,
                visible=self.layer_model.visible_for_row(top_left.row()),
            )
        except WorkspaceError as error:
            self.warnings_summary.setText(f"Không lưu được layer: {error}")
            if self.selected_composition is not None:
                self.layer_model.set_composition(self.selected_composition)
            return

        self.selected_composition = updated
        self._update_detail_panels(updated)
        self._refresh_workspace_projection(updated.composition_id)

    def _move_selected_layer(self, offset: int) -> None:
        if self._workspace_service is None or self.layer_model.composition_id is None:
            return

        layer_id = self.layer_model.layer_id_for_index(self.layer_table.currentIndex())
        if layer_id is None:
            return

        ordered_layer_ids = self.layer_model.move_layer(layer_id, offset)
        if ordered_layer_ids is None:
            return

        try:
            updated = self._workspace_service.reorder_layers(
                self.layer_model.composition_id,
                ordered_layer_ids,
            )
        except WorkspaceError as error:
            self.warnings_summary.setText(f"Không lưu được thứ tự layer: {error}")
            return

        self.selected_composition = updated
        self._update_detail_panels(updated)
        self._refresh_workspace_projection(updated.composition_id)
        new_row = max(0, self.layer_table.currentIndex().row() + offset)
        new_index = self.layer_model.index(new_row, 0)
        if new_index.isValid():
            self.layer_table.setCurrentIndex(new_index)

    def _persist_canvas_view(self, center: list[float], scale: int) -> None:
        if self._workspace_service is None or self.selected_composition is None:
            return

        composition_id = self.selected_composition.composition_id
        try:
            updated = self._workspace_service.update_view_state(
                composition_id,
                center=center,
                scale=scale,
            )
        except (WorkspaceError, ValidationError) as error:
            self.warnings_summary.setText(f"Không lưu được view canvas: {error}")
            self.gis_canvas.set_composition(self.selected_composition)
            return

        self.selected_composition = updated
        self._update_detail_panels(updated)
        self._refresh_workspace_projection(updated.composition_id)

    def _refresh_workspace_projection(self, selected_id: str | None) -> None:
        if self._workspace_service is None:
            return

        self.tree_model.set_compositions(
            self._workspace_service.list_compositions(),
            targets=self._targets,
        )
        self.tree_view.expandAll()
        self._refresh_filter_controls()
        self._restore_selection(selected_id)

    def _update_detail_panels(self, composition: Composition) -> None:
        summary = composition.validation_summary
        self.composition_title.setText(
            f"{composition.composition_id} | {composition.capture_date.isoformat()}"
        )
        self.layer_model.set_composition(composition)
        self.layer_warning_label.setVisible(self.layer_model.has_no_visible_layers())
        self.preview_summary.setText(
            "Preview cần cập nhật"
            if composition.needs_revalidation
            else f"Preview source: {composition.artifacts.preview_render_path or 'chưa render'}"
        )
        frame_aspect = self._frame_aspect_for_composition(composition)
        if frame_aspect is not None:
            self.gis_canvas.set_frame_aspect(frame_aspect)
        self.gis_canvas.set_composition(composition)
        self.warnings_summary.setText(
            "Validation "
            f"{composition.persisted_validation_state.value}: "
            f"{summary.error_count} error, {summary.warning_count} warning, "
            f"{summary.info_count} info"
        )

    def _frame_aspect_for_composition(self, composition: Composition) -> float | None:
        for target in self._targets or []:
            if target.id != composition.target_id:
                continue
            explicit_aspect = target.metadata.get("map_frame_aspect")
            if _is_positive_number(explicit_aspect):
                return float(explicit_aspect)
            map_frame = target.metadata.get("map_frame")
            if isinstance(map_frame, dict):
                width = map_frame.get("width")
                height = map_frame.get("height")
                if _is_positive_number(width) and _is_positive_number(height):
                    return float(width) / float(height)
        return None


def _is_positive_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
