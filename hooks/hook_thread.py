from __future__ import annotations

import threading

from hooks.message_loop import (
    MessageLoop
)


class HookThread:

    def __init__(
        self,
        installer
    ) -> None:

        self._installer = (
            installer
        )

        self._thread = None

    def start(
        self
    ) -> None:

        self._thread = (
            threading.Thread(

                target=self._worker,

                daemon=True
            )
        )

        self._thread.start()

    def _worker(
        self
    ) -> None:

        self._installer()

        MessageLoop.run()