"""Qt application shell."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from thucthengay.editor.modes.review_edit_mode import ReviewEditMode
from thucthengay.editor.modes.setup_mode import SetupMode


class AppShell(QMainWindow):
    """Top-level desktop window for the application."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("3.ThucTheNgay")
        self.setup_mode = SetupMode()
        self.review_edit_mode = ReviewEditMode()

        self.mode_tabs = QTabWidget()
        self.mode_tabs.setObjectName("modeTabs")
        self.mode_tabs.addTab(self.setup_mode, "Setup")
        self.mode_tabs.addTab(self.review_edit_mode, "Review/Edit")

        self.setCentralWidget(self.mode_tabs)
        self.resize(1280, 720)


def run_gui(argv: list[str] | None = None) -> int:
    """Run the Qt app shell."""
    app = QApplication.instance() or QApplication(sys.argv if argv is None else argv)
    shell = AppShell()
    shell.show()
    return app.exec()
