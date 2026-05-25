from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from thucthengay.editor.modes.setup_mode import SetupMode
from thucthengay.editor.widgets.path_picker import (
    PathKind,
    PathPickerRow,
    PathStatus,
    validate_selected_path,
)


def qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_validate_selected_config_path_requires_json_file(tmp_path: Path) -> None:
    config_file = tmp_path / "project.json"
    config_file.write_text("{}", encoding="utf-8")
    folder = tmp_path / "folder"
    folder.mkdir()

    assert validate_selected_path(str(config_file), PathKind.CONFIG_FILE).ok

    folder_validation = validate_selected_path(str(folder), PathKind.CONFIG_FILE)
    assert folder_validation.status == PathStatus.INVALID
    assert "file JSON" in folder_validation.message

    txt_file = tmp_path / "project.txt"
    txt_file.write_text("{}", encoding="utf-8")
    txt_validation = validate_selected_path(str(txt_file), PathKind.CONFIG_FILE)
    assert txt_validation.status == PathStatus.INVALID
    assert ".json" in txt_validation.message


def test_path_picker_row_keeps_full_path_tooltip_and_elides_display(tmp_path: Path) -> None:
    qapp()
    long_dir = tmp_path / "very" / "long" / "local" / "or" / "lan" / "workspace" / "path"
    long_dir.mkdir(parents=True)

    row = PathPickerRow("Workspace", PathKind.WORKSPACE_FOLDER)
    row.resize(260, row.sizeHint().height())
    row.set_path(long_dir)
    row.path_field.resize(90, row.path_field.height())
    row.path_field.set_full_text(str(long_dir))

    assert row.validation.ok
    assert row.status_label.text() == "Hợp lệ"
    assert row.path_field.toolTip() == str(long_dir)
    assert row.path_field.text() != str(long_dir)


def test_setup_mode_disables_ingest_until_all_required_paths_are_valid(tmp_path: Path) -> None:
    qapp()
    config_file = tmp_path / "project.json"
    config_file.write_text("{}", encoding="utf-8")
    imagery_folder = tmp_path / "imagery"
    imagery_folder.mkdir()
    workspace_folder = tmp_path / "workspace"
    workspace_folder.mkdir()

    setup = SetupMode()
    assert not setup.ingest_button.isEnabled()
    assert setup.selected_paths() is None

    setup.config_row.set_path(config_file)
    setup.imagery_row.set_path(imagery_folder)
    assert not setup.ingest_button.isEnabled()

    setup.workspace_row.set_path(workspace_folder)
    assert setup.ingest_button.isEnabled()

    selected_paths = setup.selected_paths()
    assert selected_paths is not None
    assert selected_paths.config_file == config_file.resolve()
    assert selected_paths.imagery_input_folder == imagery_folder.resolve()
    assert selected_paths.workspace_folder == workspace_folder.resolve()


def test_setup_mode_reports_first_blocker_in_ingest_tooltip(tmp_path: Path) -> None:
    qapp()
    setup = SetupMode()

    missing_config = tmp_path / "missing.json"
    setup.config_row.set_path(missing_config)

    assert not setup.ingest_button.isEnabled()
    assert "Không tìm thấy" in setup.ingest_button.toolTip()


def test_setup_mode_requires_confirmation_before_ingest_with_existing_workspace_data(
    tmp_path: Path,
    monkeypatch,
) -> None:
    qapp()
    config_file = tmp_path / "project.json"
    config_file.write_text("{}", encoding="utf-8")
    imagery_folder = tmp_path / "imagery"
    imagery_folder.mkdir()
    workspace_folder = tmp_path / "workspace"
    (workspace_folder / "cache").mkdir(parents=True)
    (workspace_folder / "cache" / "old.tif").write_text("old", encoding="utf-8")

    confirmed_plans = []

    def deny_clear(_parent, plan):
        confirmed_plans.append(plan)
        return False

    monkeypatch.setattr("thucthengay.editor.modes.setup_mode.confirm_workspace_clear", deny_clear)

    setup = SetupMode()
    emitted = []
    setup.ingestRequested.connect(emitted.append)
    setup.config_row.set_path(config_file)
    setup.imagery_row.set_path(imagery_folder)
    setup.workspace_row.set_path(workspace_folder)

    setup.ingest_button.click()

    assert confirmed_plans
    assert emitted == []
