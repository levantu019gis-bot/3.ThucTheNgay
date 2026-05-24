# 3.ThucTheNgay

Python desktop application scaffold for preparing satellite imagery report outputs.

## Development

This project uses Python 3.11 and `uv` project management.

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
python -m pip install uv
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv sync --dev
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run pytest
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run ruff check .
UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run python -m thucthengay
```

`UV_PROJECT_ENVIRONMENT` is required for this fallback path so `uv` installs into and runs from
the active conda environment instead of creating a separate project `.venv`.
