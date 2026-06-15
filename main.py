from __future__ import annotations

import signal
import sys
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

from runtime.commands import (
    RuntimeCommand,
    CommandType,
    PlaybackCommand
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


class Application:

    def __init__(
        self
    ) -> None:

        self._shutdown_lock = (
            threading.Lock()
        )

        self._shutdown_started = False

        self.shutdown_event = (
            threading.Event()
        )

        #
        # cli
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

        if self.cli.file:

            self.logger = (
                FileLogger.build(
                    self.cli.file
                )
            )

        else:

            self.logger = (
                FileLogger.console()
            )

        #
        # debug mode
        #

        if self.cli.debug:

            self.logger.info(
                "Debug mode enabled"
            )

        #
        # controller
        #

        self.controller = (
            RuntimeController(
                self.logger
            )
        )

        #
        # hooks subsystem
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

        #
        # signals
        #

        signal.signal(
            signal.SIGINT,
            self._signal_handler
        )

        if hasattr(
            signal,
            "SIGTERM"
        ):

            signal.signal(
                signal.SIGTERM,
                self._signal_handler
            )

    #
    # start
    #

    def start(
        self
    ) -> None:

        self.logger.info(
            "Application starting"
        )

        #
        # start controller
        #

        self.controller.start()

        #
        # start dispatcher
        #

        self.dispatcher.start()

        #
        # install hooks thread
        #

        self.hook_thread.start()

        #
        # watchdog AFTER hook install thread
        #

        self.watchdog.start()

        #
        # playback mode
        #

        if self.cli.preset:

            self._start_playback()

        #
        # wait forever
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
            "Playback mode enabled"
        )

    #
    # signal
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

        #
        # prevent double shutdown
        #

        with self._shutdown_lock:

            if self._shutdown_started:

                return

            self._shutdown_started = True

        self.logger.info(
            "Shutdown initiated"
        )

        #
        # stop watchdog
        #

        try:

            self.watchdog.stop()

        except Exception:
            pass

        #
        # stop dispatcher
        #

        try:

            self.dispatcher.stop()

        except Exception:
            pass

        #
        # uninstall hooks
        #

        try:

            self.keyboard_hook.uninstall()

        except Exception:
            pass

        try:

            self.mouse_hook.uninstall()

        except Exception:
            pass

        #
        # stop hook thread
        # if implemented
        #

        if hasattr(
            self.hook_thread,
            "stop"
        ):

            try:

                self.hook_thread.stop()

            except Exception:
                pass

        #
        # shutdown controller
        #

        try:

            self.controller.publish(

                RuntimeCommand(
                    CommandType.SHUTDOWN
                )
            )

        except Exception:
            pass

        #
        # wait controller
        #

        if hasattr(
            self.controller,
            "join"
        ):

            try:

                self.controller.join()

            except Exception:
                pass

        #
        # release mutex
        #

        try:

            self.instance.release()

        except Exception:
            pass

        self.logger.info(
            "Shutdown complete"
        )


def main() -> int:

    #
    # strict python version
    #

    version = (
        sys.version_info
    )

    if not (

        version.major == 3
        and
        version.minor == 14
        and
        version.micro == 6
    ):

        print(
            "Requires Python 3.14.6 exactly"
        )

        return 1

    app = None

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

    finally:

        #
        # emergency cleanup
        #

        if app is not None:

            try:

                app.shutdown()

            except Exception:
                pass


if __name__ == "__main__":

    raise SystemExit(
        main()
    )