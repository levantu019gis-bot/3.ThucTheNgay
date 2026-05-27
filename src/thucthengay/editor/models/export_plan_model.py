"""Qt model for export preflight plan rows."""

from __future__ import annotations

from enum import IntEnum

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from thucthengay.models import ExportPlanRow

_INVALID_INDEX = QModelIndex()


class ExportPlanColumn(IntEnum):
    """Columns shown in the Export Plan table."""

    SLIDE = 0
    TARGET = 1
    DATE_TIME = 2
    TEMPLATE = 3
    ISSUES = 4
    ACTION = 5


class ExportPlanRole(IntEnum):
    """Custom roles for tests and jump handling."""

    COMPOSITION_ID = int(Qt.ItemDataRole.UserRole) + 80
    TARGET_ID = int(Qt.ItemDataRole.UserRole) + 81
    ISSUE_COUNT = int(Qt.ItemDataRole.UserRole) + 82
    BLOCKING = int(Qt.ItemDataRole.UserRole) + 83


class ExportPlanModel(QAbstractTableModel):
    """Read-only table model for Export mode plan rows."""

    HEADERS = {
        ExportPlanColumn.SLIDE: "Slide",
        ExportPlanColumn.TARGET: "Target",
        ExportPlanColumn.DATE_TIME: "Date/time",
        ExportPlanColumn.TEMPLATE: "Template",
        ExportPlanColumn.ISSUES: "Issues",
        ExportPlanColumn.ACTION: "Action",
    }

    def __init__(self, parent=None) -> None:  # noqa: ANN001
        super().__init__(parent)
        self._rows: list[ExportPlanRow] = []

    def set_rows(self, rows: list[ExportPlanRow]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def row_at(self, row: int) -> ExportPlanRow | None:
        if row < 0 or row >= len(self._rows):
            return None
        return self._rows[row]

    def rowCount(self, parent: QModelIndex = _INVALID_INDEX) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = _INVALID_INDEX) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(ExportPlanColumn)

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = int(Qt.ItemDataRole.DisplayRole),
    ) -> object:
        if orientation != Qt.Orientation.Horizontal or role != int(Qt.ItemDataRole.DisplayRole):
            return None
        return self.HEADERS.get(ExportPlanColumn(section), "")

    def data(self, index: QModelIndex, role: int = int(Qt.ItemDataRole.DisplayRole)) -> object:
        if not index.isValid():
            return None
        row = self.row_at(index.row())
        if row is None:
            return None

        if role == ExportPlanRole.COMPOSITION_ID:
            return row.composition_id
        if role == ExportPlanRole.TARGET_ID:
            return row.target_id
        if role == ExportPlanRole.ISSUE_COUNT:
            return row.issue_count
        if role == ExportPlanRole.BLOCKING:
            return row.blocking
        if role == int(Qt.ItemDataRole.ToolTipRole):
            return _tooltip(row)
        if role != int(Qt.ItemDataRole.DisplayRole):
            return None

        column = ExportPlanColumn(index.column())
        if column == ExportPlanColumn.SLIDE:
            return str(row.slide_number) if row.slide_number is not None else "-"
        if column == ExportPlanColumn.TARGET:
            return row.target_label
        if column == ExportPlanColumn.DATE_TIME:
            return f"{row.date_label} {row.time_label}".strip()
        if column == ExportPlanColumn.TEMPLATE:
            return row.template_status
        if column == ExportPlanColumn.ISSUES:
            if row.issue_count == 1:
                return "1 issue"
            return f"{row.issue_count} issues"
        if column == ExportPlanColumn.ACTION:
            return "Jump"
        return None


def _tooltip(row: ExportPlanRow) -> str:
    if not row.issues:
        return f"{row.composition_id} san sang trong export plan."
    lines = [row.composition_id]
    for issue in row.issues:
        text = f"[{issue.severity.value.upper()}] {issue.message}"
        if issue.remediation:
            text = f"{text} -> {issue.remediation}"
        lines.append(text)
    return "\n".join(lines)
