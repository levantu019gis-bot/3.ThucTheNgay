"""Qt application shell."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from thucthengay.editor.modes.setup_mode import SetupMode


class AppShell(QMainWindow):
    """Top-level desktop window for the application."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("3.ThucTheNgay")
        self.setup_mode = SetupMode()
        self.setCentralWidget(self.setup_mode)
        self.resize(960, 360)


def run_gui(argv: list[str] | None = None) -> int:
    """Run the Qt app shell."""
    app = QApplication.instance() or QApplication(sys.argv if argv is None else argv)
    shell = AppShell()
    shell.show()
    return app.exec()
