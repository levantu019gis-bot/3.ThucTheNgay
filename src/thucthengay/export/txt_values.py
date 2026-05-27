"""Shared TXT export placeholder resolution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from string import Formatter
from typing import Any

from thucthengay.models import Composition, MetadataStatus, TargetConfig

SUPPORTED_TXT_FIELDS = {
    "capture_date",
    "composition_id",
    "slide_number",
    "target_alias",
    "target_id",
    "target_name",
    "target_title",
    "time_label",
}


@dataclass(frozen=True)
class TxtPlaceholderProblem:
    """One unresolved TXT placeholder problem."""

    field: str
    issue_id: str
    optional: bool


@dataclass(frozen=True)
class TxtLineResolution:
    """Resolved TXT line or placeholder problems."""

    text: str
    problems: tuple[TxtPlaceholderProblem, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.problems


def resolve_txt_line(
    template: str,
    composition: Composition,
    target: TargetConfig,
    *,
    slide_number: int,
) -> TxtLineResolution:
    """Render one TXT line, supporting optional placeholders as ``{field?}``."""
    values = txt_values(composition, target, slide_number)
    parts: list[str] = []
    problems: list[TxtPlaceholderProblem] = []
    for literal, field_name, format_spec, conversion in Formatter().parse(template):
        parts.append(literal)
        if not field_name:
            continue
        field, optional = _parse_field(field_name)
        value = values.get(field)
        if field not in SUPPORTED_TXT_FIELDS:
            problems.append(
                TxtPlaceholderProblem(
                    field=field,
                    issue_id="export.txt_placeholder_unknown",
                    optional=optional,
                )
            )
            continue
        if value in (None, ""):
            if optional:
                parts.append("")
                continue
            problems.append(
                TxtPlaceholderProblem(
                    field=field,
                    issue_id=(
                        "export.txt_time_label_unresolved"
                        if field == "time_label"
                        else "export.txt_placeholder_unresolved"
                    ),
                    optional=False,
                )
            )
            continue
        parts.append(_format_value(value, format_spec, conversion))
    return TxtLineResolution(text="".join(parts), problems=tuple(problems))


def txt_values(
    composition: Composition,
    target: TargetConfig,
    slide_number: int,
) -> dict[str, Any]:
    """Return supported TXT placeholder values for one export row."""
    return {
        "capture_date": composition.capture_date.isoformat(),
        "composition_id": composition.composition_id,
        "slide_number": slide_number,
        "target_alias": target.alias or "",
        "target_id": target.id,
        "target_name": target.name,
        "target_title": target.title or target.name,
        "time_label": time_label(composition),
    }


def time_label(composition: Composition) -> str:
    """Return the earliest visible valid layer capture time."""
    visible_times = [
        layer.capture_time
        for layer in composition.layers
        if layer.visible
        and layer.metadata_status == MetadataStatus.VALID
        and layer.capture_time is not None
    ]
    if not visible_times:
        return ""
    return _format_time(min(visible_times))


def _parse_field(field_name: str) -> tuple[str, bool]:
    normalized = field_name.split(".", 1)[0].split("[", 1)[0]
    if normalized.endswith("?"):
        return normalized[:-1], True
    return normalized, False


def _format_value(value: Any, format_spec: str, conversion: str | None) -> str:
    if conversion == "r":
        value = repr(value)
    elif conversion == "s":
        value = str(value)
    elif conversion == "a":
        value = ascii(value)
    if format_spec:
        return format(value, format_spec)
    return str(value)


def _format_time(value: time) -> str:
    return value.strftime("%H:%M:%S")
