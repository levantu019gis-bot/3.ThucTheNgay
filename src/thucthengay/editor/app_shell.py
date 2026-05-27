"""Qt application shell."""

from __future__ import annotations

import sys
from uuid import uuid4

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from thucthengay.config import load_project_config
from thucthengay.editor.modes.export_mode import ExportMode
from thucthengay.editor.modes.review_edit_mode import ReviewEditMode
from thucthengay.editor.modes.setup_mode import SetupMode, SetupPaths
from thucthengay.jobs import IngestionSummary, JobState, run_ingestion_job
from thucthengay.workspace import WorkspaceService


class AppShell(QMainWindow):
    """Top-level desktop window for the application."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("3.ThucTheNgay")
        self.setup_mode = SetupMode()
        self.review_edit_mode = ReviewEditMode()
        self.export_mode = ExportMode()

        self.mode_tabs = QTabWidget()
        self.mode_tabs.setObjectName("modeTabs")
        self.mode_tabs.addTab(self.setup_mode, "Setup")
        self.mode_tabs.addTab(self.review_edit_mode, "Review/Edit")
        self.mode_tabs.addTab(self.export_mode, "Export")
        self.setup_mode.ingestRequested.connect(self._run_ingestion)
        self.export_mode.jumpRequested.connect(self._jump_to_review_context)

        self.setCentralWidget(self.mode_tabs)
        self.resize(1280, 720)

    def _run_ingestion(self, setup_paths: SetupPaths) -> None:
        config_result = load_project_config(setup_paths.config_file)
        workspace_service = WorkspaceService(setup_paths.workspace_folder)
        job_id = f"ingestion-{uuid4().hex}"
        self.setup_mode.start_ingestion_progress()

        def publish_progress(event) -> None:
            self.setup_mode.show_ingestion_progress(event)
            app = QApplication.instance()
            if app is not None:
                app.processEvents()

        result = run_ingestion_job(
            job_id=job_id,
            config_result=config_result,
            imagery_folder=setup_paths.imagery_input_folder,
            workspace_service=workspace_service,
            publish=publish_progress,
        )
        summary = IngestionSummary.from_job_result(
            result,
            workspace_path=setup_paths.workspace_folder,
        )
        self.setup_mode.show_ingestion_summary(summary)
        if result.state == JobState.ERROR:
            return

        self.review_edit_mode.load_workspace(
            workspace_service,
            targets=config_result.enabled_targets,
        )
        self.export_mode.load_workspace(
            workspace_service,
            targets=config_result.enabled_targets,
        )
        self.mode_tabs.setCurrentWidget(self.review_edit_mode)

    def _jump_to_review_context(
        self,
        target_id: str,
        composition_id: str,
        layer_id: str,
    ) -> None:
        self.mode_tabs.setCurrentWidget(self.review_edit_mode)
        self.review_edit_mode._handle_issue_jump(target_id, composition_id, layer_id)


def run_gui(argv: list[str] | None = None) -> int:
    """Run the Qt app shell."""
    app = QApplication.instance() or QApplication(sys.argv if argv is None else argv)
    shell = AppShell()
    shell.show()
    return app.exec()
