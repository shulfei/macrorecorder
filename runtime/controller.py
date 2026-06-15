from __future__ import annotations

from serialization.preset_decoder import (
    PresetDecoder
)

from system.window_tracker import (
    WindowTracker
)

import threading
import time
from pathlib import Path

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

from serialization.preset_builder import (
    PresetBuilder
)

from serialization.preset_encoder import (
    PresetEncoder
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

        self._thread = None

    #
    # external api
    #

    def start(
        self
    ) -> None:

        self.running.set()

        self._thread = (
            threading.Thread(

                target=self._worker,

                daemon=True
            )
        )

        self._thread.start()

    def publish(
        self,
        command
    ) -> None:

        self.bus.send(
            command
        )

    #
    # internal loop
    #

    def _worker(
        self
    ) -> None:

        while self.running.is_set():

            cmd = (
                self.bus.receive()
            )

            if cmd is None:

                time.sleep(
                    0.001
                )

                continue

            self._process(
                cmd
            )

    #
    # command processor
    #

    def _process(
        self,
        cmd
    ) -> None:

        if cmd.command == \
           CommandType.START_RECORD:

            self._start_record()

        elif cmd.command == \
             CommandType.STOP_RECORD:

            self._stop_record()

        elif cmd.command == \
             CommandType.START_PLAYBACK:

            self._start_playback(
                cmd.payload
            )

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

        elif cmd.command == \
             CommandType.SHUTDOWN:

            self._shutdown()

    #
    # record start
    #

    def _start_record(
        self
    ) -> None:

        self.capture.start()

        self.logger.info(
            "Recording started"
        )

    #
    # record stop
    #

    def _stop_record(
        self
    ) -> None:

        self.capture.stop()

        packets = (
            self.capture.snapshot()
        )

        duration = (
            self.capture.duration_ns()
        )

        preset = PresetBuilder.build(

            packets=packets,

            duration_ns=duration,

            monitor_count=1,

            window_title=(

                WindowTracker.active_title()
            ),

            repeatable=False
        )

        filename = (

            f"preset_"

            f"{time.time_ns()}.json"
        )

        PresetEncoder().save(

            preset,

            Path(filename)
        )

        self.logger.info(

            f"Saved {filename}"
        )

    #
    # playback
    #

    def _start_playback(
            self,
            playback_command
    ) -> None:

        #
        # load preset
        #

        preset = (

            PresetDecoder()

            .load(

                playback_command.preset_path
            )
        )

        #
        # start playback
        #

        self.playback.start(

            packets=
            preset.packets,

            repeat=
            playback_command.repeat,

            expected_window=
            preset.window_title
        )

        self.logger.info(

            "Playback started"
        )

    #
    # shutdown
    #

    def _shutdown(
        self
    ) -> None:

        self.capture.stop()

        self.playback.stop()

        self.running.clear()

        self.logger.info(
            "Controller shutdown"
        )