"""Tests for story 4.6: cache move confirmation when corrected date changes."""

from __future__ import annotations

import os
from datetime import date, time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication

from thucthengay.editor.modes.review_edit_mode import ReviewEditMode
from thucthengay.models import (
    Composition,
    GridConfig,
    GridInterval,
    ImageLayer,
    MetadataSource,
    MetadataStatus,
    TargetConfig,
    TargetExportConfig,
    ViewState,
)
from thucthengay.workspace import WorkspaceError, WorkspaceService


def qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


def _target_config(target_id: str = "tgt") -> TargetConfig:
    return TargetConfig(
        id=target_id,
        sort_order=1,
        name=f"{target_id} Target",
        geojson_file=f"{target_id}.geojson",
        coordinate=[106.7, 10.8],
        scale=50000,
        grid=GridConfig(interval=GridInterval(minutes=1)),
        export=TargetExportConfig(template_metadata_file=f"{target_id}.template.json"),
        metadata={
            "template_metadata": {
                "template_pptx": f"{target_id}.pptx",
                "slide_index": 0,
                "map_frame": {"x": 0, "y": 0, "width": 640, "height": 360},
            }
        },
    )


def _layer(layer_id: str, *, capture_date: date | None = date(2026, 5, 25)) -> ImageLayer:
    return ImageLayer(
        layer_id=layer_id,
        source_path=f"{layer_id}.tif",
        order=0,
        capture_date=capture_date,
        capture_time=time(8, 0),
        cloud_percent=10.0,
        metadata_status=MetadataStatus.VALID,
        metadata_source=MetadataSource.FILENAME,
    )


def _composition(
    composition_id: str,
    target_id: str,
    capture_date: date,
    layers: list[ImageLayer],
    *,
    ready: bool = False,
    include: bool = False,
    review_order: int | None = None,
) -> Composition:
    return Composition(
        composition_id=composition_id,
        target_id=target_id,
        capture_date=capture_date,
        view=ViewState(center=[106.7, 10.8], scale=50000),
        needs_revalidation=False,
        ready=ready,
        include=include,
        review_order=review_order,
        layers=layers,
    )


# --- WorkspaceService.move_layer_between_compositions tests ---

class TestMoveLayerBetweenCompositions:
    def _bootstrap(self, tmp_path: Path) -> WorkspaceService:
        service = WorkspaceService(tmp_path / "workspace")
        service.initialize(config_path="config.json")
        return service

    def test_move_to_newly_created_destination(self, tmp_path: Path) -> None:
        service = self._bootstrap(tmp_path)
        source = _composition(
            "tgt__20260525",
            "tgt",
            date(2026, 5, 25),
            [_layer("L1"), _layer("L2")],
        )
        service.write_composition(source)

        updated_source, updated_dest = service.move_layer_between_compositions(
            "tgt__20260525",
            "L1",
            new_composition_id="tgt__20260601",
            new_target_id="tgt",
            new_capture_date=date(2026, 6, 1),
            capture_time=time(9, 0),
            cloud_percent=20.0,
            metadata_source=MetadataSource.MANUAL,
            metadata_status=MetadataStatus.VALID,
        )

        assert [layer.layer_id for layer in updated_source.layers] == ["L2"]
        assert [layer.layer_id for layer in updated_dest.layers] == ["L1"]
        assert updated_dest.layers[0].capture_date == date(2026, 6, 1)
        assert updated_dest.layers[0].capture_time == time(9, 0)
        assert updated_dest.layers[0].metadata_source == MetadataSource.MANUAL
        assert updated_dest.target_id == "tgt"
        assert updated_dest.capture_date == date(2026, 6, 1)

    def test_move_to_existing_destination_appends_layer(self, tmp_path: Path) -> None:
        service = self._bootstrap(tmp_path)
        source = _composition(
            "tgt__20260525", "tgt", date(2026, 5, 25), [_layer("L1")]
        )
        dest = _composition(
            "tgt__20260601", "tgt", date(2026, 6, 1), [_layer("X1", capture_date=date(2026, 6, 1))]
        )
        service.write_composition(source)
        service.write_composition(dest)

        _src, updated_dest = service.move_layer_between_compositions(
            "tgt__20260525",
            "L1",
            new_composition_id="tgt__20260601",
            new_target_id="tgt",
            new_capture_date=date(2026, 6, 1),
            capture_time=time(9, 0),
            cloud_percent=None,
            metadata_source=MetadataSource.MANUAL,
            metadata_status=MetadataStatus.VALID,
        )

        layer_ids = [layer.layer_id for layer in updated_dest.layers]
        assert "X1" in layer_ids and "L1" in layer_ids

    def test_both_compositions_marked_needs_revalidation(self, tmp_path: Path) -> None:
        service = self._bootstrap(tmp_path)
        source = _composition(
            "tgt__20260525",
            "tgt",
            date(2026, 5, 25),
            [_layer("L1"), _layer("L2")],
            ready=True,
            include=True,
            review_order=1,
        )
        service.write_composition(source)

        updated_source, updated_dest = service.move_layer_between_compositions(
            "tgt__20260525",
            "L1",
            new_composition_id="tgt__20260601",
            new_target_id="tgt",
            new_capture_date=date(2026, 6, 1),
            capture_time=time(9, 0),
            cloud_percent=None,
            metadata_source=MetadataSource.MANUAL,
            metadata_status=MetadataStatus.VALID,
        )

        assert updated_source.needs_revalidation is True
        assert updated_dest.needs_revalidation is True
        # ready/include not silently promoted
        assert updated_source.ready is False
        assert updated_source.include is False
        assert updated_dest.ready is False
        assert updated_dest.include is False

    def test_missing_layer_raises_workspace_error(self, tmp_path: Path) -> None:
        service = self._bootstrap(tmp_path)
        service.write_composition(
            _composition("tgt__20260525", "tgt", date(2026, 5, 25), [_layer("L1")])
        )

        with pytest.raises(WorkspaceError):
            service.move_layer_between_compositions(
                "tgt__20260525",
                "MISSING",
                new_composition_id="tgt__20260601",
                new_target_id="tgt",
                new_capture_date=date(2026, 6, 1),
                capture_time=None,
                cloud_percent=None,
                metadata_source=MetadataSource.MANUAL,
                metadata_status=MetadataStatus.NEEDS_MANUAL_CORRECTION,
            )

    def test_none_capture_date_raises_workspace_error(self, tmp_path: Path) -> None:
        service = self._bootstrap(tmp_path)
        service.write_composition(
            _composition("tgt__20260525", "tgt", date(2026, 5, 25), [_layer("L1")])
        )

        with pytest.raises(WorkspaceError):
            service.move_layer_between_compositions(
                "tgt__20260525",
                "L1",
                new_composition_id="tgt__20260601",
                new_target_id="tgt",
                new_capture_date=None,
                capture_time=None,
                cloud_percent=None,
                metadata_source=MetadataSource.MANUAL,
                metadata_status=MetadataStatus.NEEDS_MANUAL_CORRECTION,
            )


