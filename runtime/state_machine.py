from __future__ import annotations

from enum import Enum


class EngineState(
    Enum
):
    BOOTING = 1

    READY = 2

    RECORDING = 3

    SAVING = 4

    LOADING = 5

    PLAYING = 6

    PAUSED = 7

    STOPPING = 8

    SHUTTING_DOWN = 9

    ERROR = 10


class InvalidTransition(
    RuntimeError
):
    pass


class RuntimeStateMachine:

    ALLOWED = {

        EngineState.BOOTING: {

            EngineState.READY
        },

        EngineState.READY: {

            EngineState.RECORDING,

            EngineState.LOADING,

            EngineState.SHUTTING_DOWN
        },

        EngineState.RECORDING: {

            EngineState.SAVING,

            EngineState.STOPPING
        },

        EngineState.SAVING: {

            EngineState.READY
        },

        EngineState.LOADING: {

            EngineState.PLAYING
        },

        EngineState.PLAYING: {

            EngineState.PAUSED,

            EngineState.STOPPING
        },

        EngineState.PAUSED: {

            EngineState.PLAYING,

            EngineState.STOPPING
        }
    }

    def __init__(
        self
    ) -> None:

        self._state = (
            EngineState.BOOTING
        )

    @property
    def state(
        self
    ) -> EngineState:

        return self._state

    def transition(
        self,
        new_state: EngineState
    ) -> None:

        allowed = (
            self.ALLOWED.get(
                self._state,

                set()
            )
        )

        if new_state \
           not in allowed:

            raise InvalidTransition(

                f"{self._state}"

                f" -> "

                f"{new_state}"
            )

        self._state = (
            new_state
        )