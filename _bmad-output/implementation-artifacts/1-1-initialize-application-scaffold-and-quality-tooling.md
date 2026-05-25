# Story 1.1: Initialize Application Scaffold and Quality Tooling

Status: done

<!-- Ultimate context engine analysis completed - comprehensive developer guide created -->

## Story

As a Developer,
I want a clean Python desktop application scaffold with standard tooling,
so that future stories can be implemented consistently and tested without ad hoc setup.

## Acceptance Criteria

1. **Given** the repository has no finalized application scaffold  
   **When** the developer initializes the app structure  
   **Then** the project contains `pyproject.toml`, source package layout, test layout, and configured dependencies for PySide6, Pydantic, pytest, and ruff  
   **And** the package follows the architecture modules: `models`, `config`, `workspace`, `ingestion`, `gis`, `render`, `validation`, `export`, `jobs`, `editor`, and `utils`.

2. **Given** the scaffold is present  
   **When** the developer runs the test and lint commands documented for the project  
   **Then** the commands execute against the package without requiring network access or external project data  
   **And** at least one smoke test verifies the package can be imported.

3. **Given** future implementation stories depend on core modules  
   **When** modules are created in the scaffold  
   **Then** non-UI core modules do not import Qt widgets  
   **And** UI entrypoint code is isolated from model/workspace/config services.

## Tasks / Subtasks

- [x] Initialize project metadata and dependency management (AC: 1, 2)
  - [x] Create or adapt a `uv` Python app scaffold in the current project root without deleting existing planning assets, `scripts/`, `webapp_geojson/`, `Slide_1.pptx`, or `Slide_1.template.json`.
  - [x] Add `pyproject.toml`, `.python-version`, `uv.lock`, `.gitignore`, and a concise `README.md` if missing.
  - [x] Configure runtime dependencies for the MVP architecture: `PySide6`, `pydantic`, `rasterio`, `GDAL` or a documented GDAL-compatible install path, `shapely`, `pyproj`, `numpy`, `Pillow`, and `python-pptx`.
  - [x] Configure dev dependencies with `pytest` and `ruff`; include `mypy` or `pyright` only if dependency resolution is clean and documented.

- [x] Create the source package layout (AC: 1, 3)
  - [x] Create `src/thucthengay/__init__.py`, `src/thucthengay/__main__.py`, and `src/thucthengay/app.py`.
  - [x] Create package directories with `__init__.py`: `models`, `config`, `workspace`, `ingestion`, `gis`, `render`, `validation`, `export`, `jobs`, `editor`, and `utils`.
  - [x] Under `editor/`, create placeholder subpackages for future UI work: `modes`, `models`, `widgets`, and `delegates`.
  - [x] Keep scaffold modules lightweight; do not implement story 1.2 model schemas or later workflow logic in this story.

- [x] Add test layout and smoke coverage (AC: 2, 3)
  - [x] Create `tests/fixtures/{configs,geojson,geotiff,templates,workspaces}`, `tests/unit`, and `tests/integration`.
  - [x] Add a smoke test under `tests/unit/` that imports `thucthengay` and verifies import does not require project data, network, or launching a Qt event loop.
  - [x] Add a guardrail test or static import check confirming core modules do not import `PySide6` or `thucthengay.editor`.

- [x] Configure quality commands and developer entrypoints (AC: 2)
  - [x] Configure `ruff` in `pyproject.toml` for lint/format, excluding generated/cache/build folders.
  - [x] Configure `pytest` in `pyproject.toml` with `tests` as the default test path.
  - [x] Ensure these commands work from a clean checkout after dependencies are installed: `uv run pytest`, `uv run ruff check .`, and `uv run python -m thucthengay`.
  - [x] Make `python -m thucthengay` print or launch only a minimal placeholder app shell; it must not scan files, open dialogs, or require sample data.

- [x] Preserve current repository assets (AC: 1, 2)
  - [x] Do not move or rewrite `_bmad-output/`, `_bmad/`, `.agents/`, `scripts/`, `webapp_geojson/`, `docs/`, `Slide_1.pptx`, `Slide_1.template.json`, or `environment.yml` unless explicitly required for tooling.
  - [x] If `.gitignore` is added, ignore `.venv/`, `.ruff_cache/`, `.pytest_cache/`, `__pycache__/`, build artifacts, and local workspace output; do not ignore planning artifacts.

### Review Findings


