from __future__ import annotations

import ctypes
from ctypes import wintypes


user32 = ctypes.windll.user32


class POINT(ctypes.Structure):

    _fields_ = [

        ("x", wintypes.LONG),

        ("y", wintypes.LONG)
    ]


class MSG(ctypes.Structure):

    _fields_ = [

        ("hwnd", wintypes.HWND),

        ("message", wintypes.UINT),

        ("wParam", wintypes.WPARAM),

        ("lParam", wintypes.LPARAM),

        ("time", wintypes.DWORD),

        ("pt", POINT)
    ]


class MessageLoop:

    @staticmethod
    def run() -> None:

        msg = MSG()

        while user32.GetMessageW(

            ctypes.byref(msg),

            None,

            0,

            0

        ) != 0:

            user32.TranslateMessage(

                ctypes.byref(msg)
            )

            user32.DispatchMessageW(

                ctypes.byref(msg)
            )