# Story 1.4: Select Project Paths in Setup Mode

Status: done

## Story

As an Operator,
I want to select the project config, imagery input folder, and workspace folder in Setup mode,
So that I can verify the project inputs before ingestion changes any files.

## Requirement References

- FR2
- UX-DR1
- UX-DR2
- UX-DR14
- UX-DR16
- NFR5
- NFR9

## Acceptance Criteria

1. Given the application opens in Setup mode, when the Operator views the path selection area, then it shows path picker rows for config file, imagery input folder, and workspace folder, and each row has a label, read-only path field, browse button, validation indicator, middle-elided long path display, and full path tooltip.
2. Given a selected path is missing, unreadable, or not the expected type, when the path row validates, then the row displays a non-color-only invalid status, and the primary ingestion action remains disabled with a tooltip explaining the blocker.
3. Given all required paths are valid, when Setup validation completes, then the app enables the next available setup action, and the selected paths are visible before any workspace clear or ingestion operation begins.
4. Given a long local or LAN path is selected, when the path row is narrower than the full text, then the path is elided without changing row height, and the full path remains available through tooltip or equivalent detail display.

## Implementation Context

- Prior stories 1.1, 1.2, and 1.3 are complete; reuse the existing PySide6 dependency, Pydantic model contracts, and config service.
- Story 1.4 owns only Setup-mode path selection and validation. It must not implement ingestion, workspace clearing, GeoTIFF scanning, or progress jobs.
- UI code belongs under `src/thucthengay/editor/`.
- Core packages must remain headless-testable and must not import `PySide6.QtWidgets` or `editor`.
- Path rows should follow UX anatomy: label, read-only path field, browse button, validation indicator, middle-elided long paths, full-path tooltip.
- The primary setup action text is `Lấy dữ liệu`; it remains disabled until config file, imagery folder, and workspace folder validate.

## Tasks

- [x] Create reusable Setup path picker widget with typed validation states.
- [x] Create Setup mode widget with config/input/workspace rows and disabled/enabled primary action state.
- [x] Create app shell that opens in Setup mode when GUI is available.
- [x] Keep CLI smoke behavior usable in headless environments.
- [x] Add unit tests for path validation, row display state, and Setup action enablement.
- [x] Run quality gates.

## Dev Agent Record

### Debug Log

- 2026-05-25: Confirmed sprint status: stories 1.1, 1.2, 1.3 are done; Story 1.4 was backlog.
- 2026-05-25: Reviewed Story 1.4 ACs in epics and Path Picker Row UX spec.
- 2026-05-25: Implemented Setup-only UI slice without ingestion or destructive workspace behavior.
- 2026-05-25: Ran `pytest`, `ruff check .`, and `python -m thucthengay --smoke`; all passed.

### Completion Notes

- Setup mode now provides three path picker rows for config JSON, imagery input folder, and workspace folder.
- Long paths are displayed through a middle-elided read-only field while the full path remains in the tooltip.
- Invalid state is text-based (`Lỗi`) with a Vietnamese blocker message, not color-only.
- `Lấy dữ liệu` stays disabled until all required paths are valid and exposes the first blocker in its tooltip.
- In headless environments, the app entrypoint returns a smoke message instead of attempting to launch Qt.

### File List

- `_bmad-output/implementation-artifacts/1-4-select-project-paths-in-setup-mode.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `src/thucthengay/app.py`
- `src/thucthengay/editor/app_shell.py`
- `src/thucthengay/editor/modes/setup_mode.py`
- `src/thucthengay/editor/widgets/path_picker.py`
- `tests/unit/test_setup_mode.py`

### Change Log

- 2026-05-25: Added Setup mode path selection UI and tests.
- 2026-05-25: Marked Story 1.4 complete after passing quality gates.
