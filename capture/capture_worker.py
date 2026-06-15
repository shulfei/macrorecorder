from __future__ import annotations

import threading
import time

from capture.capture_queue import (
    CaptureQueue
)

from capture.delta_recorder import (
    DeltaRecorder
)

from capture.event_store import (
    EventStore
)

from hooks.raw_events import (
    RawMouseEvent
)

from capture.hotkey_filter import (
    ServiceHotkeyFilter
)


class CaptureWorker:

    def __init__(
        self
    ) -> None:

        self._queue = (
            CaptureQueue()
        )

        self._store = (
            EventStore()
        )

        self._delta = (
            DeltaRecorder()
        )

        self._filter = (
            ServiceHotkeyFilter()
        )

        self._running = (
            threading.Event()
        )

        self._thread = None

    def start(
        self
    ) -> None:

        self._delta.reset()

        self._running.set()

        self._thread = (
            threading.Thread(

                target=self._worker,

                daemon=True
            )
        )

        self._thread.start()

    def stop(
        self
    ) -> None:

        self._running.clear()

    def push(
        self,
        event
    ) -> None:

        self._queue.push(
            event
        )

    def snapshot(
        self
    ):

        return self._store.snapshot()

    def _worker(
        self
    ) -> None:

        while self._running.is_set():

            event = (
                self._queue.pop()
            )

            if event is None:

                time.sleep(
                    0.001
                )

                continue

            self._process(
                event
            )

    def _process(
        self,
        event
    ) -> None:

        if isinstance(
            event,
            RawMouseEvent
        ):

            delta = (
                self._delta.capture(

                    event.x,
                    event.y
                )
            )

            if delta:

                self._store.append(
                    delta
                )

            return

        # keyboard events
        # click events
        # pause timing
        # added next stage