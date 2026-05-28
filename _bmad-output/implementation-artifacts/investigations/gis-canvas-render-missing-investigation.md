# GIS Canvas Render Missing Investigation

## Case Info

- Date: 2026-05-28
- Input: "ảnh vẫn chưa render ra canvas GIS Editor"
- Status: Concluded

## Evidence

- Confirmed: `examples/workspace_1/compositions/BaicanScarborough__20260526.json` stores layer `cache_path` as workspace-relative `cache/...` while `source_path` is absolute.
- Confirmed: `src/thucthengay/render/raster.py` opens `layer.cache_path or layer.source_path`, so a relative `cache_path` wins over an absolute `source_path`.
- Confirmed: `src/thucthengay/editor/modes/review_edit_mode.py` built `RenderSpec` directly from persisted composition layers before this fix.

## Conclusion

Root cause: canvas preview passed workspace-relative cache paths into the renderer without resolving them against the active workspace root. The renderer therefore attempted to open `cache/...` relative to the process working directory, not `examples/workspace_1/cache/...`, so valid cached GeoTIFFs were not found by the GIS canvas render job.

Confidence: High.

## Fix

- Added a transient `WorkspaceService.resolve_composition_layer_paths()` helper that keeps persisted JSON unchanged and returns a composition copy with absolute layer paths.
- Used the resolved composition when Review/Edit GIS canvas builds `RenderSpec`.
- Applied the same resolution to final render/export spec generation so preview and final render share the same path semantics.

## Verification

- `conda run -n ttn-env python -m pytest tests/unit/test_workspace_service.py tests/unit/test_export_final_render.py tests/unit/test_review_edit_mode.py` reported `62 passed`.
- `conda run -n ttn-env python -m ruff check ...` reported `All checks passed!`.
- Manual render smoke check for `BaicanScarborough__20260526` produced canvas shape `(360, 640, 3)` and painted two layer ids with zero render issues.
