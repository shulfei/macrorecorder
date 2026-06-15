from __future__ import annotations

from enum import Enum


class EventType(
    Enum
):
    MOUSE_MOVE = 1

    LEFT_DOWN = 2

    LEFT_UP = 3

    RIGHT_DOWN = 4

    RIGHT_UP = 5

    KEY_DOWN = 6

    KEY_UP = 7

    PAUSE = 8