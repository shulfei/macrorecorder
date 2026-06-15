from __future__ import annotations

import ctypes

from ctypes import wintypes

from core.exceptions import (
    MacroRecorderError
)


kernel32 = ctypes.windll.kernel32


ERROR_ALREADY_EXISTS = 183


class SingleInstance:

    def __init__(
        self,
        mutex_name: str
    ) -> None:

        self._mutex_name = (
            mutex_name
        )

        self._handle = None

    def acquire(
        self
    ) -> None:

        self._handle = (

            kernel32.CreateMutexW(

                None,

                wintypes.BOOL(
                    True
                ),

                self._mutex_name
            )
        )

        if not self._handle:

            raise MacroRecorderError(

                "Failed to create mutex"
            )

        error = (
            kernel32.GetLastError()
        )

        if error == ERROR_ALREADY_EXISTS:

            raise MacroRecorderError(

                "Another instance is already running"
            )

    def release(
        self
    ) -> None:

        if self._handle:

            kernel32.ReleaseMutex(

                self._handle
            )

            kernel32.CloseHandle(

                self._handle
            )

            self._handle = None