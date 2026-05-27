"""Cooperative control primitives for long-running jobs."""

from __future__ import annotations

from threading import Condition


class JobCancelled(Exception):
    """Raised when a cooperative job observes a cancellation request."""


class JobControl:
    """Thread-safe pause/resume/cancel control for background jobs."""

    def __init__(self) -> None:
        self._condition = Condition()
        self._pause_requested = False
        self._cancel_requested = False

    @property
    def pause_requested(self) -> bool:
        """Return true when the job should pause at its next checkpoint."""
        with self._condition:
            return self._pause_requested

    @property
    def cancel_requested(self) -> bool:
        """Return true when the job should stop at its next checkpoint."""
        with self._condition:
            return self._cancel_requested

    def request_pause(self) -> None:
        """Ask the job to pause at the next cooperative checkpoint."""
        with self._condition:
            if not self._cancel_requested:
                self._pause_requested = True

    def resume(self) -> None:
        """Resume a paused job."""
        with self._condition:
            self._pause_requested = False
            self._condition.notify_all()

    def request_cancel(self) -> None:
        """Ask the job to stop and wake it if it is paused."""
        with self._condition:
            self._cancel_requested = True
            self._pause_requested = False
            self._condition.notify_all()

    def checkpoint(self) -> None:
        """Block while paused and raise if cancellation was requested."""
        with self._condition:
            while self._pause_requested and not self._cancel_requested:
                self._condition.wait(timeout=0.2)
            if self._cancel_requested:
                raise JobCancelled
