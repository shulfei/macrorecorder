from __future__ import annotations

from runtime.controller import (
    RuntimeController
)

from runtime.commands import (
    RuntimeCommand,
    CommandType
)


class Application:

    def __init__(
        self,
        logger
    ) -> None:

        self.logger = logger

        self.controller = (
            RuntimeController(
                logger
            )
        )

    def start(
        self
    ) -> None:

        self.controller.start()

    def publish_start_record(
        self
    ) -> None:

        self.controller.publish(

            RuntimeCommand(
                CommandType.START_RECORD
            )
        )

    def publish_stop(
        self
    ) -> None:

        self.controller.publish(

            RuntimeCommand(
                CommandType.STOP
            )
        )

    def publish_pause(
        self
    ) -> None:

        self.controller.publish(

            RuntimeCommand(
                CommandType.PAUSE_RESUME
            )
        )