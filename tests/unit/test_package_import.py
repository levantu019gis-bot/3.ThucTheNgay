from __future__ import annotations

import importlib


def test_package_imports_without_runtime_side_effects() -> None:
    package = importlib.import_module("thucthengay")

    assert package.__version__ == "0.1.0"
