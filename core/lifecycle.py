from __future__ import annotations

import signal
import threading


class ApplicationLifecycle:

    def __init__(
        self,
        app
    ) -> None:

        self.app = app

        self.shutdown = (
            threading.Event()
        )

        signal.signal(

            signal.SIGINT,

            self._signal
        )

    def _signal(
        self,
        *_args
    ) -> None:

        self.shutdown.set()

    def run(
        self
    ) -> None:

        self.app.start()

        self.shutdown.wait()