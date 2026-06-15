from __future__ import annotations

import threading

from runtime.command_bus import (
    CommandBus
)

from runtime.commands import (
    CommandType
)

from capture.capture_worker import (
    CaptureWorker
)

from playback.playback_worker import (
    PlaybackWorker
)


class RuntimeController:

    def __init__(
        self,
        logger
    ) -> None:

        self.logger = logger

        self.bus = (
            CommandBus()
        )

        self.capture = (
            CaptureWorker()
        )

        self.playback = (
            PlaybackWorker()
        )

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

            cmd = (
                self.bus.receive()
            )

            if cmd is None:
                continue

            self._process(
                cmd
            )

    def _process(
        self,
        cmd
    ) -> None:

        if cmd.command == \
           CommandType.START_RECORD:

            self.capture.start()

            self.logger.info(
                "capture started"
            )

        elif cmd.command == \
             CommandType.STOP:

            self.capture.stop()

            self.playback.stop()

        elif cmd.command == \
             CommandType.PAUSE_RESUME:

            self.playback.pause_resume()

        elif cmd.command == \
             CommandType.RAW_MOUSE:

            self.capture.push(
                cmd.payload
            )

        elif cmd.command == \
             CommandType.RAW_KEYBOARD:

            self.capture.push(
                cmd.payload
            )