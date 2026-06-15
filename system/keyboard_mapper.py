from __future__ import annotations


VK_TO_NAME = {

    0x41: "A",

    0x42: "B",

    0x43: "C",

    0x44: "D",

    0x45: "E",

    0x46: "F",

    0x47: "G",

    0x48: "H",

    0x49: "I",

    0x4A: "J",

    0x4B: "K",

    0x4C: "L",

    0x4D: "M",

    0x4E: "N",

    0x4F: "O",

    0x50: "P"
}


class KeyboardMapper:

    @staticmethod
    def to_name(
        vk_code: int
    ) -> str:

        return VK_TO_NAME.get(

            vk_code,

            f"VK_{vk_code}"
        )