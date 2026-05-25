#!/usr/bin/env python3
import argparse
import copy
import json
import math
import re
import unicodedata
from pathlib import Path


def strip_vietnamese_accents(value):
    normalized = unicodedata.normalize("NFD", value)
    without_marks = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )
    return without_marks.replace("đ", "d").replace("Đ", "D")


def normalize_name(value):
    value = str(value).replace("/", "_").replace(",", "_")
    value = strip_vietnamese_accents(value)
    return "".join(value.split())


def fallback_name(feature, index):
    properties = feature.get("properties") or {}
    feature_id = properties.get("id", index + 1)
    return f"feature_{feature_id}"


def first_nonblank(*values):
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return None


def ring_centroid(ring):
    if len(ring) < 3:
        return 0.0, None

    points = ring[:]
    if points[0] != points[-1]:
        points.append(points[0])

    area2 = 0.0
    cx_factor = 0.0
    cy_factor = 0.0

    for point_a, point_b in zip(points, points[1:]):
        x0, y0 = point_a[:2]
        x1, y1 = point_b[:2]
        cross = x0 * y1 - x1 * y0
        area2 += cross
        cx_factor += (x0 + x1) * cross
        cy_factor += (y0 + y1) * cross

    if math.isclose(area2, 0.0, abs_tol=1e-15):
        return 0.0, None

    return area2 / 2.0, (cx_factor / (3.0 * area2), cy_factor / (3.0 * area2))


def iter_positions(coordinates):
    if not isinstance(coordinates, list):
        return

    if coordinates and isinstance(coordinates[0], (int, float)):
        if len(coordinates) >= 2:
            yield coordinates[:2]
        return

    for item in coordinates:
        yield from iter_positions(item)


def average_position(coordinates):
    positions = list(iter_positions(coordinates))
    if not positions:
        raise ValueError("geometry does not contain coordinates")

    lon = sum(point[0] for point in positions) / len(positions)
    lat = sum(point[1] for point in positions) / len(positions)
    return lon, lat


def polygon_centroid(rings):
    weighted_area = 0.0
    weighted_lon = 0.0
    weighted_lat = 0.0

    for ring in rings:
        area, centroid = ring_centroid(ring)
        if centroid is None:
            continue
        weighted_area += area
        weighted_lon += centroid[0] * area
        weighted_lat += centroid[1] * area

    if math.isclose(weighted_area, 0.0, abs_tol=1e-15):
        return average_position(rings)

    return weighted_lon / weighted_area, weighted_lat / weighted_area


def geometry_centroid(geometry):
    if not geometry:
        raise ValueError("feature does not contain geometry")

    geometry_type = geometry.get("type")
    coordinates = geometry.get("coordinates")

    if geometry_type == "Point":
        return coordinates[0], coordinates[1]

    if geometry_type == "Polygon":
        return polygon_centroid(coordinates)

    if geometry_type == "MultiPolygon":
        weighted_area = 0.0
        weighted_lon = 0.0
        weighted_lat = 0.0

        for polygon in coordinates:
            polygon_area = 0.0
            polygon_lon = 0.0
            polygon_lat = 0.0

            for ring in polygon:
                area, centroid = ring_centroid(ring)
                if centroid is None:
                    continue
                polygon_area += area
                polygon_lon += centroid[0] * area
                polygon_lat += centroid[1] * area

            if math.isclose(polygon_area, 0.0, abs_tol=1e-15):
                continue

            polygon_centroid_lon = polygon_lon / polygon_area
            polygon_centroid_lat = polygon_lat / polygon_area
            weighted_area += polygon_area
            weighted_lon += polygon_centroid_lon * polygon_area
            weighted_lat += polygon_centroid_lat * polygon_area

        if not math.isclose(weighted_area, 0.0, abs_tol=1e-15):
            return weighted_lon / weighted_area, weighted_lat / weighted_area

    return average_position(coordinates)


def unique_path(output_dir, stem, used_stems):
    safe_stem = re.sub(r'[<>:"\\\\|?*]', "_", stem).strip(".")
    if not safe_stem:
        safe_stem = "feature"

    candidate = safe_stem
    counter = 2
    while candidate in used_stems:
        candidate = f"{safe_stem}_{counter}"
        counter += 1

    used_stems.add(candidate)
    return output_dir / f"{candidate}.geojson"


def process_geojson(input_path, output_dir, output_name):
    with input_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if data.get("type") != "FeatureCollection":
        raise ValueError("input GeoJSON must be a FeatureCollection")

    output_dir.mkdir(parents=True, exist_ok=True)
    processed = copy.deepcopy(data)
    used_feature_file_stems = set()

    for index, feature in enumerate(processed.get("features", [])):
        properties = feature.setdefault("properties", {})
        display_name = first_nonblank(
            properties.get("alias"),
            properties.get("name"),
            fallback_name(feature, index),
        )
        lon, lat = geometry_centroid(feature.get("geometry"))

        properties["center"] = [lat, lon]
        properties["alias"] = display_name
        properties["name"] = normalize_name(display_name)
        group_value = properties.get("group")
        if group_value is None or (isinstance(group_value, str) and not group_value.strip()):
            properties["group"] = 0.0

        feature_path = unique_path(output_dir, properties["name"], used_feature_file_stems)
        with feature_path.open("w", encoding="utf-8") as file:
            json.dump(feature, file, ensure_ascii=False, indent=2)
            file.write("\n")

    output_path = output_dir / output_name
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(processed, file, ensure_ascii=False, indent=2)
        file.write("\n")

    return output_path, len(processed.get("features", []))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process GeoJSON features: center, alias, normalized name, group."
    )
    parser.add_argument("--input", default="all.geojson", help="Input GeoJSON file.")
    parser.add_argument(
        "--output-dir",
        default="output_geojson",
        help="Folder for the processed GeoJSON files.",
    )
    parser.add_argument(
        "--output-name",
        default="all_processed.geojson",
        help="Filename for the processed FeatureCollection.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_path, feature_count = process_geojson(
        Path(args.input), Path(args.output_dir), args.output_name
    )
    print(f"Processed {feature_count} features")
    print(f"Output FeatureCollection: {output_path}")
    print(f"Individual feature files: {Path(args.output_dir)}")


if __name__ == "__main__":
    main()
