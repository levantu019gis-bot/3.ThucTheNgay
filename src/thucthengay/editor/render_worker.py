"""Qt worker adapter for background preview render jobs."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from thucthengay.jobs import PreviewRenderRequest, run_preview_render_job


class RenderWorker(QObject):
    """Run a preview render off the UI thread and emit the result."""

    finished = Signal(object)

    def __init__(
        self,
        request: PreviewRenderRequest,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._request = request

    @Slot()
    def run(self) -> None:
        """Worker entry point invoked by QThread."""
        result = run_preview_render_job(self._request)
        self.finished.emit(result)
