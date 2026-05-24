from __future__ import annotations

import ast
from pathlib import Path

PACKAGE_ROOT = "thucthengay"
CORE_PACKAGES = {
    "models",
    "config",
    "workspace",
    "ingestion",
    "gis",
    "render",
    "validation",
    "export",
    "jobs",
    "utils",
}


def module_path_for_source(package_root: Path, source: Path) -> str:
    relative = source.relative_to(package_root).with_suffix("")
    parts = relative.parts[:-1] if relative.name == "__init__" else relative.parts
    return ".".join((PACKAGE_ROOT, *parts))


def resolve_import_from(module_path: str, node: ast.ImportFrom) -> set[str]:
    if node.level == 0:
        return {node.module} if node.module else set()

    package_parts = module_path.split(".")
    base_parts = package_parts[: max(len(package_parts) - node.level, 0)]
    if node.module:
        base_parts.extend(node.module.split("."))

    resolved = ".".join(base_parts)
    modules = {resolved} if resolved else set()
    modules.update(f"{resolved}.{alias.name}" for alias in node.names if resolved)
    return modules


def imported_modules(package_root: Path, source: Path) -> set[str]:
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    imports: set[str] = set()
    module_path = module_path_for_source(package_root, source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.update(resolve_import_from(module_path, node))

    return imports


def test_relative_imports_are_resolved_to_absolute_module_names() -> None:
    tree = ast.parse("from ..editor import widgets\nfrom .. import editor\n")
    import_from_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]

    modules = set()
    for node in import_from_nodes:
        modules.update(resolve_import_from("thucthengay.models.service", node))

    assert "thucthengay.editor" in modules
    assert "thucthengay.editor.widgets" in modules


def test_core_packages_do_not_import_qt_or_editor_modules() -> None:
    package_root = Path(__file__).parents[2] / "src" / "thucthengay"
    violations: list[str] = []

    for package_name in sorted(CORE_PACKAGES):
        for source in (package_root / package_name).rglob("*.py"):
            for module_name in imported_modules(package_root, source):
                if module_name == "PySide6" or module_name.startswith("PySide6."):
                    violations.append(f"{source}: imports {module_name}")
                if module_name == "thucthengay.editor" or module_name.startswith(
                    "thucthengay.editor."
                ):
                    violations.append(f"{source}: imports {module_name}")

    assert violations == []
