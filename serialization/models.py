from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    slots=True
)
class MousePacket:

    dx: int
    dy: int
    dt_ns: int


@dataclass(
    slots=True
)
class PresetMetadata:

    machine_name: str

    os_version: str

    python_version: str

    monitor_count: int

    record_duration_ns: int


@dataclass(
    slots=True
)
class PresetV2:

    schema_version: int

    created_at_ns: int

    window_title: str

    screen_width: int

    screen_height: int

    dpi_scale: float

    repeatable: bool

    metadata: PresetMetadata

    packets: list[MousePacket]