from __future__ import annotations

import threading
import time

from playback.playback_state import (
    PlaybackState
)

from playback.high_precision_timer import (
    HighPrecisionTimer
)

from system.send_input import (
    SendInputAPI
)

from system.window_tracker import (
    WindowTracker
)

from core.exceptions import (
    PlaybackError
)


class PlaybackWorker:

    def __init__(
        self
    ) -> None:

        self._state = (
            PlaybackState()
        )

        self._thread = None

        self._packets = []

        self._repeat = False

        self._expected_window = None

    #
    # external api
    #

    def start(
        self,

        packets: list,

        repeat: bool,

        expected_window: str
    ) -> None:

        if self.running():

            raise PlaybackError(
                "Playback already running"
            )

        self._packets = packets

        self._repeat = repeat

        self._expected_window = (
            expected_window
        )

        #
        # reset state
        #

        self._state = (
            PlaybackState()
        )

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

        self._state.stop()

    def pause_resume(
        self
    ) -> None:

        self._state.pause_toggle()

    def running(
        self
    ) -> bool:

        if self._thread is None:

            return False

        return (
            self._thread.is_alive()
        )

    #
    # main worker
    #

    def _worker(
        self
    ) -> None:

        while True:

            #
            # immediate stop
            #

            if self._state.stopped():

                return

            #
            # active window check
            #

            if not self._validate_window():

                self.stop()

                return

            #
            # replay one sequence
            #

            self._play_sequence()

            #
            # no repeat
            #

            if not self._repeat:

                break

        self.stop()

    #
    # one replay cycle
    #

    def _play_sequence(
        self
    ) -> None:

        for packet in self._packets:

            #
            # stop check
            #

            if self._state.stopped():

                return

            #
            # pause check
            #

            self._pause_wait()

            #
            # window check
            #

            if not self._validate_window():

                self.stop()

                return

            #
            # replay packet
            #

            self._send_packet(
                packet
            )

    #
    # packet replay
    #

    def _send_packet(
        self,
        packet
    ) -> None:

        SendInputAPI.move_relative(

            packet.dx,

            packet.dy
        )

        HighPrecisionTimer.wait_ns(

            packet.dt_ns
        )

    #
    # pause logic
    #

    def _pause_wait(
        self
    ) -> None:

        while self._state.paused():

            if self._state.stopped():

                return

            time.sleep(
                0.005
            )

    #
    # target window validation
    #

    def _validate_window(
        self
    ) -> bool:

        if not self._expected_window:

            return True

        return WindowTracker.matches(

            self._expected_window
        )