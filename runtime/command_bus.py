from __future__ import annotations

import queue

from runtime.commands import (
    RuntimeCommand
)


class CommandBus:

    def __init__(
        self
    ) -> None:

        self._queue = (
            queue.Queue[
                RuntimeCommand
            ]()
        )

    def publish(
        self,
        command: RuntimeCommand
    ) -> None:

        self._queue.put(
            command
        )

    def receive(
        self,
        timeout: float = 0.05
    ) -> RuntimeCommand | None:

        try:

            return self._queue.get(
                timeout=timeout
            )

        except queue.Empty:

            return None