- [x] [Review][Patch] Keep conda GDAL fallback from replacing conda-forge native GIS packages with PyPI wheels [README.md:30]
- [x] [Review][Patch] Fix relative import resolution for core package `__init__.py` files [tests/unit/test_core_import_boundaries.py:32]
- [x] [Review][Patch] Detect constant-string dynamic imports in core import-boundary guardrail [tests/unit/test_core_import_boundaries.py:47]
- [x] [Review][Patch] Include non-GIS runtime dependencies in conda fallback environment [environment.yml:4]
- [x] [Review][Patch] Detect aliased and relative constant-string dynamic imports in core import-boundary guardrail [tests/unit/test_core_import_boundaries.py:42]
- [x] [Review][Patch] Document conda+uv GDAL fallback without bypassing conda environment [README.md:21]
- [x] [Review][Patch] Align project metadata with Python 3.11 baseline [pyproject.toml:6]
- [x] [Review][Patch] Normalize relative imports in core import-boundary guardrail [tests/unit/test_core_import_boundaries.py:27]

## Dev Notes

### Implementation Scope

This story is only the greenfield scaffold and quality tooling baseline. It must not implement config schemas, workspace persistence, ingestion, GIS rendering, validation rules, export, or full UI screens. Those are separate stories. The goal is to leave the repository ready for all later implementation agents.

### Architecture Requirements

- Use a custom Python package scaffold, starting from `uv init --app` or an equivalent `uv`-managed project layout, then adapt it to the architecture source layout.
- Runtime app type is desktop Python with PySide6 Qt Widgets.
- Use `pyproject.toml` as the source of truth for project metadata, dependencies, pytest config, and ruff config.
- Source layout must be `src/thucthengay/`.
- Required top-level package modules: `models`, `config`, `workspace`, `ingestion`, `gis`, `render`, `validation`, `export`, `jobs`, `editor`, `utils`.
- Core services must remain headless-testable. `models`, `config`, `workspace`, `ingestion`, `gis`, `render`, `validation`, `export`, `jobs`, and `utils` must not import `PySide6.QtWidgets` or any `editor` module.
- `editor/` is the only package intended for PySide6 widgets/models/delegates.

### Recommended File Structure

```text
pyproject.toml
uv.lock
.python-version
README.md
src/thucthengay/
  __init__.py
  __main__.py
  app.py
  models/__init__.py
  config/__init__.py
  workspace/__init__.py
  ingestion/__init__.py
  gis/__init__.py
  render/__init__.py
  validation/__init__.py
  export/__init__.py
  jobs/__init__.py
  editor/__init__.py
  editor/modes/__init__.py
  editor/models/__init__.py
  editor/widgets/__init__.py
  editor/delegates/__init__.py
  utils/__init__.py
tests/
  fixtures/configs/
  fixtures/geojson/
  fixtures/geotiff/
  fixtures/templates/
  fixtures/workspaces/
  unit/test_package_import.py
  unit/test_core_import_boundaries.py
  integration/
```

### Dependency and Tooling Guidance

