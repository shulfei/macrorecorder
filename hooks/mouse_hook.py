from __future__ import annotations

import ctypes

from ctypes import wintypes

from hooks.raw_events import (
    RawMouseEvent
)

from hooks.hook_queue import (
    HookQueue
)

from core.exceptions import (
    HookInstallError
)


user32 = ctypes.windll.user32

kernel32 = ctypes.windll.kernel32


WH_MOUSE_LL = 14

WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202

WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

LLMHF_INJECTED = 0x00000001


class POINT(
    ctypes.Structure
):

    _fields_ = [

        (
            "x",
            wintypes.LONG
        ),

        (
            "y",
            wintypes.LONG
        )
    ]


class MSLLHOOKSTRUCT(
    ctypes.Structure
):

    _fields_ = [

        (
            "pt",
            POINT
        ),

        (
            "mouseData",
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

        self._callback = None

    def install(
        self
    ) -> None:

        self._callback = HOOKPROC(
            self._hook_proc
        )

        self._handle = (

            user32.SetWindowsHookExW(

                WH_MOUSE_LL,

                self._callback,

                kernel32.GetModuleHandleW(
                    None
                ),

                0
            )
        )

        if not self._handle:

            raise HookInstallError(
                "Mouse hook install failed"
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
                    MSLLHOOKSTRUCT
                )

            ).contents

            event = RawMouseEvent(

                x=data.pt.x,

                y=data.pt.y,

                event_type=
                    str(w_param),

                injected=bool(

                    data.flags

                    &

                    LLMHF_INJECTED
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