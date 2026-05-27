"""Export mode dashboard and preflight plan UI."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from thucthengay.editor.models.export_plan_model import ExportPlanModel
from thucthengay.editor.widgets.export_summary import ExportSummaryWidget
from thucthengay.export import build_export_preflight_plan
from thucthengay.models import ExportPreflightPlan, TargetConfig
from thucthengay.workspace import WorkspaceError, WorkspaceService


class ExportMode(QWidget):
    """Desktop Export mode focused on preflight and export plan review."""

    jumpRequested = Signal(str, str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("exportMode")
        self.setMinimumSize(960, 560)
        self._workspace_service: WorkspaceService | None = None
        self._targets: list[TargetConfig] = []
        self._last_plan: ExportPreflightPlan | None = None

        self.summary = ExportSummaryWidget()
        self.preflight_button = QPushButton("Preflight")
        self.preflight_button.setObjectName("exportPreflight")
        self.preflight_button.clicked.connect(self.run_preflight)
        self.export_button = QPushButton("Export PPTX/TXT")
        self.export_button.setObjectName("exportFinal")
        self.export_button.setProperty("primaryAction", True)
        self.export_button.setEnabled(False)
        self.export_button.setToolTip("Chay Preflight va xu ly loi blocking truoc khi export.")

        self.status_label = QLabel("Chua chay preflight.")
        self.status_label.setObjectName("exportStatus")
        self.status_label.setWordWrap(True)

        self.plan_model = ExportPlanModel(self)
        self.plan_table = QTableView()
        self.plan_table.setObjectName("exportPlanTable")
        self.plan_table.setModel(self.plan_model)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.plan_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.plan_table.setAlternatingRowColors(True)
        self.plan_table.verticalHeader().setDefaultSectionSize(30)
        self.plan_table.verticalHeader().setVisible(False)
        self.plan_table.doubleClicked.connect(self._jump_from_index)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.preflight_button)
        toolbar.addWidget(self.export_button)
        toolbar.addStretch(1)
        toolbar.addWidget(self.status_label)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        layout.addWidget(self.summary)
        layout.addLayout(toolbar)
        layout.addWidget(self._panel_frame("Export Plan", self.plan_table), 1)

    def load_workspace(
        self,
        workspace_service: WorkspaceService,
        *,
        targets: list[TargetConfig] | None = None,
    ) -> None:
        self._workspace_service = workspace_service
        self._targets = list(targets or [])
        self.status_label.setText("San sang chay preflight.")

    def run_preflight(self) -> None:
        if self._workspace_service is None:
            self.status_label.setText("Chua co workspace de chay preflight.")
            self.export_button.setEnabled(False)
            return
        try:
            plan = build_export_preflight_plan(self._workspace_service, self._targets)
        except WorkspaceError as error:
            self.status_label.setText(f"Khong doc duoc workspace: {error}")
            self.export_button.setEnabled(False)
            return

        self._last_plan = plan
        self.summary.set_summary(plan.summary)
        self.plan_model.set_rows(plan.rows)
        self.plan_table.resizeColumnsToContents()
        self.export_button.setEnabled(False)
        if plan.summary.error_count:
            self.export_button.setToolTip("Export bi chan vi preflight con loi blocking.")
            self.status_label.setText(
                "Preflight bi chan. Double click row co issue de quay lai sua."
            )
        else:
            self.export_button.setToolTip("Final export se duoc mo o cac story tiep theo.")
            self.status_label.setText(
                "Preflight khong co loi blocking; final export chua implement."
            )

    def _jump_from_index(self, index) -> None:  # noqa: ANN001
        row = self.plan_model.row_at(index.row())
        if row is None:
            return
        self.jumpRequested.emit(row.target_id, row.composition_id, "")

    def _panel_frame(self, title: str, content: QWidget) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        layout.addWidget(QLabel(title))
        layout.addWidget(content, 1)
        return frame
