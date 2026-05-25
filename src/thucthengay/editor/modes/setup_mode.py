"""Setup mode for selecting project input paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFormLayout, QPushButton, QVBoxLayout, QWidget

from thucthengay.editor.widgets.path_picker import PathKind, PathPickerRow
from thucthengay.editor.widgets.workspace_confirmation import confirm_workspace_clear
from thucthengay.workspace import WorkspaceService


@dataclass(frozen=True)
class SetupPaths:
    """Validated paths selected in Setup mode."""

    config_file: Path
    imagery_input_folder: Path
    workspace_folder: Path


class SetupMode(QWidget):
    """Setup screen containing required project path pickers."""

    ingestRequested = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.config_row = PathPickerRow("Config JSON", PathKind.CONFIG_FILE)
        self.imagery_row = PathPickerRow("Thư mục ảnh", PathKind.INPUT_FOLDER)
        self.workspace_row = PathPickerRow("Workspace", PathKind.WORKSPACE_FOLDER)
        self.ingest_button = QPushButton("Lấy dữ liệu")
        self.ingest_button.setObjectName("setupIngestButton")

        form = QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(10)
        form.addRow(self.config_row)
        form.addRow(self.imagery_row)
        form.addRow(self.workspace_row)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addWidget(self.ingest_button)

        for row in self.path_rows:
            row.validationChanged.connect(self._update_action_state)
        self.ingest_button.clicked.connect(self._emit_ingest_requested)
        self._update_action_state()

    @property
    def path_rows(self) -> tuple[PathPickerRow, PathPickerRow, PathPickerRow]:
        return (self.config_row, self.imagery_row, self.workspace_row)

    @property
    def blockers(self) -> list[str]:
        return [row.validation.message for row in self.path_rows if not row.validation.ok]

    @property
    def is_ready(self) -> bool:
        return not self.blockers

    def selected_paths(self) -> SetupPaths | None:
        if not self.is_ready:
            return None

        config_file = self.config_row.selected_path
        imagery_folder = self.imagery_row.selected_path
        workspace_folder = self.workspace_row.selected_path
        if config_file is None or imagery_folder is None or workspace_folder is None:
            return None

        return SetupPaths(
            config_file=config_file,
            imagery_input_folder=imagery_folder,
            workspace_folder=workspace_folder,
        )

    def _update_action_state(self, *_args: object) -> None:
        self.ingest_button.setEnabled(self.is_ready)
        if self.is_ready:
            self.ingest_button.setToolTip("Sẵn sàng lấy dữ liệu.")
            return

        first_blocker = self.blockers[0] if self.blockers else "Chưa đủ đường dẫn hợp lệ."
        self.ingest_button.setToolTip(first_blocker)

    def _emit_ingest_requested(self) -> None:
        selected_paths = self.selected_paths()
        if selected_paths is None:
            return

        workspace_service = WorkspaceService(selected_paths.workspace_folder)
        if workspace_service.has_app_owned_data():
            clear_confirmed = confirm_workspace_clear(self, workspace_service.clear_plan())
            if not clear_confirmed:
                return

        self.ingestRequested.emit(selected_paths)
