from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLineEdit, QTextEdit, QWidget

from thucthengay.editor.shortcuts import review_shortcuts_enabled_for_focus


def qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_review_shortcuts_are_disabled_for_text_editing_focus() -> None:
    qapp()

    assert not review_shortcuts_enabled_for_focus(QLineEdit())
    assert not review_shortcuts_enabled_for_focus(QTextEdit())


def test_review_shortcuts_are_enabled_for_non_text_focus() -> None:
    qapp()

    assert review_shortcuts_enabled_for_focus(None)
    assert review_shortcuts_enabled_for_focus(QWidget())
