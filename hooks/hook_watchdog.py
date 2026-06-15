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

    def stop(
        self
    ) -> None:

        self.running.clear()

    def _worker(
        self
    ) -> None:

        while self.running.is_set():

            #
            # monitor only
            #

            keyboard_alive = (
                self.keyboard.alive()
            )

            mouse_alive = (
                self.mouse.alive()
            )

            #
            # later:
            # logging / diagnostics
            #

            if not keyboard_alive:

                print(
                    "Warning: keyboard hook inactive"
                )

            if not mouse_alive:

                print(
                    "Warning: mouse hook inactive"
                )

            time.sleep(
                1
            )