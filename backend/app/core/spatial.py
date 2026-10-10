# Owner: B — spatial low-pass filters (average, Gaussian, median)
"""
Smoothing filters: average, Gaussian, median. See CLAUDE.md §6.6.
Each has a manual (from scratch) and a built-in (SciPy) implementation.
"""
from __future__ import annotations

import numpy as np


def smooth(
    img: np.ndarray,
    method: str,
    k: int = 3,
    sigma: float = 1.0,
    implementation: str = "builtin",
) -> np.ndarray:
    """Apply a low-pass (smoothing) filter to an image.

    One function for all low-pass filters, as the assignment asks.

    Args:
        img: Input uint8 image (gray or RGB).
        method: "average" | "gaussian" | "median" (raise ValueError otherwise).
        k: Kernel size (positive odd integer, raise ValueError otherwise).
        sigma: Standard deviation (Gaussian only).
        implementation: "manual" or "builtin".

    Returns:
        Smoothed uint8 image, same shape as input.

    average  → apply_kernel(img, box(k))
    gaussian → apply_kernel(img, gaussian(k, sigma))
    median   → manual: sliding_window_view + np.median
               builtin: scipy.ndimage.median_filter(size=k, mode="reflect")
    """
    raise NotImplementedError("TODO (B): implement smooth()")
