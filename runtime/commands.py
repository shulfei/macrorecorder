from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class CommandType(
    Enum
):
    START_RECORD = (
        "start_record"
    )

    STOP = (
        "stop_record"
    )

    PAUSE_RESUME = (
        "pause_resume"
    )

    START_PLAYBACK = (
        "start_playback"
    )

    SHUTDOWN = (
        "shutdown"
    )

    RAW_KEYBOARD = (
        "raw_keyboard"
    )

    RAW_MOUSE = (
        "raw_mouse"
    )


@dataclass(
    frozen=True,
    slots=True
)
class RuntimeCommand:

    command: CommandType

    payload: object | None = None


@dataclass(
    frozen=True,
    slots=True
)
class PlaybackCommand:

    preset_path: Path

    repeat: bool