# Owner: B — spatial low-pass filters (average, Gaussian, median)
"""
Smoothing filters: average, Gaussian, median. See CLAUDE.md §6.6.
Each has a manual (from scratch) and a built-in (SciPy) implementation.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import median_filter

from app.core.convolution import apply_kernel, pad
from app.core.kernels import box, gaussian
from app.utils.channels import apply_per_channel


def _median_manual_2d(channel: np.ndarray, k: int) -> np.ndarray:
    """Manual median filter for a single 2-D channel.

    Uses sliding_window_view to gather k×k neighbourhoods, then takes
    np.median over them. Keeps input uint8 to limit memory usage.
    """
    # Pad the channel so the output has the same spatial size.
    padded = pad(channel, k, k)
    # Create a view of all k×k sliding windows — no data is copied.
    windows = np.lib.stride_tricks.sliding_window_view(padded, (k, k))
    # Median over the two window axes (the last two dimensions).
    result = np.median(windows, axis=(-2, -1))
    return np.clip(result, 0, 255).astype(np.uint8)


def _median_builtin_2d(channel: np.ndarray, k: int) -> np.ndarray:
    """Builtin median filter for a single 2-D channel using SciPy."""
    # SciPy reflect mode matches NumPy symmetric padding.
    result = median_filter(channel, size=k, mode="reflect")
    return np.clip(result, 0, 255).astype(np.uint8)


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

    if method == "average":
        # Reuse the shared box kernel and correlation engine.
        kernel = box(k)
        result = apply_kernel(img, kernel, implementation=implementation)
        return np.clip(result, 0, 255).astype(np.uint8)

    if method == "gaussian":
        # Reuse the shared kernel and correlation engine.
        kernel = gaussian(k, sigma)
        result = apply_kernel(img, kernel, implementation=implementation)
        return np.clip(result, 0, 255).astype(np.uint8)

    # method == "median"
    if implementation == "builtin":
        return apply_per_channel(_median_builtin_2d, img, k)
    else:
        return apply_per_channel(_median_manual_2d, img, k)
