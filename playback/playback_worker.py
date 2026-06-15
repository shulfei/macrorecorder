from __future__ import annotations

import threading
import time

from playback.playback_state import (
    PlaybackState
)

from playback.delta_player import (
    DeltaPlayer
)

from playback.repeat_loop import (
    RepeatLoop
)


class PlaybackWorker:

    def __init__(
        self
    ) -> None:

        self._state = (
            PlaybackState()
        )

        self._thread = None

    def start(
        self,
        packets: list,
        repeat: bool
    ) -> None:

        self._thread = (
            threading.Thread(

                target=self._worker,

                args=(
                    packets,
                    repeat
                ),

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

    def _worker(
        self,
        packets: list,
        repeat: bool
    ) -> None:

        repeater = (
            RepeatLoop(
                repeat
            )
        )

        while True:

            if self._state.stopped():
                return

            while self._state.paused():

                time.sleep(
                    0.01
                )

            DeltaPlayer.replay(
                packets
            )

            if not repeater.repeat():
                break