from __future__ import annotations

import threading
import time

from hooks.raw_events import (
    RawKeyboardEvent,
    RawMouseEvent
)

from runtime.commands import (
    RuntimeCommand,
    CommandType
)


class HookDispatcher:

    def __init__(
        self,
        hook_queue,
        controller
    ) -> None:

        self._queue = (
            hook_queue
        )

        self._controller = (
            controller
        )

        self._running = (
            threading.Event()
        )

        self._thread = None

    def start(
        self
    ) -> None:

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

            self._dispatch(
                event
            )

    def _dispatch(
        self,
        event
    ) -> None:

        if isinstance(

            event,

            RawKeyboardEvent
        ):

            self._controller.publish(

                RuntimeCommand(

                    CommandType.RAW_KEYBOARD,

                    event
                )
            )

        elif isinstance(

            event,

            RawMouseEvent
        ):

            self._controller.publish(

                RuntimeCommand(

                    CommandType.RAW_MOUSE,

                    event
                )
            )