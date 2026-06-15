from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True
)
class RawKeyboardEvent:

    vk_code: int

    scan_code: int

    pressed: bool

    injected: bool


@dataclass(
    frozen=True,
    slots=True
)
class RawMouseEvent:

    x: int

    y: int

    event_type: str

    injected: bool