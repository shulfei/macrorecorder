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

        self._loop = (
            MessageLoop()
        )

    def start(
        self
    ) -> None:

        self._loop.start(

            install_hooks=
                self._installer
        )

    def stop(
        self
    ) -> None:

        self._loop.stop()