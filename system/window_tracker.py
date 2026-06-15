from __future__ import annotations

import ctypes
from ctypes import wintypes


user32 = ctypes.windll.user32


class WindowTracker:

    @staticmethod
    def active_title() -> str:

        hwnd = (
            user32.GetForegroundWindow()
        )

        buffer = ctypes.create_unicode_buffer(
            512
        )

        user32.GetWindowTextW(

            hwnd,

            buffer,

            512
        )

        return buffer.value

    @staticmethod
    def matches(
        expected: str
    ) -> bool:

        return (
            WindowTracker.active_title()
            ==
            expected
        )