# --- ReviewEditMode date-change integration ---

class TestReviewEditModeDateChange:
    def _setup_mode(self, tmp_path: Path) -> tuple[ReviewEditMode, WorkspaceService]:
        qapp()
        service = WorkspaceService(tmp_path / "workspace")
        service.initialize(config_path="config.json")
        source = _composition(
            "tgt__20260525",
            "tgt",
            date(2026, 5, 25),
            [_layer("L1")],
        )
        service.write_composition(source)
        mode = ReviewEditMode()
        mode.load_workspace(service, targets=[_target_config("tgt")])
        target_index = mode.tree_model.index(0, 0)
        comp_index = mode.tree_model.index(0, 0, target_index)
        mode.tree_view.setCurrentIndex(comp_index)
        return mode, service

    def test_same_date_uses_update_layer_metadata(self, tmp_path: Path) -> None:
        mode, service = self._setup_mode(tmp_path)
        mode._confirm_date_change = lambda *args, **kwargs: True  # would be ignored

        payload = {
            "capture_date": date(2026, 5, 25),  # same as composition's date
            "capture_time": time(11, 0),
            "cloud_percent": 22.0,
            "metadata_source": MetadataSource.MANUAL,
            "metadata_status": MetadataStatus.VALID,
        }
        mode._apply_layer_metadata("L1", payload)

        # Should still be in same composition with new time
        comp = service.read_composition("tgt__20260525")
        assert comp.layers[0].capture_time == time(11, 0)
        assert comp.layers[0].cloud_percent == 22.0
        # Destination should not exist
        with pytest.raises(WorkspaceError):
            service.read_composition("tgt__20260601")

    def test_different_date_with_confirm_moves_layer(self, tmp_path: Path) -> None:
        mode, service = self._setup_mode(tmp_path)
        mode._confirm_date_change = lambda *args, **kwargs: True  # accept

        payload = {
            "capture_date": date(2026, 6, 1),
            "capture_time": time(9, 0),
            "cloud_percent": None,
            "metadata_source": MetadataSource.MANUAL,
            "metadata_status": MetadataStatus.VALID,
        }
        mode._apply_layer_metadata("L1", payload)

        source = service.read_composition("tgt__20260525")
        dest = service.read_composition("tgt__20260601")
        assert source.layers == []
        assert len(dest.layers) == 1
        assert dest.layers[0].layer_id == "L1"
        assert dest.layers[0].capture_date == date(2026, 6, 1)

    def test_different_date_with_cancel_makes_no_changes(self, tmp_path: Path) -> None:
        mode, service = self._setup_mode(tmp_path)
        mode._confirm_date_change = lambda *args, **kwargs: False  # cancel

        payload = {
            "capture_date": date(2026, 6, 1),
            "capture_time": time(9, 0),
            "cloud_percent": None,
            "metadata_source": MetadataSource.MANUAL,
            "metadata_status": MetadataStatus.VALID,
        }
        mode._apply_layer_metadata("L1", payload)

        source = service.read_composition("tgt__20260525")
        # No changes: layer still in source, original metadata
        assert len(source.layers) == 1
        assert source.layers[0].capture_date == date(2026, 5, 25)
        assert source.layers[0].capture_time == time(8, 0)
        # Destination should not exist
        with pytest.raises(WorkspaceError):
            service.read_composition("tgt__20260601")
        assert "hủy" in mode.action_summary.text().lower()

    def test_cleared_date_falls_through_to_update_layer_metadata(self, tmp_path: Path) -> None:
        mode, service = self._setup_mode(tmp_path)

        # Track if confirm was called (it shouldn't be)
        confirm_calls = []
        mode._confirm_date_change = lambda *args, **kwargs: (
            confirm_calls.append(args) or True
        )

        payload = {
            "capture_date": None,  # cleared
            "capture_time": None,
            "cloud_percent": None,
            "metadata_source": MetadataSource.MANUAL,
            "metadata_status": MetadataStatus.NEEDS_MANUAL_CORRECTION,
        }
        mode._apply_layer_metadata("L1", payload)

        assert confirm_calls == []
        source = service.read_composition("tgt__20260525")
        assert source.layers[0].capture_date is None
