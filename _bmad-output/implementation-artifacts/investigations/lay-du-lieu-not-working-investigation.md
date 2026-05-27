# Investigation: Chuc nang Lay du lieu khong hoat dong

## Hand-off Brief

1. **What happened.** Confirmed: Setup mode emitted `ingestRequested`, but AppShell did not connect that signal to any runtime ingestion handler before this fix.
2. **Where the case stands.** Concluded: `AppShell` now runs config loading, ingestion, summary display, and workspace handoff to Review/Edit and Export.
3. **What's needed next.** Run a manual UI pass with the real imagery folder to validate end-to-end data volume and operator feedback.

## Case Info

| Field | Value |
| --- | --- |
| Ticket | N/A |
| Date opened | 2026-05-26 |
| Status | Concluded |
| System | Windows, conda env `ttn-env` |
| Evidence sources | Source code, focused regression test, config load check |

## Problem Statement

User reported: chuc nang "lay du lieu" hien khong hoat dong.

## Evidence Inventory

| Source | Status | Notes |
| --- | --- | --- |
| `src/thucthengay/editor/modes/setup_mode.py` | Available | Button click emits `ingestRequested` after path validation. |
| `src/thucthengay/editor/app_shell.py` | Available | Confirmed missing connection before fix; fixed at lines 33 and 39-64. |
| `src/thucthengay/jobs/ingestion_job.py` | Available | Ingestion job implementation existed and was already covered by unit tests. |
| `config.json` | Available | Config load check after investigation: `ok=True`, 70 enabled targets, 0 issues. |

## Confirmed Findings

### Finding 1: Setup emitted a signal but runtime shell did not consume it

**Evidence:** `src/thucthengay/editor/modes/setup_mode.py` emits `ingestRequested`; prior AppShell only connected export jump handling and had no ingestion handler.

**Detail:** Clicking the enabled button could emit a signal without running `run_ingestion_job`, so the UI appeared to do nothing.

### Finding 2: Regression test now covers the runtime handoff

**Evidence:** `tests/unit/test_setup_mode.py:137`

**Detail:** The new test verifies AppShell handles Setup's request by loading config, running ingestion, showing summary, loading Review/Edit and Export workspaces, and switching to Review/Edit.

## Source Code Trace

| Element | Detail |
| --- | --- |
| Error origin | Missing connection in `AppShell.__init__` before fix |
| Trigger | User clicks Setup mode `Lay du lieu` button |
| Condition | Paths are valid, signal emits, no connected slot existed |
| Related files | `src/thucthengay/editor/app_shell.py`, `src/thucthengay/editor/modes/setup_mode.py`, `src/thucthengay/jobs/ingestion_job.py` |

## Conclusion

**Confidence:** High

Root cause was a missing AppShell integration point, not a broken ingestion pipeline. The ingestion pipeline and config loader were present; the UI shell simply did not call them when Setup emitted the request.

## Recommended Next Steps

### Fix direction

Implemented in `src/thucthengay/editor/app_shell.py`: connect `setup_mode.ingestRequested` to `_run_ingestion`, then hand successful results to Review/Edit and Export.

### Diagnostic

Run the desktop app, select `config.json`, a real imagery folder, and a workspace, then click `Lay du lieu`. Expected: summary counters update and the UI switches to Review/Edit when ingestion succeeds or completes with warnings.

## Reproduction Plan

1. Open app.
2. Select valid config, imagery folder, and workspace.
3. Click `Lay du lieu`.
4. Before fix: no ingestion job was invoked.
5. After fix: summary is shown and downstream modes receive the workspace.
