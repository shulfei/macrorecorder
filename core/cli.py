from __future__ import annotations

import argparse

from dataclasses import dataclass
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True
)
class CLIArguments:

    preset: Path | None

    repeat: bool

    debug: bool

    file: Path | None


class CLIParser:

    @staticmethod
    def parse() -> CLIArguments:

        parser = argparse.ArgumentParser(

            prog="macro_recorder",

            description=(
                "Industrial Windows Macro Recorder"
            )
        )

        parser.add_argument(

            "-p",
            "--preset",

            type=Path,

            required=False,

            help=(
                "Run playback using preset json"
            )
        )

        parser.add_argument(

            "-r",
            "--repeat",

            action="store_true",

            help=(
                "Repeat playback forever"
            )
        )

        parser.add_argument(

            "-d",
            "--debug",

            action="store_true",

            help=(
                "Enable verbose debug output"
            )
        )

        parser.add_argument(

            "-f",
            "--file",

            type=Path,

            required=False,

            help=(
                "Write logs to file"
            )
        )

        args = parser.parse_args()

        return CLIArguments(

            preset=args.preset,

            repeat=args.repeat,

            debug=args.debug,

            file=args.file
        )