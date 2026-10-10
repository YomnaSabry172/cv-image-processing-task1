# Owner: Lead — per-channel application and display helpers
"""
Utilities for applying single-channel functions to multi-channel images
and converting signed/float results to displayable uint8.
"""
from __future__ import annotations

from typing import Callable

import numpy as np


def apply_per_channel(
    fn: Callable[..., np.ndarray],
    img: np.ndarray,
    *args,
    **kwargs,
) -> np.ndarray:
    """Apply a single-channel function to each channel of a color image.

    If *img* is 2-D (grayscale), calls *fn* once.
    If *img* is 3-D (H×W×C), calls *fn* on each channel and stacks.
    """
    if img.ndim == 2:
        return fn(img, *args, **kwargs)
    channels = [fn(img[:, :, c], *args, **kwargs) for c in range(img.shape[2])]
    return np.stack(channels, axis=-1)


def to_display(
    arr: np.ndarray,
    mode: str = "minmax",
) -> np.ndarray:
    """Convert a signed/float array to displayable uint8.

    Modes:
        minmax — min-max stretch to [0, 255]. Uses core.histogram.normalize_minmax.
        abs    — take |x|, then min-max stretch.
        offset — add 128, then clip to [0, 255]. Good for high-pass previews.
    """
    from app.core.histogram import normalize_minmax

    arr = arr.astype(np.float64)

    if mode == "abs":
        arr = np.abs(arr)
        return normalize_minmax(arr)
    elif mode == "offset":
        arr = arr + 128.0
        return np.clip(arr, 0, 255).astype(np.uint8)
    else:  # "minmax"
        return normalize_minmax(arr)
