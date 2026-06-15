from __future__ import annotations

import json

from pathlib import Path

from serialization.schema_v2 import (
    REQUIRED,
    METADATA_REQUIRED,
    SCHEMA_VERSION
)

from serialization.models import (
    MousePacket,
    PresetMetadata,
    PresetV2
)

from core.exceptions import (
    InvalidPresetError
)


class PresetDecoder:

    def load(
        self,
        path: Path
    ) -> PresetV2:

        try:

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as file:

                data = json.load(
                    file
                )

        except Exception as exc:

            raise InvalidPresetError(

                f"Cannot read preset: {exc}"
            )

        self._validate(
            data
        )

        return self._build(
            data
        )

    #
    # schema validation
    #

    def _validate(
        self,
        data: dict
    ) -> None:

        #
        # root fields
        #

        for field in REQUIRED:

            if field not in data:

                raise InvalidPresetError(

                    f"Missing field: {field}"
                )

        #
        # schema version
        #

        if data["schema_version"] != SCHEMA_VERSION:

            raise InvalidPresetError(

                "Unsupported schema version"
            )

        #
        # metadata
        #

        metadata = data["metadata"]

        for field in METADATA_REQUIRED:

            if field not in metadata:

                raise InvalidPresetError(

                    f"Missing metadata: {field}"
                )

        #
        # packets
        #

        packets = data["packets"]

        if not isinstance(
            packets,
            list
        ):

            raise InvalidPresetError(

                "Packets must be list"
            )

        for packet in packets:

            if "dx" not in packet:

                raise InvalidPresetError(
                    "Packet dx missing"
                )

            if "dy" not in packet:

                raise InvalidPresetError(
                    "Packet dy missing"
                )

            if "dt_ns" not in packet:

                raise InvalidPresetError(
                    "Packet dt_ns missing"
                )

    #
    # build dataclasses
    #

    def _build(
        self,
        data: dict
    ) -> PresetV2:

        metadata_data = (
            data["metadata"]
        )

        metadata = PresetMetadata(

            machine_name=
                metadata_data[
                    "machine_name"
                ],

            os_version=
                metadata_data[
                    "os_version"
                ],

            python_version=
                metadata_data[
                    "python_version"
                ],

            monitor_count=
                metadata_data[
                    "monitor_count"
                ],

            record_duration_ns=
                metadata_data[
                    "record_duration_ns"
                ]
        )

        packets = []

        for item in data["packets"]:

            packets.append(

                MousePacket(

                    dx=item["dx"],

                    dy=item["dy"],

                    dt_ns=item["dt_ns"]
                )
            )

        return PresetV2(

            schema_version=
                data["schema_version"],

            created_at_ns=
                data["created_at_ns"],

            window_title=
                data["window_title"],

            screen_width=
                data["screen_width"],

            screen_height=
                data["screen_height"],

            dpi_scale=
                data["dpi_scale"],

            repeatable=
                data["repeatable"],

            metadata=
                metadata,

            packets=
                packets
        )