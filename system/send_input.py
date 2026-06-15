from __future__ import annotations

import ctypes


user32 = ctypes.windll.user32


class SendInputAPI:

    @staticmethod
    def move_relative(
        dx: int,
        dy: int
    ) -> None:

        user32.mouse_event(

            0x0001,

            dx,

            dy,

            0,

            0
        )