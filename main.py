from __future__ import annotations

import sys
import signal
import threading

from core.cli import CLIParser
from core.singleton import SingleInstance
from core.config import RuntimeConfig
from core.file_logger import FileLogger
from core.exceptions import (
    MacroRecorderError
)

from runtime.controller import (
    RuntimeController
)

from hooks.hook_queue import (
    HookQueue
)

from hooks.keyboard_hook import (
    KeyboardHook
)

from hooks.mouse_hook import (
    MouseHook
)

from hooks.hook_dispatcher import (
    HookDispatcher
)

from hooks.hook_thread import (
    HookThread
)

from hooks.hook_watchdog import (
    HookWatchdog
)

from runtime.commands import (
    RuntimeCommand,
    CommandType,
    PlaybackCommand
)

from serialization.preset_decoder import (
    PresetDecoder
)


class Application:

    def __init__(
        self
    ) -> None:

        self.shutdown_event = (
            threading.Event()
        )

        #
        # CLI
        #

        self.cli = (
            CLIParser.parse()
        )

        #
        # single instance
        #

        self.instance = (
            SingleInstance(

                RuntimeConfig().mutex_name
            )
        )

        self.instance.acquire()

        #
        # logger
        #

        logfile = None

        if self.cli.file:

            logfile = (
                self.cli.file
            )

        self.logger = (
            FileLogger.build(

                logfile or "macro.log"
            )
        )

        #
        # runtime controller
        #

        self.controller = (
            RuntimeController(
                self.logger
            )
        )

        #
        # hook subsystem
        #

        self.hook_queue = (
            HookQueue()
        )

        self.keyboard_hook = (
            KeyboardHook(
                self.hook_queue
            )
        )

        self.mouse_hook = (
            MouseHook(
                self.hook_queue
            )
        )

        self.dispatcher = (
            HookDispatcher(

                self.hook_queue,

                self.controller
            )
        )

        self.hook_thread = (
            HookThread(

                installer=
                    self._install_hooks
            )
        )

        self.watchdog = (
            HookWatchdog(

                self.keyboard_hook,

                self.mouse_hook
            )
        )

        signal.signal(
            signal.SIGINT,
            self._signal_handler
        )

    #
    # startup
    #

    def start(
        self
    ) -> None:

        self.logger.info(
            "Starting application"
        )

        #
        # start controller
        #

        self.controller.start()

        #
        # dispatcher thread
        #

        self.dispatcher.start()

        #
        # hook watchdog
        #

        self.watchdog.start()

        #
        # windows hooks
        #

        self.hook_thread.start()

        #
        # playback mode
        #

        if self.cli.preset:

            self._start_playback()

        #
        # main loop
        #

        self.shutdown_event.wait()

        self.shutdown()

    #
    # install hooks
    #

    def _install_hooks(
        self
    ) -> None:

        self.keyboard_hook.install()

        self.mouse_hook.install()

    #
    # playback mode
    #

    def _start_playback(
        self
    ) -> None:

        decoder = (
            PresetDecoder()
        )

        preset = (
            decoder.load(
                self.cli.preset
            )
        )

        command = RuntimeCommand(

            CommandType.START_PLAYBACK,

            PlaybackCommand(

                preset_path=
                    self.cli.preset,

                repeat=
                    self.cli.repeat
            )
        )

        self.controller.publish(
            command
        )

        self.logger.info(
            "Playback mode"
        )

    #
    # ctrl+c
    #

    def _signal_handler(
        self,
        *_args
    ) -> None:

        self.shutdown_event.set()

    #
    # shutdown
    #

    def shutdown(
        self
    ) -> None:

        self.logger.info(
            "Shutdown initiated"
        )

        #
        # stop dispatcher
        #

        self.dispatcher.stop()

        #
        # unhook
        #

        self.keyboard_hook.uninstall()

        self.mouse_hook.uninstall()

        #
        # stop controller
        #

        self.controller.publish(

            RuntimeCommand(
                CommandType.SHUTDOWN
            )
        )

        #
        # release mutex
        #

        self.instance.release()

        self.logger.info(
            "Shutdown complete"
        )


def main() -> int:

    #
    # python version strict
    #

    version = sys.version_info

    if not (

        version.major == 3

        and

        version.minor == 14
    ):

        print(

            "Requires Python 3.14.4"

        )

        return 1

    try:

        app = Application()

        app.start()

        return 0

    except MacroRecorderError as exc:

        print(
            f"Error: {exc}"
        )

        return 1

    except KeyboardInterrupt:

        return 0

    except Exception as exc:

        print(
            f"Fatal: {exc}"
        )

        return 1


if __name__ == "__main__":

    raise SystemExit(
        main()
    )