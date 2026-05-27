"""Slide preview panel for Review/Edit mode."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from thucthengay.jobs import JobState, PreviewRenderJobResult, PreviewRenderPlan
from thucthengay.models import Composition, GridConfig, ImageLayer


class SlidePreviewState(StrEnum):
    """Display states for the slide preview panel."""

    EMPTY = "empty"
    NEEDS_UPDATE = "needs_update"
    LOADING = "loading"
    RENDERED = "rendered"
    RENDER_ERROR = "render_error"
    NO_VISIBLE_LAYER = "no_visible_layer"


@dataclass(frozen=True)
class PreviewRequestToken:
    """Generation token used to ignore stale debounced preview completions."""

    generation: int
    composition_id: str | None
    signature: tuple[Any, ...]


class SlidePreviewWidget(QWidget):
    """Debounced deterministic preview projection for the selected composition."""

    DEFAULT_DEBOUNCE_MS = 120

    def __init__(self, parent: QWidget | None = None, *, debounce_ms: int | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("reviewSlidePreview")
        self.setMinimumHeight(132)
        self._debounce_ms = max(
            0, self.DEFAULT_DEBOUNCE_MS if debounce_ms is None else debounce_ms
        )
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._complete_scheduled_preview)
        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self._apply_pending_render)
        self._generation = 0
        self._composition: Composition | None = None
        self._effective_grid: GridConfig | None = None
        self._background: dict[str, Any] = {}
        self._state = SlidePreviewState.EMPTY
        self._last_token: PreviewRequestToken | None = None
        self._pending_render: tuple[PreviewRequestToken, str] | None = None
        self._preview_job_revision: int | None = None
        self._preview_job_ids: set[str] = set()
        self._preview_job_applied_quality_rank = -1

        self.status_label = QLabel("Chưa chọn composition.")
        self.status_label.setObjectName("reviewPreviewSummary")
        self.status_label.setWordWrap(True)
        self.detail_label = QLabel("")
        self.detail_label.setObjectName("reviewPreviewDetails")
        self.detail_label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.status_label)
        layout.addWidget(self.detail_label, 1)

    @property
    def generation(self) -> int:
        return self._generation

    def state(self) -> SlidePreviewState:
        return self._state

    def state_text(self) -> str:
        return self.status_label.text()

    def detail_text(self) -> str:
        return self.detail_label.text()

    def set_composition(
        self,
        composition: Composition | None,
        *,
        effective_grid: GridConfig | None = None,
        background: dict[str, Any] | None = None,
    ) -> None:
        """Load a composition and debounce a preview update for its current state."""
        self._composition = composition
        self._effective_grid = effective_grid
        self._background = dict(background or {})
        self._bump_generation()
        self._timer.stop()
        self._render_timer.stop()
        self._pending_render = None
        self._clear_preview_job_tracking()

        if composition is None:
            self._state = SlidePreviewState.EMPTY
            self._last_token = None
            self.status_label.setText("Chưa chọn composition.")
            self.detail_label.setText("")
            return

        if not _visible_layers(composition):
            self._state = SlidePreviewState.NO_VISIBLE_LAYER
            self._last_token = None
            self.status_label.setText("Không có layer đang bật để tạo slide preview.")
            self.detail_label.setText("Bật ít nhất một layer trước khi cập nhật preview.")
            return

        self._state = SlidePreviewState.NEEDS_UPDATE
        self.status_label.setText("Preview cần cập nhật. Đang chờ debounce...")
        self.detail_label.setText(self._preview_text(composition))
        self._last_token = self.begin_preview_request()
        self._timer.start(self._debounce_ms)

    def track_preview_plan(self, plan: PreviewRenderPlan) -> None:
        """Track the current two-stage preview plan for stale job-result filtering."""
        if self._composition is None:
            return
        self._preview_job_revision = plan.interactive.revision
        self._preview_job_ids = {plan.interactive.job_id, plan.settled.job_id}
        self._preview_job_applied_quality_rank = -1
        self._state = SlidePreviewState.LOADING
        self.status_label.setText("Đang cập nhật preview hai tầng...")

    def apply_preview_job_result(self, result: PreviewRenderJobResult) -> bool:
        """Apply only current-revision preview job results to the widget."""
        if not self._matches_preview_job(result):
            return False
        if result.state == JobState.ERROR:
            self.set_render_error(result.message)
            return True
        if result.state not in {JobState.SUCCESS, JobState.WARNING}:
            return False
        quality_rank = _preview_quality_rank(result)
        if quality_rank < self._preview_job_applied_quality_rank:
            return False
        self._preview_job_applied_quality_rank = quality_rank

        self._state = SlidePreviewState.RENDERED
        self.status_label.setText("Preview đã cập nhật.")
        issue_text = f"; issues: {len(result.issues)}" if result.issues else ""
        self.detail_label.setText(
            f"{result.quality.value} {result.output_width}x{result.output_height}{issue_text}"
        )
        return True

    def begin_preview_request(self) -> PreviewRequestToken:
        """Capture the current preview generation and render-affecting signature."""
        return PreviewRequestToken(
            generation=self._generation,
            composition_id=(
                None if self._composition is None else self._composition.composition_id
            ),
            signature=self._signature(),
        )

    def apply_preview_result(self, token: PreviewRequestToken, rendered_text: str) -> bool:
        """Apply a preview result only if it still matches the latest request."""
        if token != self.begin_preview_request():
            return False
        self._state = SlidePreviewState.RENDERED
        self.status_label.setText("Preview đã cập nhật.")
        self.detail_label.setText(rendered_text)
        return True

    def set_render_error(self, message: str) -> None:
        """Show a recoverable render error for the current preview request."""
        self._bump_generation()
        self._timer.stop()
        self._render_timer.stop()
        self._pending_render = None
        self._last_token = None
        self._clear_preview_job_tracking()
        self._state = SlidePreviewState.RENDER_ERROR
        self.status_label.setText("Preview lỗi render.")
        self.detail_label.setText(
            f"{message.strip() or 'Không tạo được preview.'} "
            "Có thể tiếp tục chỉnh sửa rồi cập nhật lại preview."
        )

    def _complete_scheduled_preview(self) -> None:
        if self._composition is None or self._last_token is None:
            return
        self._state = SlidePreviewState.LOADING
        self.status_label.setText("Đang cập nhật preview...")
        self._pending_render = (self._last_token, self._preview_text(self._composition))
        self._render_timer.start(0)

    def _apply_pending_render(self) -> None:
        if self._pending_render is None:
            return
        token, rendered_text = self._pending_render
        self._pending_render = None
        self.apply_preview_result(token, rendered_text)

    def _signature(self) -> tuple[Any, ...]:
        composition = self._composition
        if composition is None:
            return ()
        grid = self._effective_grid or composition.grid_override
        grid_signature: tuple[Any, ...] = ()
        if grid is not None:
            grid_signature = (
                grid.interval.degrees,
                grid.interval.minutes,
                grid.interval.seconds,
                grid.label_format,
                tuple(sorted(grid.style.items())),
            )
        return (
            tuple(composition.view.center),
            composition.view.scale,
            composition.view.rotation,
            tuple((layer.layer_id, layer.order, layer.visible) for layer in composition.layers),
            grid_signature,
            _metadata_signature(self._background),
        )

    def _preview_text(self, composition: Composition) -> str:
        layers = _visible_layers(composition)
        layer_text = ", ".join(layer.layer_id for layer in layers)
        grid = self._effective_grid or composition.grid_override
        if grid is None:
            grid_text = "Grid: chưa có cấu hình"
        else:
            seconds = _format_number(grid.interval.seconds)
            grid_text = (
                "Grid: "
                f"{grid.interval.degrees}d {grid.interval.minutes}m {seconds}s, "
                f"label {grid.label_format or 'dms_full'}"
            )
        background_text = _background_text(self._background)
        return (
            f"Composition: {composition.composition_id}\n"
            f"Center: {composition.view.center[0]:.6f}, {composition.view.center[1]:.6f}; "
            f"Scale 1:{composition.view.scale:,}; Rotation {composition.view.rotation}\n"
            f"Layers: {layer_text}\n"
            f"{grid_text}\n"
            f"{background_text}"
        )

    def _bump_generation(self) -> None:
        self._generation += 1

    def _clear_preview_job_tracking(self) -> None:
        self._preview_job_revision = None
        self._preview_job_ids = set()
        self._preview_job_applied_quality_rank = -1

    def _matches_preview_job(self, result: PreviewRenderJobResult) -> bool:
        if self._composition is None:
            return False
        return (
            result.composition_id == self._composition.composition_id
            and result.revision == self._preview_job_revision
            and result.job_id in self._preview_job_ids
        )


def _preview_quality_rank(result: PreviewRenderJobResult) -> int:
    if result.quality.value == "settled_high_res":
        return 1
    return 0


def _visible_layers(composition: Composition) -> list[ImageLayer]:
    return sorted(
        (layer for layer in composition.layers if layer.visible),
        key=lambda layer: (layer.order, layer.layer_id),
    )


def _background_text(background: dict[str, Any]) -> str:
    if not background:
        return "Background: mặc định preview"
    color = background.get("color") or background.get("background") or background.get("fill")
    if isinstance(color, str) and color.strip():
        return f"Background: {color.strip()}"
    return "Background: metadata target"


def _metadata_signature(metadata: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted((str(key), repr(value)) for key, value in metadata.items()))


def _format_number(value: float | int) -> str:
    numeric = float(value)
    if isfinite(numeric) and numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:g}"
