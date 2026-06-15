from __future__ import annotations

import queue


class CaptureQueue:

    def __init__(
        self
    ) -> None:

        self._queue = (
            queue.SimpleQueue()
        )

    def push(
        self,
        event
    ) -> None:

        self._queue.put(
            event
        )

    def pop(
        self
    ):

        try:
            return self._queue.get_nowait()

        except Exception:
            return None