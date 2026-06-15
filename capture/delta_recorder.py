from __future__ import annotations

from dataclasses import dataclass

from capture.timestamp import (
    HighPrecisionClock
)


@dataclass(
    frozen=True,
    slots=True
)
class MouseDelta:

    dx: int

    dy: int

    dt_ns: int


class DeltaRecorder:

    def __init__(
        self
    ) -> None:

        self._last_x = None
        self._last_y = None
        self._last_t = None

    def reset(
        self
    ) -> None:

        self._last_x = None
        self._last_y = None
        self._last_t = None

    def capture(
        self,
        x: int,
        y: int
    ) -> MouseDelta | None:

        now = (
            HighPrecisionClock.now_ns()
        )

        if self._last_t is None:

            self._last_x = x
            self._last_y = y
            self._last_t = now

            return None

        delta = MouseDelta(

            dx=x - self._last_x,

            dy=y - self._last_y,

            dt_ns=(
                now -
                self._last_t
            )
        )

        self._last_x = x
        self._last_y = y
        self._last_t = now

        return delta