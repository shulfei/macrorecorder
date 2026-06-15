from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler


class FileLogger:

    @staticmethod
    def build(
        filename: str
    ) -> logging.Logger:

        logger = logging.getLogger(
            "macro"
        )

        handler = (
            RotatingFileHandler(

                filename,

                maxBytes=
                    10_000_000,

                backupCount=5
            )
        )

        logger.addHandler(
            handler
        )

        return logger