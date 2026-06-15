from __future__ import annotations

import ctypes


user32 = ctypes.windll.user32


class DPIContext:

    @staticmethod
    def enable() -> None:

        user32.SetProcessDPIAware()