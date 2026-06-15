from __future__ import annotations

import time


class HighPrecisionClock:

    @staticmethod
    def now_ns() -> int:
        return time.perf_counter_ns()