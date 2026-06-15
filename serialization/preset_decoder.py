from __future__ import annotations

import json

from serialization.schema_v2 import (
    REQUIRED
)


class PresetDecoder:

    def load(
        self,
        path
    ) -> dict:

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            data = json.load(
                f
            )

        for field in REQUIRED:

            if field \
               not in data:

                raise ValueError(

                    f"Missing {field}"
                )

        return data