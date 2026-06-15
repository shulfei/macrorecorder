from __future__ import annotations

import logging


class FileLogger:

    @staticmethod
    def build(
        filename: str
    ) -> logging.Logger:

        logger = logging.getLogger(
            "macro"
        )

        logger.setLevel(
            logging.INFO
        )

        handler = logging.FileHandler(
            filename,
            encoding="utf-8"
        )

        logger.addHandler(
            handler
        )

        return logger

    @staticmethod
    def console():

        logger = logging.getLogger(
            "macro"
        )

        logger.setLevel(
            logging.INFO
        )

        handler = logging.StreamHandler()

        logger.addHandler(
            handler
        )

        return logger