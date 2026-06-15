from serialization.preset_encoder import (
    PresetEncoder
)


def test_codec() -> None:

    e = PresetEncoder()

    assert e is not None