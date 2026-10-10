# Owner: B — convolution engine (manual + builtin)
"""
2-D correlation with manual (vectorized) and built-in (SciPy) implementations.
This project uses correlation (the kernel is NOT flipped). See CLAUDE.md §3.3, §3.4, §6.3.

Border handling must match between the two implementations:
  - Manual:   np.pad(mode="symmetric")
  - Built-in: scipy.ndimage mode="reflect"   (same thing, different name)

C's edge detection depends on apply_kernel — keep the signature exactly as is.
"""
from __future__ import annotations

import numpy as np


def pad(img: np.ndarray, kh: int, kw: int) -> np.ndarray:
    """Pad a 2-D image for correlation with a kernel of size (kh, kw).

    Must handle even kernels (Roberts 2×2). Anchor = (kh // 2, kw // 2):
        top    = kh // 2
        bottom = kh - 1 - kh // 2
        left   = kw // 2
        right  = kw - 1 - kw // 2
    Use np.pad(..., mode="symmetric").
    """
    raise NotImplementedError("TODO (B): implement pad()")


def correlate2d_manual(img2d: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Vectorized manual 2-D correlation. Returns float64, same H×W as input.

    Do NOT loop over pixels. Loop over kernel positions (a, b) only:
        out += kernel[a, b] * padded[a:a+H, b:b+W]
    """
    raise NotImplementedError("TODO (B): implement correlate2d_manual()")


def correlate2d_builtin(img2d: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Built-in 2-D correlation. Returns float64, same H×W as input.

    Use scipy.ndimage.correlate(img2d.astype(np.float64), kernel, mode="reflect").
    """
    raise NotImplementedError("TODO (B): implement correlate2d_builtin()")


def apply_kernel(
    img: np.ndarray,
    kernel: np.ndarray,
    implementation: str = "builtin",
) -> np.ndarray:
    """Apply a correlation kernel to an image (gray or color).

    Args:
        img: Input image (uint8, gray 2-D or RGB 3-D).
        kernel: 2-D float64 kernel.
        implementation: "manual" or "builtin" (raise ValueError otherwise).

    Returns:
        float64 array, same shape as input.

    Use apply_per_channel from app.utils.channels for color images.
    """
    raise NotImplementedError("TODO (B): implement apply_kernel()")
