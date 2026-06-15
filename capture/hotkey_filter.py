from __future__ import annotations


class ServiceHotkeyFilter:

    def __init__(
        self
    ) -> None:

        self.ctrl = False
        self.alt = False

    def process(
        self,
        vk: int,
        pressed: bool
    ) -> bool:

        if vk in (
            0xA2,
            0xA3
        ):
            self.ctrl = pressed

        if vk in (
            0xA4,
            0xA5
        ):
            self.alt = pressed

        if self.ctrl and self.alt:

            if vk in (
                0x5A,
                0x58,
                0x43
            ):
                return False

        return True