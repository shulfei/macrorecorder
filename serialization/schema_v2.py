from __future__ import annotations


SCHEMA_VERSION = 2


REQUIRED = [

    "schema_version",

    "created_at_ns",

    "window_title",

    "screen_width",

    "screen_height",

    "dpi_scale",

    "repeatable",

    "metadata",

    "packets"
]


METADATA_REQUIRED = [

    "machine_name",

    "os_version",

    "python_version",

    "monitor_count",

    "record_duration_ns"
]


PACKET_REQUIRED = [

    "dx",

    "dy",

    "dt_ns"
]