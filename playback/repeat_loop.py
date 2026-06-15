from __future__ import annotations


class RepeatLoop:

    def __init__(
        self,
        enabled: bool
    ) -> None:

        self.enabled = enabled

    def repeat(
        self
    ) -> bool:

        return self.enabled