- Use Python 3.11 unless there is a documented reason to change it; the existing `environment.yml` already declares `python=3.11`, so `.python-version` and `pyproject.toml.requires-python` should stay compatible with that baseline.
- Use official `uv` project dependency management. `uv add` updates project dependencies; dev dependencies should use `uv add --dev` or dependency groups rather than ad hoc environment installs. [Source: uv dependency docs, https://docs.astral.sh/uv/concepts/projects/dependencies/]
- PySide6 is the official Qt for Python package for Qt 6 APIs and is installed as `PySide6`. [Source: Qt for Python, https://www.qt.io/development/qt-framework/python-bindings]
- Pydantic models should later inherit from `pydantic.BaseModel`; do not create those schemas in this story beyond package placeholders. [Source: Pydantic BaseModel docs, https://pydantic.dev/docs/validation/dev/api/pydantic/base_model/]
- Pytest supports configuration in `pyproject.toml`; keep tests runnable as `uv run pytest`. [Source: pytest configuration docs, https://docs.pytest.org/en/9.0.x/reference/customize.html]
- Ruff supports project configuration in `pyproject.toml` and can infer target version from `requires-python`; keep lint runnable as `uv run ruff check .`. [Source: Ruff configuration docs, https://docs.astral.sh/ruff/configuration/]

### Current Repository Context

Current project root contains planning artifacts and utility/sample assets but no finalized Python package scaffold. Existing files that must be preserved include:

- `_bmad-output/` planning and implementation artifacts.
- `_bmad/` and `.agents/` workflow assets.
- `scripts/copy_intersecting_geotiffs.py` and `scripts/extract_pptx_template_metadata.py`.
- `webapp_geojson/` helper web app.
- `Slide_1.pptx` and `Slide_1.template.json` sample/template assets.
- `environment.yml` existing environment note.

### Testing Requirements

- At minimum, add a smoke import test for `thucthengay`.
- Add an import-boundary test for core packages. Acceptable implementation: parse source files under core packages with `ast` and fail if they import `PySide6` or `thucthengay.editor`.
- Tests must not require network, local/LAN project data, GeoTIFF fixtures, PPTX files, or a Qt GUI event loop.
- GDAL/rasterio packaging is a known risk; if direct `uv add GDAL rasterio` cannot resolve reliably on this machine, document the chosen compatible install strategy in `README.md` and keep `pyproject.toml` consistent with the architecture decision rather than silently dropping GIS dependencies.
- The story is complete only if `uv run pytest` and `uv run ruff check .` pass after dependencies are installed.

### Anti-Patterns to Avoid

- Do not put business logic in `app.py` or `editor/`.
- Do not create models/services for Story 1.2+ in this story.
- Do not read/write workspace JSON directly from UI scaffold.
- Do not require actual satellite images or PowerPoint templates for scaffold tests.
- Do not hardcode user-specific absolute paths.
- Do not remove or reorganize existing BMAD/planning assets.

### References

- [Epics: Story 1.1] `_bmad-output/planning-artifacts/epics.md`
- [Architecture: Selected Starter / initialization command] `_bmad-output/planning-artifacts/architecture.md`
- [Architecture: Source layout and ownership rules] `_bmad-output/planning-artifacts/architecture.md`
- [Architecture: Development workflow commands] `_bmad-output/planning-artifacts/architecture.md`
- [PRD: MVP technology direction] `_bmad-output/planning-artifacts/prds/prd-3.ThucTheNgay-2026-05-23/prd.md`
- [uv dependency docs] https://docs.astral.sh/uv/concepts/projects/dependencies/
- [Qt for Python / PySide6] https://www.qt.io/development/qt-framework/python-bindings
- [Pydantic BaseModel docs] https://pydantic.dev/docs/validation/dev/api/pydantic/base_model/
- [pytest configuration docs] https://docs.pytest.org/en/9.0.x/reference/customize.html
- [Ruff configuration docs] https://docs.astral.sh/ruff/configuration/

## Project Structure Notes

- Expected app package name: `thucthengay`.
- Expected module path: `src/thucthengay/`.
- No existing app source tree is present at story creation time, so most files in this story are NEW.
- Existing `scripts/` are standalone utilities; do not pull them into package structure unless a later story explicitly does so.
- This workspace is currently not a git repository from the observed project root, so dev agents should not assume git status/commit automation is available.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-05-24: `uv --version` initially failed because `uv` was not installed on PATH.
- 2026-05-24: Installed `uv` into existing `ttn-env`; `uv run` installed the project dev tools, including `ruff`, from `uv.lock`.
- 2026-05-24: `conda run -n ttn-env uv lock` generated the real `uv.lock` after removing the temporary placeholder.
- 2026-05-24: `conda run -n ttn-env uv run pytest` passed: 2 tests collected, 2 passed.
- 2026-05-24: `conda run -n ttn-env uv run ruff check .` passed: all checks passed.
- 2026-05-24: `conda run -n ttn-env uv run python -m thucthengay` passed and printed the minimal scaffold message.
- 2026-05-25: Local shell did not have `uv`, `pytest`, or `ruff` on PATH; found conda at `/home/ongtu/miniconda3/bin/conda`.
- 2026-05-25: Installed `uv`, `pytest`, and `ruff` into `ttn-env` from conda-forge to run the documented fallback workflow.
- 2026-05-25: `python3 -m compileall src tests` passed.
- 2026-05-25: `PYTHONPATH=src python3 -m thucthengay` passed and printed the minimal scaffold message.
- 2026-05-25: Direct execution of the import-boundary test functions passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv pip install --no-deps -e .` passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` passed: 5 tests collected, 5 passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` passed: all checks passed.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay` passed and printed the minimal scaffold message.
- 2026-05-25: Code review rerun found remaining guardrail edge cases and missing fallback runtime dependencies; patched both.
- 2026-05-25: Installed `pyside6` and `pydantic` into `ttn-env` from conda-forge so the local environment matches the fallback dependency path.
- 2026-05-25: `/home/ongtu/miniconda3/bin/conda run -n ttn-env python -c "import PySide6, pydantic, numpy"` passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest` passed: 5 tests collected, 5 passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .` passed: all checks passed.
- 2026-05-25: Final `/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay` passed and printed the minimal scaffold message.

### Completion Notes List

- Resolved review finding: added `pyside6`, `pydantic`, and explicit `numpy` to `environment.yml` so the conda fallback includes all runtime dependencies declared by the scaffold.
- Resolved review finding: fixed package `__init__.py` context calculation and added a regression test that exercises `package_context_for_source()` directly.
- Resolved review finding: extended dynamic import detection for importlib aliases, `from importlib import import_module`, function aliases, relative import strings, and `__package__`-based package context.
- Resolved review finding: revised the conda GDAL fallback to avoid `uv sync`, install only this app with `uv pip install --no-deps -e .`, and run commands with `uv run --no-sync` so conda-forge keeps ownership of native GIS packages.
- Resolved review finding: changed relative import analysis to use package context for both module files and package `__init__.py` files.
- Resolved review finding: added constant-string dynamic import detection for `importlib.import_module(...)` and `__import__(...)` to the core import-boundary guardrail.
- Resolved review finding: documented the conda+uv fallback with `UV_PROJECT_ENVIRONMENT` so uv uses `ttn-env` instead of creating a separate `.venv`.
- Resolved review finding: constrained package metadata to Python `>=3.11,<3.12` and regenerated `uv.lock`.
- Resolved review finding: normalized relative imports in the core import-boundary guardrail and added a direct regression test for `from ..editor import widgets`.
- Initialized the Python project scaffold with `pyproject.toml`, `.python-version`, generated `uv.lock`, `.gitignore`, and README development instructions.
- Added the `src/thucthengay` package layout and required architecture packages, keeping core modules headless and UI code isolated under `editor/`.
- Added smoke import coverage and an AST-based import-boundary guardrail test for non-UI core packages.
- Configured pytest and ruff in `pyproject.toml`; ruff excludes preserved BMAD/workflow and legacy utility assets so `ruff check .` validates the scaffold cleanly.

### File List

- `.gitignore`
- `.python-version`
- `README.md`
- `environment.yml`
- `pyproject.toml`
- `uv.lock`
- `src/thucthengay/__init__.py`
- `src/thucthengay/__main__.py`
- `src/thucthengay/app.py`
- `src/thucthengay/models/__init__.py`
- `src/thucthengay/config/__init__.py`
- `src/thucthengay/workspace/__init__.py`
- `src/thucthengay/ingestion/__init__.py`
- `src/thucthengay/gis/__init__.py`
- `src/thucthengay/render/__init__.py`
- `src/thucthengay/validation/__init__.py`
- `src/thucthengay/export/__init__.py`
- `src/thucthengay/jobs/__init__.py`
- `src/thucthengay/editor/__init__.py`
- `src/thucthengay/editor/modes/__init__.py`
- `src/thucthengay/editor/models/__init__.py`
- `src/thucthengay/editor/widgets/__init__.py`
- `src/thucthengay/editor/delegates/__init__.py`
- `src/thucthengay/utils/__init__.py`
- `tests/unit/test_package_import.py`
- `tests/unit/test_core_import_boundaries.py`
- `tests/integration/.gitkeep`
- `tests/fixtures/configs/.gitkeep`
- `tests/fixtures/geojson/.gitkeep`
- `tests/fixtures/geotiff/.gitkeep`
- `tests/fixtures/templates/.gitkeep`
- `tests/fixtures/workspaces/.gitkeep`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `_bmad-output/implementation-artifacts/1-1-initialize-application-scaffold-and-quality-tooling.md`

### Change Log

- 2026-05-25: Completed code review rerun patches for conda fallback runtime dependencies and import-boundary dynamic import edge cases.
- 2026-05-25: Addressed remaining code review findings for conda GIS fallback, package `__init__.py` relative import resolution, and constant-string dynamic import detection.
- 2026-05-24: Addressed code review findings - 3 patch items resolved.
- 2026-05-24: Implemented Story 1.1 scaffold, tests, quality tooling, and validation commands.
