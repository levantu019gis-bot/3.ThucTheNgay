"""Confirmation UI for destructive workspace operations."""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget

from thucthengay.workspace.service import WorkspaceClearPlan


def confirm_workspace_clear(parent: QWidget | None, plan: WorkspaceClearPlan) -> bool:
    """Ask the Operator before clearing app-owned workspace data."""
    message = QMessageBox(parent)
    message.setIcon(QMessageBox.Icon.Warning)
    message.setWindowTitle("Xác nhận xóa dữ liệu workspace")
    message.setText("Thao tác này sẽ xóa dữ liệu do ứng dụng tạo trong workspace.")
    message.setInformativeText("Sẽ xóa: " + ", ".join(plan.labels))
    message.setStandardButtons(QMessageBox.StandardButton.Cancel)

    cancel_button = message.button(QMessageBox.StandardButton.Cancel)
    if cancel_button is not None:
        cancel_button.setText("Giữ nguyên")
        message.setDefaultButton(cancel_button)

    clear_button = message.addButton(
        "Xóa cache, compositions, renders, exports",
        QMessageBox.ButtonRole.DestructiveRole,
    )
    message.exec()
    return message.clickedButton() is clear_button
