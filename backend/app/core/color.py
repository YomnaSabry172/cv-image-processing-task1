# Owner: Lead — color conversion utilities
"""
Grayscale conversion, channel splitting, and color detection.
All from scratch (no cv2.cvtColor for grayscale).
"""
from __future__ import annotations

import numpy as np


def to_grayscale(img: np.ndarray) -> np.ndarray:
    """Convert an RGB image to grayscale using the luminosity formula.

    Formula: Y = 0.299·R + 0.587·G + 0.114·B
    These weights match human perception (ITU-R BT.601).

    If the input is already 2-D (grayscale), return it unchanged.
    Returns uint8.
    """
    if img.ndim == 2:
        return img
    # Apply luminosity weights to each channel
    gray = (
        0.299 * img[:, :, 0].astype(np.float64)
        + 0.587 * img[:, :, 1].astype(np.float64)
        + 0.114 * img[:, :, 2].astype(np.float64)
    )
    return np.clip(gray, 0, 255).astype(np.uint8)


def split_channels(img: np.ndarray) -> dict[str, np.ndarray]:
    """Split an image into its constituent channels.

    For color (3-D): returns {"r": ..., "g": ..., "b": ...}.
    For grayscale (2-D): returns {"gray": ...}.
    """
    if img.ndim == 2:
        return {"gray": img}
    return {
        "r": img[:, :, 0],
        "g": img[:, :, 1],
        "b": img[:, :, 2],
    }


def is_color(img: np.ndarray) -> bool:
    """Check if an image is color (3-D with 3 channels)."""
    return img.ndim == 3 and img.shape[2] == 3
