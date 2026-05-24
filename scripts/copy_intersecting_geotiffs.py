#!/usr/bin/env python3
"""Copy GeoTIFF files whose spatial extent intersects a GeoJSON geometry.

Dependencies:
    pip install rasterio shapely

Examples:
    python scripts/copy_intersecting_geotiffs.py \
        --geojson regions.geojson \
        --input-dir /data/geotiff \
        --output-dir /data/selected

    # Copy all intersecting rasters into one flat output folder.
    python scripts/copy_intersecting_geotiffs.py -g regions.geojson -i tif_dir -o out --flat
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import rasterio
from rasterio.crs import CRS
from rasterio.errors import RasterioIOError
from rasterio.warp import transform_geom
from shapely.geometry import box, shape
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union


GEOTIFF_SUFFIXES = {".tif", ".tiff"}


@dataclass(frozen=True)
class CopyResult:
    scanned: int = 0
    matched: int = 0
    copied: int = 0
    skipped_existing: int = 0
    failed: int = 0

    def add(self, **kwargs: int) -> "CopyResult":
        values = self.__dict__.copy()
        for key, delta in kwargs.items():
            values[key] += delta
        return CopyResult(**values)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy GeoTIFF files that intersect any polygon/geometry in a GeoJSON file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-g", "--geojson", required=True, type=Path, help="Path to input GeoJSON.")
    parser.add_argument(
        "-i",
        "--input-dir",
        required=True,
        type=Path,
        help="Folder containing GeoTIFF files. Subfolders are scanned recursively.",
    )
    parser.add_argument("-o", "--output-dir", required=True, type=Path, help="Destination folder.")
    parser.add_argument(
        "--geojson-crs",
        default=None,
        help=(
            "CRS of the GeoJSON, for example EPSG:4326 or EPSG:3405. "
            "If omitted, the script uses GeoJSON 'crs' when present, otherwise EPSG:4326."
        ),
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Copy matching files directly into output-dir instead of preserving relative subfolders.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite files already in output-dir.")
    parser.add_argument("--dry-run", action="store_true", help="Print matched files without copying.")
    parser.add_argument(
        "--include-boundary-touch",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Treat files that only touch the GeoJSON boundary as matches. "
            "Use --no-include-boundary-touch to require area overlap."
        ),
    )
    return parser.parse_args()


def read_geojson_crs(data: dict, explicit_crs: str | None) -> CRS:
    if explicit_crs:
        return CRS.from_user_input(explicit_crs)

    crs_info = data.get("crs")
    if isinstance(crs_info, dict):
        properties = crs_info.get("properties") or {}
        name = properties.get("name")
        if name:
            return CRS.from_user_input(name)

    return CRS.from_epsg(4326)


def extract_geometries(data: dict) -> list[BaseGeometry]:
    data_type = data.get("type")

    if data_type == "FeatureCollection":
        raw_geometries = [
            feature.get("geometry")
            for feature in data.get("features", [])
            if isinstance(feature, dict) and feature.get("geometry")
        ]
    elif data_type == "Feature":
        raw_geometries = [data.get("geometry")]
    else:
        raw_geometries = [data]

    geometries: list[BaseGeometry] = []
    for raw_geometry in raw_geometries:
        if not raw_geometry:
            continue
        geometry = shape(raw_geometry)
        if geometry.is_empty:
            continue
        if not geometry.is_valid:
            geometry = geometry.buffer(0)
        if not geometry.is_empty:
            geometries.append(geometry)

    return geometries


def load_geojson_union(geojson_path: Path, explicit_crs: str | None) -> tuple[BaseGeometry, CRS]:
    with geojson_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    geometries = extract_geometries(data)
    if not geometries:
        raise ValueError(f"No usable geometries found in GeoJSON: {geojson_path}")

    return unary_union(geometries), read_geojson_crs(data, explicit_crs)


def iter_geotiffs(input_dir: Path) -> Iterable[Path]:
    for path in input_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in GEOTIFF_SUFFIXES:
            yield path


def geometry_for_raster_crs(
    geometry: BaseGeometry,
    source_crs: CRS,
    target_crs: CRS | None,
    cache: dict[str, BaseGeometry],
) -> BaseGeometry:
    if target_crs is None or target_crs == source_crs:
        return geometry

    cache_key = target_crs.to_string()
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    transformed = shape(transform_geom(source_crs, target_crs, geometry.__geo_interface__))
    if not transformed.is_valid:
        transformed = transformed.buffer(0)
    cache[cache_key] = transformed
    return transformed


def output_path_for(source_path: Path, input_dir: Path, output_dir: Path, flat: bool) -> Path:
    if flat:
        return output_dir / source_path.name
    return output_dir / source_path.relative_to(input_dir)


def paths_are_same(source_path: Path, destination_path: Path) -> bool:
    try:
        return source_path.resolve() == destination_path.resolve()
    except OSError:
        return False


def copy_matching_geotiffs(
    geojson_geometry: BaseGeometry,
    geojson_crs: CRS,
    input_dir: Path,
    output_dir: Path,
    flat: bool,
    overwrite: bool,
    dry_run: bool,
    include_boundary_touch: bool,
) -> CopyResult:
    result = CopyResult()
    geometry_cache: dict[str, BaseGeometry] = {}

    for raster_path in iter_geotiffs(input_dir):
        result = result.add(scanned=1)

        try:
            with rasterio.open(raster_path) as dataset:
                raster_bounds = box(*dataset.bounds)
                comparable_geometry = geometry_for_raster_crs(
                    geojson_geometry,
                    geojson_crs,
                    dataset.crs,
                    geometry_cache,
                )
        except (RasterioIOError, ValueError) as exc:
            print(f"[WARN] Cannot read {raster_path}: {exc}", file=sys.stderr)
            result = result.add(failed=1)
            continue

        intersects = raster_bounds.intersects(comparable_geometry)
        if intersects and not include_boundary_touch:
            intersects = raster_bounds.intersection(comparable_geometry).area > 0
        if not intersects:
            continue

        result = result.add(matched=1)
        destination_path = output_path_for(raster_path, input_dir, output_dir, flat)

        if paths_are_same(raster_path, destination_path):
            print(f"[WARN] Source and destination are the same, skipped: {raster_path}", file=sys.stderr)
            result = result.add(skipped_existing=1)
            continue

        print(f"{raster_path} -> {destination_path}")
        if dry_run:
            continue

        if destination_path.exists() and not overwrite:
            print(f"[SKIP] Exists: {destination_path}", file=sys.stderr)
            result = result.add(skipped_existing=1)
            continue

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(raster_path, destination_path)
        result = result.add(copied=1)

    return result


def validate_paths(geojson_path: Path, input_dir: Path, output_dir: Path) -> None:
    if not geojson_path.is_file():
        raise FileNotFoundError(f"GeoJSON file does not exist: {geojson_path}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")
    if input_dir.resolve() == output_dir.resolve():
        raise ValueError("output-dir must be different from input-dir")


def main() -> int:
    args = parse_args()

    try:
        validate_paths(args.geojson, args.input_dir, args.output_dir)
        geojson_geometry, geojson_crs = load_geojson_union(args.geojson, args.geojson_crs)
        result = copy_matching_geotiffs(
            geojson_geometry=geojson_geometry,
            geojson_crs=geojson_crs,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            flat=args.flat,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            include_boundary_touch=args.include_boundary_touch,
        )
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(
        "Done: "
        f"scanned={result.scanned}, "
        f"matched={result.matched}, "
        f"copied={result.copied}, "
        f"skipped_existing={result.skipped_existing}, "
        f"failed={result.failed}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
