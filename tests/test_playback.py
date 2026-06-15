from playback.playback_worker import (
    PlaybackWorker
)


def test_playback() -> None:

    p = PlaybackWorker()

    assert p is not None