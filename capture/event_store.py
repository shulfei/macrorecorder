from __future__ import annotations

import threading


class EventStore:

    def __init__(
        self
    ) -> None:

        self._events = []

        self._lock = (
            threading.Lock()
        )

    def append(
        self,
        event
    ) -> None:

        with self._lock:

            self._events.append(
                event
            )

    def snapshot(
        self
    ) -> list:

        with self._lock:

            return list(
                self._events
            )

    def clear(
        self
    ) -> None:

        with self._lock:

            self._events.clear()