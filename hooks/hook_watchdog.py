from __future__ import annotations

import threading
import time


class HookWatchdog:

    def __init__(
        self,
        keyboard_hook,
        mouse_hook
    ) -> None:

        self.keyboard = keyboard_hook

        self.mouse = mouse_hook

        self.running = (
            threading.Event()
        )

    def start(
        self
    ) -> None:

        self.running.set()

        threading.Thread(

            target=self._worker,

            daemon=True

        ).start()

    def _worker(
        self
    ) -> None:

        while self.running.is_set():

            if not self.keyboard.alive():

                self.keyboard.install()

            if not self.mouse.alive():

                self.mouse.install()

            time.sleep(1)