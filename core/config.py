from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True
)
class RuntimeConfig:

    preset_dir: Path = Path(
        "presets"
    )

    logs_dir: Path = Path(
        "logs"
    )

    hook_poll_interval_ms: int = 1

    playback_pause_poll_ms: int = 10

    max_event_queue_size: int = 500000

    debug_enabled: bool = False

    default_repeat: bool = False

    json_indent: int = 4

    mutex_name: str = (
        "MacroRecorderMutexV5"
    )

    keyboard_buffer_size: int = 4096

    mouse_buffer_size: int = 4096