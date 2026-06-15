from __future__ import annotations

import ctypes

from ctypes import wintypes

from hooks.raw_events import (
    RawKeyboardEvent
)

from hooks.hook_queue import (
    HookQueue
)

from core.exceptions import (
    HookInstallError
)


user32 = ctypes.windll.user32

kernel32 = ctypes.windll.kernel32


WH_KEYBOARD_LL = 13

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

LLKHF_INJECTED = 0x10


class KBDLLHOOKSTRUCT(
    ctypes.Structure
):

    _fields_ = [

        (
            "vkCode",
            wintypes.DWORD
        ),

        (
            "scanCode",
            wintypes.DWORD
        ),

        (
            "flags",
            wintypes.DWORD
        ),

        (
            "time",
            wintypes.DWORD
        ),

        (
            "dwExtraInfo",
            ctypes.c_ulonglong
        )
    ]


HOOKPROC = ctypes.WINFUNCTYPE(
    wintypes.LPARAM,
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

        self._callback = None

    def install(
        self
    ) -> None:

        self._callback = HOOKPROC(
            self._hook_proc
        )

        self._handle = (

            user32.SetWindowsHookExW(

                WH_KEYBOARD_LL,

                self._callback,

                kernel32.GetModuleHandleW(
                    None
                ),

                0
            )
        )

        if not self._handle:

            raise HookInstallError(
                "Keyboard hook install failed"
            )

    def uninstall(
        self
    ) -> None:

        if self._handle:

            user32.UnhookWindowsHookEx(
                self._handle
            )

            self._handle = None

    def alive(
        self
    ) -> bool:

        return (
            self._handle
            is not None
        )

    def _hook_proc(
        self,

        n_code: int,

        w_param: int,

        l_param: int
    ) -> int:

        if n_code >= 0:

            data = ctypes.cast(

                l_param,

                ctypes.POINTER(
                    KBDLLHOOKSTRUCT
                )

            ).contents

            event = RawKeyboardEvent(

                vk_code=
                    data.vkCode,

                scan_code=
                    data.scanCode,

                pressed=(

                    w_param == WM_KEYDOWN

                ),

                injected=bool(

                    data.flags

                    &

                    LLKHF_INJECTED
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