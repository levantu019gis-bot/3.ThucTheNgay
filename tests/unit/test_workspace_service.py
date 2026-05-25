from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from thucthengay.models import (
    Composition,
    PersistedValidationState,
    ValidationSummary,
    ViewState,
)
from thucthengay.workspace.atomic_write import atomic_write_json
from thucthengay.workspace.service import WorkspaceClearNotConfirmedError, WorkspaceService


def valid_composition(composition_id: str = "target_001__20260525") -> Composition:
    return Composition(
        composition_id=composition_id,
        target_id="target_001",
        capture_date=date(2026, 5, 25),
        view=ViewState(center=[106.7, 10.8], scale=50000),
    )


def test_initialize_creates_manifest_and_known_subfolders(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")

    manifest = service.initialize(config_path="config.json", imagery_input_path="imagery")

    assert service.paths.manifest.is_file()
    assert service.paths.cache.is_dir()
    assert service.paths.compositions.is_dir()
    assert service.paths.renders.is_dir()
    assert service.paths.exports.is_dir()
    assert manifest.config_path == "config.json"
    assert manifest.imagery_input_path == "imagery"


def test_reopen_recreates_missing_known_folders_without_changing_compositions(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())
    service.paths.renders.rmdir()

    reopened = WorkspaceService(tmp_path / "workspace")
    manifest = reopened.load_manifest()

    assert reopened.paths.renders.is_dir()
    assert manifest.composition_ids == ["target_001__20260525"]
    assert reopened.read_composition("target_001__20260525").target_id == "target_001"


def test_write_composition_is_atomic_and_registers_manifest_id(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")

    composition_path = service.write_composition(valid_composition())

    manifest = service.load_manifest()
    assert composition_path == service.paths.composition_file("target_001__20260525")
    assert manifest.composition_ids == ["target_001__20260525"]
    assert service.read_composition("target_001__20260525").capture_date == date(2026, 5, 25)


def test_atomic_write_failure_keeps_existing_final_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    final_path = tmp_path / "manifest.json"
    final_path.write_text('{"stable": true}\n', encoding="utf-8")

    def fail_replace(_source: str, _destination: Path) -> None:
        raise OSError("replace failed")

    monkeypatch.setattr("thucthengay.workspace.atomic_write.os.replace", fail_replace)

    with pytest.raises(OSError):
        atomic_write_json(final_path, {"stable": False})

    assert final_path.read_text(encoding="utf-8") == '{"stable": true}\n'
    assert not list(tmp_path.glob(".manifest.json.*.tmp"))


def test_clear_app_owned_data_requires_confirmation_and_resets_manifest(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())
    (service.paths.cache / "image.tif").write_text("cache", encoding="utf-8")
    (service.paths.renders / "preview.png").write_text("render", encoding="utf-8")

    assert service.has_app_owned_data()
    with pytest.raises(WorkspaceClearNotConfirmedError):
        service.clear_app_owned_data()

    assert service.read_composition("target_001__20260525").target_id == "target_001"

    service.clear_app_owned_data(confirmed=True)

    assert service.load_manifest().composition_ids == []
    assert service.paths.cache.is_dir()
    assert service.paths.compositions.is_dir()
    assert not any(service.paths.cache.iterdir())
    assert not any(service.paths.compositions.iterdir())


def test_composition_id_cannot_escape_workspace(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")

    with pytest.raises(ValueError):
        service.write_composition(valid_composition("../escape"))


def test_update_review_state_persists_status_and_notes_after_reload(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())

    service.update_review_state(
        "target_001__20260525",
        reviewed=True,
        ready=True,
        include=True,
        review_order=7,
        notes="Đã kiểm tra.",
    )

    reloaded = WorkspaceService(tmp_path / "workspace").read_composition("target_001__20260525")
    assert reloaded.reviewed is True
    assert reloaded.ready is True
    assert reloaded.include is True
    assert reloaded.review_order == 7
    assert reloaded.notes == "Đã kiểm tra."


def test_update_review_state_validates_review_order(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())

    with pytest.raises(ValidationError):
        service.update_review_state("target_001__20260525", review_order=0)


def test_include_transition_requires_passing_validation_gate(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())

    with pytest.raises(Exception, match="passing validation"):
        service.apply_include_transition("target_001__20260525", validation_passed=False)

    unchanged = service.read_composition("target_001__20260525")
    assert unchanged.reviewed is False
    assert unchanged.ready is False
    assert unchanged.include is False
    assert unchanged.review_order is None


def test_include_transition_marks_ready_include_and_assigns_review_order(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition("target_001__20260525"))
    service.write_composition(valid_composition("target_002__20260526"))

    first = service.apply_include_transition("target_001__20260525", validation_passed=True)
    second = service.apply_include_transition("target_002__20260526", validation_passed=True)

    assert first.reviewed is True
    assert first.ready is True
    assert first.include is True
    assert first.review_order == 1
    assert second.review_order == 2


def test_skip_transition_marks_reviewed_not_included_and_clears_review_order(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())
    service.apply_include_transition("target_001__20260525", validation_passed=True)

    skipped = service.apply_skip_transition("target_001__20260525")

    assert skipped.reviewed is True
    assert skipped.ready is False
    assert skipped.include is False
    assert skipped.review_order is None


def test_previous_and_next_navigation_do_not_mutate_current_composition(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition("target_001__20260525"))
    service.write_composition(valid_composition("target_002__20260526"))

    before = service.read_composition("target_002__20260526").model_dump()

    assert service.previous_composition_id("target_002__20260526") == "target_001__20260525"
    assert service.next_composition_id("target_001__20260525") == "target_002__20260526"
    assert service.previous_composition_id("target_001__20260525") is None
    assert service.read_composition("target_002__20260526").model_dump() == before


def test_save_validation_summary_persists_only_compact_summary(tmp_path: Path) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())

    summary = ValidationSummary(
        last_validated_at=datetime(2026, 5, 25, 8, 30, tzinfo=UTC),
        info_count=2,
        warning_count=1,
        error_count=0,
    )
    service.save_validation_summary("target_001__20260525", summary)

    raw = json.loads(
        service.paths.composition_file("target_001__20260525").read_text(encoding="utf-8")
    )
    assert raw["validation_summary"]["warning_count"] == 1
    assert raw["needs_revalidation"] is False
    assert "issues" not in raw
    assert "detailed_issues" not in raw


def test_mark_needs_revalidation_makes_prior_summary_stale_and_unincludes(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())
    service.save_validation_summary(
        "target_001__20260525",
        ValidationSummary(warning_count=1),
    )
    service.apply_include_transition("target_001__20260525", validation_passed=True)

    stale = service.mark_needs_revalidation("target_001__20260525")

    assert stale.needs_revalidation is True
    assert stale.ready is False
    assert stale.include is False
    assert stale.review_order is None
    assert stale.validation_summary.warning_count == 1
    assert stale.persisted_validation_state == PersistedValidationState.STALE


def test_reloaded_validation_summary_provides_aggregate_counts_and_state(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition())
    service.save_validation_summary(
        "target_001__20260525",
        ValidationSummary(info_count=1, warning_count=2, error_count=0),
    )

    reloaded = WorkspaceService(tmp_path / "workspace").read_composition("target_001__20260525")

    assert reloaded.validation_summary.info_count == 1
    assert reloaded.validation_summary.warning_count == 2
    assert reloaded.validation_summary.error_count == 0
    assert reloaded.persisted_validation_state == PersistedValidationState.WARNING


def test_included_export_candidates_refuse_stale_or_errored_persisted_state(
    tmp_path: Path,
) -> None:
    service = WorkspaceService(tmp_path / "workspace")
    service.initialize(config_path="config.json")
    service.write_composition(valid_composition("clean"))
    service.write_composition(valid_composition("stale"))
    service.write_composition(valid_composition("errored"))

    service.save_validation_summary("clean", ValidationSummary())
    service.apply_include_transition("clean", validation_passed=True)

    service.save_validation_summary("stale", ValidationSummary())
    service.apply_include_transition("stale", validation_passed=True)
    service.mark_needs_revalidation("stale")

    service.save_validation_summary("errored", ValidationSummary(error_count=1))
    service.update_review_state("errored", reviewed=True, ready=True, include=True, review_order=3)

    assert [composition.composition_id for composition in service.included_export_candidates()] == [
        "clean"
    ]
