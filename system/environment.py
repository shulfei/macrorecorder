from __future__ import annotations

import os
import platform
import sys

from serialization.models import (
    PresetMetadata
)


class EnvironmentInfo:

    @staticmethod
    def collect(
        duration_ns: int,
        monitor_count: int
    ) -> PresetMetadata:

        return PresetMetadata(

            machine_name=
                platform.node(),

            os_version=
                platform.platform(),

            python_version=
                sys.version,

            monitor_count=
                monitor_count,

            record_duration_ns=
                duration_ns
        )