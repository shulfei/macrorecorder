from __future__ import annotations

import ctypes


user32 = ctypes.windll.user32


class MonitorInfo:

    @staticmethod
    def count() -> int:

        return user32.GetSystemMetrics(
            80
        )