from __future__ import annotations

import time

from system.environment import (
    EnvironmentInfo
)

from serialization.models import (
    PresetV2
)


class PresetBuilder:

    @staticmethod
    def build(

        packets: list,

        duration_ns: int,

        monitor_count: int,

        window_title: str,

        repeatable: bool

    ) -> PresetV2:

        metadata = (
            EnvironmentInfo.collect(

                duration_ns,

                monitor_count
            )
        )

        return PresetV2(

            schema_version=2,

            created_at_ns=
                time.time_ns(),

            window_title=
                window_title,

            screen_width=1920,

            screen_height=1080,

            dpi_scale=1.0,

            repeatable=
                repeatable,

            metadata=
                metadata,

            packets=
                packets
        )