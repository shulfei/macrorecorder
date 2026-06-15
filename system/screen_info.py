from __future__ import annotations

import ctypes


user32 = ctypes.windll.user32


class ScreenInfo:

    @staticmethod
    def width() -> int:

        return user32.GetSystemMetrics(
            0
        )

    @staticmethod
    def height() -> int:

        return user32.GetSystemMetrics(
            1
        )