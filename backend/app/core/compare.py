# Owner: B — compare manual vs builtin implementations
"""
Run both manual and built-in implementations, time them, and compute
the absolute difference. Generic — any feature can reuse this. See CLAUDE.md §6.4.
"""
from __future__ import annotations

from typing import Any, Callable

import numpy as np


def run_both(
    manual_fn: Callable[..., np.ndarray],
    builtin_fn: Callable[..., np.ndarray],
    *args: Any,
    **kwargs: Any,
) -> dict[str, Any]:
    """Run manual_fn(*args, **kwargs) and builtin_fn(*args, **kwargs), timing each
    with time.perf_counter.

    Returns a dict with exactly these keys (the /api/filter route reads them):
        manual          — manual result (ndarray)
        builtin         — builtin result (ndarray)
        difference      — absolute difference image (uint8)
        time_manual_ms  — manual execution time in ms
        time_builtin_ms — builtin execution time in ms
        speedup         — time_manual_ms / time_builtin_ms
        max_abs_diff    — maximum absolute pixel difference (should be ≈ 0)
    """
    raise NotImplementedError("TODO (B): implement run_both()")
