from __future__ import annotations


class EventSerializer:

    @staticmethod
    def encode_mouse(
        packet
    ) -> dict:

        return {

            "type": "mouse",

            "dx": packet.dx,

            "dy": packet.dy,

            "dt_ns": packet.dt_ns
        }

    @staticmethod
    def decode_mouse(
        data: dict
    ):

        from serialization.models import (
            MousePacket
        )

        return MousePacket(

            dx=data["dx"],

            dy=data["dy"],

            dt_ns=data["dt_ns"]
        )