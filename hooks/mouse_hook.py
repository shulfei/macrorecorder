from __future__ import annotations

import ctypes
from ctypes import wintypes

from hooks.raw_events import (
    RawMouseEvent
)

from hooks.hook_queue import (
    HookQueue
)


user32 = ctypes.windll.user32

WH_MOUSE_LL = 14

WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202


class POINT(
    ctypes.Structure
):
    _fields_ = [

        ("x",
         wintypes.LONG),

        ("y",
         wintypes.LONG)
    ]


class MSLLHOOKSTRUCT(
    ctypes.Structure
):
    _fields_ = [

        ("pt",
         POINT),

        ("mouseData",
         wintypes.DWORD),

        ("flags",
         wintypes.DWORD),

        ("time",
         wintypes.DWORD),

        ("dwExtraInfo",
         ctypes.c_ulonglong)
    ]


HOOKPROC = ctypes.WINFUNCTYPE(

    ctypes.c_long,

    ctypes.c_int,

    wintypes.WPARAM,

    wintypes.LPARAM
)


class MouseHook:

    def __init__(
        self,
        queue: HookQueue
    ) -> None:

        self._queue = queue

        self._handle = None

        self._proc = None

    def install(
        self
    ) -> None:

        kernel32 = (
            ctypes.windll.kernel32
        )

        self._proc = HOOKPROC(
            self._hook_proc
        )

        self._handle = (
            user32.SetWindowsHookExW(

                WH_MOUSE_LL,

                self._proc,

                kernel32.GetModuleHandleW(
                    None
                ),

                0
            )
        )

    def _hook_proc(
        self,
        n_code,
        w_param,
        l_param
    ):

        if n_code >= 0:

            ms = ctypes.cast(

                l_param,

                ctypes.POINTER(
                    MSLLHOOKSTRUCT
                )

            ).contents

            event = (
                RawMouseEvent(

                    x=ms.pt.x,

                    y=ms.pt.y,

                    event_type=
                        str(
                            w_param
                        ),

                    injected=False
                )
            )

            self._queue.push(
                event
            )

        return user32.CallNextHookEx(

            self._handle,

            n_code,

            w_param,

            l_param
        )