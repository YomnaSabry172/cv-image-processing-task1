# Owner: B — compare manual vs builtin implementations
"""
Run both manual and built-in implementations, time them, and compute
the absolute difference. Generic — any feature can reuse this. See CLAUDE.md §6.4.
"""
from __future__ import annotations

import time
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
    # Time the manual implementation.
    t0 = time.perf_counter()
    manual_result = manual_fn(*args, **kwargs)
    time_manual = (time.perf_counter() - t0) * 1000.0

    # Time the builtin implementation.
    t0 = time.perf_counter()
    builtin_result = builtin_fn(*args, **kwargs)
    time_builtin = (time.perf_counter() - t0) * 1000.0

    # Compute the absolute difference in float64 for precision.
    abs_diff = np.abs(
        manual_result.astype(np.float64) - builtin_result.astype(np.float64)
    )
    max_abs_diff = float(abs_diff.max())

    # Convert difference to a displayable uint8 image.
    difference = np.clip(abs_diff, 0, 255).astype(np.uint8)

    # Speedup ratio: avoid division by zero.
    speedup = (
        time_manual / time_builtin
        if time_builtin > 0
        else float("inf")
    )

    return {
        "manual": manual_result,
        "builtin": builtin_result,
        "difference": difference,
        "time_manual_ms": round(time_manual, 2),
        "time_builtin_ms": round(time_builtin, 2),
        "speedup": round(speedup, 2),
        "max_abs_diff": max_abs_diff,
    }
