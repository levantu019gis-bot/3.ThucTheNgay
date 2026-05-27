"""Export summary metrics widget."""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

from thucthengay.models import ExportPreflightState, ExportPreflightSummary


class ExportSummaryWidget(QWidget):
    """Compact dashboard metrics for Export mode."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("exportSummary")
        self._labels: dict[str, QLabel] = {}
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(4)

        for column, key in enumerate(("slides", "targets", "skipped", "warnings", "errors")):
            value = QLabel("0")
            value.setObjectName(f"exportSummary_{key}")
            label = QLabel(_metric_label(key))
            label.setObjectName(f"exportSummary_{key}_label")
            layout.addWidget(value, 0, column)
            layout.addWidget(label, 1, column)
            self._labels[key] = value

        self.state_label = QLabel("Preflight: not_run")
        self.state_label.setObjectName("exportSummaryState")
        layout.addWidget(self.state_label, 0, 5, 2, 1)

    def set_summary(self, summary: ExportPreflightSummary) -> None:
        self._labels["slides"].setText(str(summary.included_slide_count))
        self._labels["targets"].setText(str(summary.target_count))
        self._labels["skipped"].setText(str(summary.skipped_count))
        self._labels["warnings"].setText(str(summary.warning_count))
        self._labels["errors"].setText(str(summary.error_count))
        self.state_label.setText(f"Preflight: {summary.state.value}")
        self.state_label.setProperty("blocked", summary.state == ExportPreflightState.BLOCKED)


def _metric_label(key: str) -> str:
    return {
        "slides": "included slides",
        "targets": "targets",
        "skipped": "skipped/blocked",
        "warnings": "warnings",
        "errors": "errors",
    }[key]
