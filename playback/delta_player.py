from __future__ import annotations

from system.send_input import (
    SendInputAPI
)

from playback.high_precision_timer import (
    HighPrecisionTimer
)


class DeltaPlayer:

    @staticmethod
    def replay(
        packets: list
    ) -> None:

        for packet in packets:

            SendInputAPI.move_relative(

                packet.dx,

                packet.dy
            )

            HighPrecisionTimer.wait_ns(

                packet.dt_ns
            )