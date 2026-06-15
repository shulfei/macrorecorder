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

from capture.hotkey_filter import (
    ServiceHotkeyFilter
)

from capture.timestamp import (
    HighPrecisionClock
)

from hooks.raw_events import (
    RawMouseEvent,
    RawKeyboardEvent
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

        self._started_ns = None

    def start(
        self
    ) -> None:

        self._store.clear()

        self._delta.reset()

        self._started_ns = (
            HighPrecisionClock.now_ns()
        )

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
    ) -> list:

        return self._store.snapshot()

    def duration_ns(
        self
    ) -> int:

        if self._started_ns is None:

            return 0

        return (

            HighPrecisionClock.now_ns()

            -

            self._started_ns
        )

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

        #
        # ignore playback generated events
        #

        if event.injected:

            return

        #
        # mouse movement
        #

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

        #
        # keyboard
        #

        if isinstance(
            event,
            RawKeyboardEvent
        ):

            allowed = (
                self._filter.process(

                    event.vk_code,

                    event.pressed
                )
            )

            if not allowed:

                return

            #
            # keyboard event storage later
            #