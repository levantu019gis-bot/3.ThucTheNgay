# 3.ThucTheNgay

Python desktop application scaffold for preparing satellite imagery report outputs.

## Development

This project uses Python 3.11 and `uv` project management.

### Run the app

Windows PowerShell:

```powershell
.\run_windows.ps1
```

Windows Command Prompt:

```bat
run_windows.bat
```

Ubuntu:

```bash
chmod +x ./run_ubuntu.sh
./run_ubuntu.sh
```

All launchers use the conda environment `ttn-env` by default and set `PYTHONPATH=src` before
running `python -m thucthengay`. To use a different conda environment, set `TTN_CONDA_ENV`.

### Generate real data config

The current real target config is generated from one GeoJSON `Feature` per target in
`webapp_geojson/output_geojson`. Each GeoJSON `properties.center` is treated as `[lat, lon]` and
written to app config `coordinate` as `[lon, lat]`. The original GeoJSON `properties` and
`geometry` are preserved under each target's `metadata`.

```powershell
conda run -n ttn-env python scripts\generate_template_metadata.py `
  examples\templates\target_001.template.pptx `
  --output examples\templates\target_001.template.json

conda run -n ttn-env python scripts\generate_config_from_geojson.py `
  webapp_geojson\output_geojson `
  --output config.json `
  --template-pptx examples\templates\target_001.template.pptx `
  --map-element-id 1026
```

`config.json` points directly to the one-slide PPTX template through
`export.template_pptx_file`. `scripts/generate_template_metadata.py` is now an inspection aid for
discovering shape ids and text content; the app does not require the generated JSON at runtime.

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run python -m thucthengay
```

The current scaffold keeps tests independent from project data, network access, GeoTIFF files,
PowerPoint templates, and a Qt event loop.

## GDAL-compatible install path

`rasterio` is the configured raster/GDAL access layer for the MVP package. On most supported
platforms its wheels provide the compatible GDAL runtime needed by the application. If a platform
cannot use those wheels, create the environment from `environment.yml` so GDAL, rasterio, pyproj,
and shapely are resolved together by conda-forge:

```bash
conda env create -f environment.yml
conda activate ttn-env
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv pip install --no-deps -e .
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run --no-sync pytest
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run --no-sync ruff check .
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run --no-sync python -m thucthengay
```

This fallback intentionally avoids `uv sync` so `uv` does not replace conda-forge's native GIS
packages with PyPI wheels. `uv pip install --no-deps -e .` installs only this application package;
`UV_PROJECT_ENVIRONMENT` keeps `uv run` inside the active conda environment instead of creating a
separate project `.venv`; conda remains responsible for GDAL, rasterio, pyproj, shapely, Pillow,
and python-pptx.
