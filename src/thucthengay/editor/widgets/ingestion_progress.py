"""Qt widget for live ingestion progress."""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QLabel, QProgressBar, QVBoxLayout, QWidget

from thucthengay.jobs import JobState, ProgressEvent


class IngestionProgressWidget(QWidget):
    """Render live Setup ingestion progress from headless progress events."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.status_label = QLabel("Chưa lấy dữ liệu")
        self.image_count_label = QLabel("Ảnh đã scan: 0/0")
        self.target_count_label = QLabel("Target đã scan: 0/0")
        self.current_target_label = QLabel("Target hiện tại: -")

        self.image_progress = QProgressBar()
        self.target_progress = QProgressBar()

        self.status_label.setObjectName("ingestionProgressStatus")
        self.image_count_label.setObjectName("ingestionProgressImageCount")
        self.target_count_label.setObjectName("ingestionProgressTargetCount")
        self.current_target_label.setObjectName("ingestionProgressCurrentTarget")
        self.image_progress.setObjectName("ingestionImageProgress")
        self.target_progress.setObjectName("ingestionTargetProgress")

        for label in (
            self.status_label,
            self.image_count_label,
            self.target_count_label,
            self.current_target_label,
        ):
            label.setWordWrap(True)

        self.progress_body = QWidget()
        self.progress_body.setObjectName("ingestionProgressBody")
        grid = QGridLayout(self.progress_body)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)
        grid.addWidget(QLabel("Ảnh"), 0, 0)
        grid.addWidget(self.image_progress, 0, 1)
        grid.addWidget(self.image_count_label, 0, 2)
        grid.addWidget(QLabel("Target"), 1, 0)
        grid.addWidget(self.target_progress, 1, 1)
        grid.addWidget(self.target_count_label, 1, 2)
        grid.addWidget(self.current_target_label, 2, 1, 1, 2)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_body)

        self.setVisible(False)
        self.progress_body.setVisible(False)
        self._set_progress(self.image_progress, 0, 0)
        self._set_progress(self.target_progress, 0, 0)

    def start(self) -> None:
        """Reset and show progress for a new ingestion run."""
        self.status_label.setText("Đang khởi tạo lấy dữ liệu.")
        self.image_count_label.setText("Ảnh đã scan: 0/0")
        self.target_count_label.setText("Target đã scan: 0/0")
        self.current_target_label.setText("Target hiện tại: -")
        self._set_progress(self.image_progress, 0, 0)
        self._set_progress(self.target_progress, 0, 0)
        self.progress_body.setVisible(False)
        self.setVisible(True)

    def apply_event(self, event: ProgressEvent) -> None:
        """Apply a job event without reading workspace state."""
        self.status_label.setText(_status_prefix(event.state, event.message))
        if event.stage != "setup":
            self.progress_body.setVisible(True)

        image_total = event.total_image_count or event.total or 0
        image_current = event.scanned_file_count
        if event.stage == "scan" and event.current is not None:
            image_current = event.current
        self._set_progress(self.image_progress, image_current, image_total)
        self.image_count_label.setText(
            f"Ảnh đã scan: {image_current}/{image_total} "
            f"(hợp lệ: {event.scanned_image_count})"
        )

        target_total = event.total_target_count
        target_current = event.processed_target_count
        if event.stage == "match" and event.current is not None and event.total is not None:
            target_current = event.current
            target_total = event.total
        self._set_progress(self.target_progress, target_current, target_total)
        self.target_count_label.setText(f"Target đã scan: {target_current}/{target_total}")

        if event.current_target_name:
            self.current_target_label.setText(
                f"Target hiện tại: {event.current_target_name} - "
                f"đã lấy {event.current_target_matched_count} ảnh"
            )
        elif target_total == 0:
            self.current_target_label.setText("Target hiện tại: chưa có target bật")

        self.setVisible(True)

    @staticmethod
    def _set_progress(progress: QProgressBar, current: int, total: int) -> None:
        progress.setMinimum(0)
        progress.setMaximum(max(total, 0))
        progress.setValue(min(max(current, 0), max(total, 0)))
        progress.setFormat(f"{current}/{total}" if total else "0/0")


def _status_prefix(state: JobState, message: str) -> str:
    if state == JobState.CANCELLED:
        return f"Đã dừng lấy dữ liệu: {message}"
    if state == JobState.ERROR:
        return f"Lấy dữ liệu thất bại: {message}"
    if state == JobState.WARNING:
        return f"Lấy dữ liệu hoàn tất với cảnh báo: {message}"
    if state == JobState.SUCCESS:
        return f"Lấy dữ liệu thành công: {message}"
    return message
