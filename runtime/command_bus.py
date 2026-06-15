from __future__ import annotations

from queue import SimpleQueue


class CommandBus:

    def __init__(
        self
    ) -> None:

        self._queue = (
            SimpleQueue()
        )

    def send(
        self,
        command
    ) -> None:

        self._queue.put(
            command
        )

    def receive(
        self
    ):

        if self._queue.empty():

            return None

        return self._queue.get()