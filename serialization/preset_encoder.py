from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path


class PresetEncoder:

    def save(
        self,
        preset,
        path: Path
    ) -> None:

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                asdict(
                    preset
                ),

                f,

                indent=4,

                ensure_ascii=False
            )