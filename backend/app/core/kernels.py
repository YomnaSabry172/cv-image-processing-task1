# Owner: B — kernel generators for convolution-based operations
"""
Generates filter kernels used by convolution, smoothing, and edge detection.
All kernels are from scratch (plain NumPy). See CLAUDE.md §6.2.

Every kernel is returned as a float64 NumPy array.
"""
from __future__ import annotations

import numpy as np


def box(k: int) -> np.ndarray:
    """Box (average) kernel of size k×k.

    Each element = 1/k², so the kernel sums to 1 (preserves brightness).
    k must be a positive odd integer (raise ValueError otherwise).
    """
    raise NotImplementedError("TODO (B): implement box(k) — ones((k, k)) / k²")


def gaussian(k: int, sigma: float) -> np.ndarray:
    """2-D Gaussian kernel of size k×k with standard deviation sigma.

    Sampled on a centered integer grid: G(x,y) = exp(-(x²+y²) / (2σ²)).
    Normalized so the kernel sums to 1.
    k must be a positive odd integer and sigma > 0 (raise ValueError otherwise).
    """
    raise NotImplementedError("TODO (B): implement gaussian(k, sigma)")


def sobel() -> tuple[np.ndarray, np.ndarray]:
    """Sobel edge-detection kernels (kx, ky).

    kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]   (the slide has a typo here)
    """
    raise NotImplementedError("TODO (B): implement sobel()")


def prewitt() -> tuple[np.ndarray, np.ndarray]:
    """Prewitt edge-detection kernels (kx, ky).

    kx = [[-1, 0, 1]] repeated 3 rows
    ky = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    """
    raise NotImplementedError("TODO (B): implement prewitt()")


def roberts() -> tuple[np.ndarray, np.ndarray]:
    """Roberts cross edge-detection kernels (kx, ky). These are 2×2 (even-sized).

    kx = [[1, 0], [0, -1]]
    ky = [[0, 1], [-1, 0]]
    """
    raise NotImplementedError("TODO (B): implement roberts()")


def laplacian() -> np.ndarray:
    """Laplacian kernel: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]."""
    raise NotImplementedError("TODO (B): implement laplacian()")
