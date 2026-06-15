from capture.delta_recorder import (
    DeltaRecorder
)


def test_delta() -> None:

    d = DeltaRecorder()

    assert d is not None