from __future__ import annotations

import queue

from hooks.raw_events import (
    RawKeyboardEvent,
    RawMouseEvent
)


class HookQueue:

    def __init__(
        self
    ) -> None:

        self._queue = (
            queue.SimpleQueue()
        )

    def push(
        self,
        event:
            RawKeyboardEvent
            |
            RawMouseEvent
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