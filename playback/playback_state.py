from __future__ import annotations

import threading


class PlaybackState:

    def __init__(
        self
    ) -> None:

        self._paused = False
        self._stopped = False

        self._lock = (
            threading.Lock()
        )

    def stop(
        self
    ) -> None:

        with self._lock:
            self._stopped = True

    def pause_toggle(
        self
    ) -> None:

        with self._lock:

            self._paused = (
                not self._paused
            )

    def paused(
        self
    ) -> bool:

        with self._lock:
            return self._paused

    def stopped(
        self
    ) -> bool:

        with self._lock:
            return self._stopped