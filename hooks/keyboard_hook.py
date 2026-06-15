from __future__ import annotations

import ctypes
from ctypes import wintypes

from hooks.raw_events import (
    RawKeyboardEvent
)

from hooks.hook_queue import (
    HookQueue
)


user32 = ctypes.windll.user32

WH_KEYBOARD_LL = 13

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101


class KBDLLHOOKSTRUCT(
    ctypes.Structure
):
    _fields_ = [

        ("vkCode",
         wintypes.DWORD),

        ("scanCode",
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


class KeyboardHook:

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

                WH_KEYBOARD_LL,

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

            kb = ctypes.cast(

                l_param,

                ctypes.POINTER(
                    KBDLLHOOKSTRUCT
                )

            ).contents

            event = (
                RawKeyboardEvent(

                    vk_code=
                        kb.vkCode,

                    scan_code=
                        kb.scanCode,

                    pressed=(
                        w_param ==
                        WM_KEYDOWN
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