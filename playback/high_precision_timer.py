from __future__ import annotations

import time


class HighPrecisionTimer:

    @staticmethod
    def wait_ns(
        duration_ns: int
    ) -> None:

        target = (

            time.perf_counter_ns()

            +

            duration_ns
        )

        while True:

            now = (
                time.perf_counter_ns()
            )

            if now >= target:
                break

            remaining = (
                target - now
            )

            if remaining > 1_000_000:

                time.sleep(
                    0.0005
                )