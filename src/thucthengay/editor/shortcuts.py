"""Keyboard shortcut helpers for editor modes."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QLineEdit,
    QPlainTextEdit,
    QTextEdit,
    QWidget,
)

TEXT_EDIT_WIDGETS = (QLineEdit, QTextEdit, QPlainTextEdit, QAbstractSpinBox, QComboBox)


def review_shortcuts_enabled_for_focus(focused_widget: QWidget | None) -> bool:
    """Return false when arrow-key review shortcuts would interfere with text editing."""
    if focused_widget is None:
        return True
    return not isinstance(focused_widget, TEXT_EDIT_WIDGETS)
