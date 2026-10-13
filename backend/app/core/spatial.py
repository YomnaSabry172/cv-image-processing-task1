# Owner: B — spatial low-pass filters (average, Gaussian, median)
"""
Smoothing filters: average, Gaussian, median. See CLAUDE.md §6.6.
Each has a manual (from scratch) and a built-in (SciPy) implementation.
"""
from __future__ import annotations

import numpy as np

from app.core.convolution import apply_kernel
from app.core.kernels import gaussian


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
    if method not in ("average", "gaussian", "median"):
        raise ValueError("Unknown smoothing method")
    if k < 1 or k % 2 == 0:
        raise ValueError("k must be a positive odd integer")
    if implementation not in ("manual", "builtin"):
        raise ValueError("implementation must be 'manual' or 'builtin'")

    if method == "gaussian":
        # Reuse the shared kernel and correlation engine.
        kernel = gaussian(k, sigma)
        result = apply_kernel(img, kernel, implementation=implementation)
        return np.clip(result, 0, 255).astype(np.uint8)

    # The remaining smoothing methods are still Member B's work.
    raise NotImplementedError(
        f"TODO (B): implement smooth() method '{method}'"
    )
