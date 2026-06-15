from __future__ import annotations


class MacroRecorderError(
    Exception
):
    pass


class HookInstallError(
    MacroRecorderError
):
    pass


class PlaybackError(
    MacroRecorderError
):
    pass


class RecordingError(
    MacroRecorderError
):
    pass


class SerializationError(
    MacroRecorderError
):
    pass


class WindowMismatchError(
    MacroRecorderError
):
    pass


class InvalidPresetError(
    MacroRecorderError
):
    pass