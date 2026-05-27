"""Coordinate frame drawing for map renders.

Story 5.3 renders an outer coordinate frame with edge ticks and labels. It
intentionally does not draw an internal grid mesh across the raster area.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from thucthengay.models.config import GridConfig
from thucthengay.models.issue import Issue, IssueScope, IssueSeverity
from thucthengay.render.raster import RenderError
from thucthengay.render.spec import GeoWindow, RenderSpec

_SUPPORTED_LABEL_FORMATS = {"dms_full", "dms_short"}
_EPSILON = 1e-10
_MAX_FRAME_TICKS_PER_AXIS = 2000


@dataclass(frozen=True)
class FrameStyle:
    """Resolved visual style for the coordinate frame."""

    frame_color: tuple[int, int, int] = (0, 0, 0)
    label_color: tuple[int, int, int] = (0, 0, 0)
    label_halo_color: tuple[int, int, int] = (255, 255, 255)
    tick_length: int = 6
    label_padding: int = 3


def _issue(
    issue_id: str,
    message: str,
    remediation: str,
    *,
    composition_id: str,
    target_id: str,
) -> Issue:
    return Issue(
        issue_id=issue_id,
        severity=IssueSeverity.ERROR,
        scope=IssueScope.RENDER,
        target_id=target_id,
        composition_id=composition_id,
        message=message,
        remediation=remediation,
    )


def _parse_hex_color(value: object, *, fallback: tuple[int, int, int]) -> tuple[int, int, int]:
    if not isinstance(value, str):
        return fallback
    text = value.strip().lstrip("#")
    if len(text) != 6:
        return fallback
    try:
        return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)
    except ValueError:
        return fallback


def _positive_int(value: object, *, fallback: int, min_value: int = 1) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed >= min_value else fallback


def _frame_style(grid: GridConfig) -> FrameStyle:
    style = grid.style
    default = FrameStyle()
    return FrameStyle(
        frame_color=_parse_hex_color(style.get("frame_color"), fallback=default.frame_color),
        label_color=_parse_hex_color(style.get("label_color"), fallback=default.label_color),
        label_halo_color=_parse_hex_color(
            style.get("label_halo_color"), fallback=default.label_halo_color
        ),
        tick_length=_positive_int(style.get("tick_length"), fallback=default.tick_length),
        label_padding=_positive_int(
            style.get("label_padding"), fallback=default.label_padding, min_value=0
        ),
    )


def _interval_degrees(spec: RenderSpec) -> float:
    interval = spec.grid.interval
    value = (
        float(interval.degrees)
        + float(interval.minutes) / 60.0
        + float(interval.seconds) / 3600.0
    )
    if not math.isfinite(value) or value <= 0.0:
        raise RenderError(
            [
                _issue(
                    "render.frame.interval_invalid",
                    "Khoang coordinate frame khong hop le.",
                    "Sua grid.interval de tong do/phut/giay lon hon 0 truoc khi render.",
                    composition_id=spec.composition_id,
                    target_id=spec.target_id,
                )
            ]
        )
    return value


def _frame_issue(
    spec: RenderSpec,
    issue_id: str,
    message: str,
    remediation: str,
) -> RenderError:
    return RenderError(
        [
            _issue(
                issue_id,
                message,
                remediation,
                composition_id=spec.composition_id,
                target_id=spec.target_id,
            )
        ]
    )


def _validate_label_format(spec: RenderSpec) -> str:
    label_format = "dms_full" if spec.grid.label_format is None else spec.grid.label_format.strip()
    if label_format not in _SUPPORTED_LABEL_FORMATS:
        raise _frame_issue(
            spec,
            "render.frame.label_format_invalid",
            "Dinh dang nhan coordinate frame khong duoc ho tro.",
            "Dung label_format la 'dms_full' hoac 'dms_short' truoc khi render.",
        )
    return label_format


def _tick_values(
    min_value: float, max_value: float, interval: float, spec: RenderSpec
) -> list[float]:
    first = math.ceil((min_value - _EPSILON) / interval) * interval
    if first > max_value + _EPSILON:
        return []

    tick_count = math.floor((max_value - first + _EPSILON) / interval) + 1
    if tick_count > _MAX_FRAME_TICKS_PER_AXIS:
        raise _frame_issue(
            spec,
            "render.frame.interval_too_dense",
            "Khoang coordinate frame qua day de render an toan.",
            (
                "Tang grid.interval de so tick tren moi truc khong vuot "
                f"{_MAX_FRAME_TICKS_PER_AXIS}."
            ),
        )

    values: list[float] = []
    current = first
    for _ in range(tick_count):
        if current >= min_value - _EPSILON:
            values.append(round(current, 10))
        current += interval
    return values


def _lon_to_x(window: GeoWindow, width: int, lon: float) -> int:
    ratio = (lon - window.min_lon) / (window.max_lon - window.min_lon)
    return max(0, min(width - 1, int(round(ratio * (width - 1)))))


def _lat_to_y(window: GeoWindow, height: int, lat: float) -> int:
    ratio = (window.max_lat - lat) / (window.max_lat - window.min_lat)
    return max(0, min(height - 1, int(round(ratio * (height - 1)))))


def _format_dms(value: float, *, axis: str, label_format: str) -> str:
    hemisphere = ("E" if value >= 0 else "W") if axis == "lon" else ("N" if value >= 0 else "S")
    absolute = abs(value)
    degrees = int(math.floor(absolute))
    minutes_float = (absolute - degrees) * 60.0
    minutes = int(math.floor(minutes_float))
    seconds = int(round((minutes_float - minutes) * 60.0))
    if seconds == 60:
        seconds = 0
        minutes += 1
    if minutes == 60:
        minutes = 0
        degrees += 1

    if label_format == "dms_short":
        return f"{degrees:02d}d{minutes:02d}m{hemisphere}"
    return f"{degrees:02d}d{minutes:02d}m{seconds:02d}s{hemisphere}"


def _draw_text_with_halo(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    *,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    halo: tuple[int, int, int],
) -> None:
    x, y = xy
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), text, font=font, fill=halo)
    draw.text((x, y), text, font=font, fill=fill)


def _clamped_text_origin(
    draw: ImageDraw.ImageDraw,
    text: str,
    desired: tuple[int, int],
    *,
    font: ImageFont.ImageFont,
    width: int,
    height: int,
) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    max_x = max(0, width - text_w - 1)
    max_y = max(0, height - text_h - 1)
    return max(0, min(desired[0], max_x)), max(0, min(desired[1], max_y))


def draw_coordinate_frame(canvas: np.ndarray, spec: RenderSpec) -> np.ndarray:
    """Draw an outer coordinate frame over ``canvas`` and return the same array."""
    if canvas.ndim != 3 or canvas.shape[2] != 3:
        raise RenderError(
            [
                _issue(
                    "render.frame.canvas_invalid",
                    "Canvas render khong dung dinh dang RGB.",
                    "Render frame can canvas numpy co shape (height, width, 3).",
                    composition_id=spec.composition_id,
                    target_id=spec.target_id,
                )
            ]
        )

    height, width = canvas.shape[:2]
    if width <= 1 or height <= 1:
        raise RenderError(
            [
                _issue(
                    "render.frame.canvas_too_small",
                    "Canvas render qua nho de ve coordinate frame.",
                    "Tang output_width/output_height truoc khi render.",
                    composition_id=spec.composition_id,
                    target_id=spec.target_id,
                )
            ]
        )

    interval = _interval_degrees(spec)
    label_format = _validate_label_format(spec)
    style = _frame_style(spec.grid)

    image = Image.fromarray(canvas, mode="RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.rectangle((0, 0, width - 1, height - 1), outline=style.frame_color, width=1)

    tick_len = min(style.tick_length, max(1, min(width, height) // 4))
    for lon in _tick_values(spec.geo_window.min_lon, spec.geo_window.max_lon, interval, spec):
        x = _lon_to_x(spec.geo_window, width, lon)
        draw.line((x, 0, x, tick_len), fill=style.frame_color, width=1)
        draw.line((x, height - 1 - tick_len, x, height - 1), fill=style.frame_color, width=1)
        label = _format_dms(lon, axis="lon", label_format=label_format)
        origin = _clamped_text_origin(
            draw,
            label,
            (x + style.label_padding, style.label_padding),
            font=font,
            width=width,
            height=height,
        )
        _draw_text_with_halo(
            draw,
            origin,
            label,
            font=font,
            fill=style.label_color,
            halo=style.label_halo_color,
        )
        bottom_origin = _clamped_text_origin(
            draw,
            label,
            (x + style.label_padding, height - style.label_padding),
            font=font,
            width=width,
            height=height,
        )
        _draw_text_with_halo(
            draw,
            bottom_origin,
            label,
            font=font,
            fill=style.label_color,
            halo=style.label_halo_color,
        )

    for lat in _tick_values(spec.geo_window.min_lat, spec.geo_window.max_lat, interval, spec):
        y = _lat_to_y(spec.geo_window, height, lat)
        draw.line((0, y, tick_len, y), fill=style.frame_color, width=1)
        draw.line((width - 1 - tick_len, y, width - 1, y), fill=style.frame_color, width=1)
        label = _format_dms(lat, axis="lat", label_format=label_format)
        origin = _clamped_text_origin(
            draw,
            label,
            (style.label_padding, y + style.label_padding),
            font=font,
            width=width,
            height=height,
        )
        _draw_text_with_halo(
            draw,
            origin,
            label,
            font=font,
            fill=style.label_color,
            halo=style.label_halo_color,
        )
        right_origin = _clamped_text_origin(
            draw,
            label,
            (width - style.label_padding, y + style.label_padding),
            font=font,
            width=width,
            height=height,
        )
        _draw_text_with_halo(
            draw,
            right_origin,
            label,
            font=font,
            fill=style.label_color,
            halo=style.label_halo_color,
        )

    np.copyto(canvas, np.asarray(image, dtype=np.uint8))
    return canvas
