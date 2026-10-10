# Owner: D — histogram, PDF, CDF, equalization, normalization
"""
Histogram, PDF, CDF, histogram equalization, and min-max normalization. See CLAUDE.md §6.8.
ALL from scratch — np.histogram, np.bincount and cv2.calcHist are forbidden.

Note: normalize_minmax is also used by utils/channels.to_display (edges and frequency
results are displayed through it), so finish and push it early.
"""
from __future__ import annotations

from typing import Any

import numpy as np


def histogram(channel: np.ndarray, levels: int = 256) -> np.ndarray:
    """Count how many pixels have each value 0..levels-1. Returns int array of length levels.

    Use np.add.at (or a loop over levels). No np.histogram / np.bincount.
    """
    raise NotImplementedError("TODO (D): implement histogram()")


def pdf(hist: np.ndarray) -> np.ndarray:
    """pdf[i] = hist[i] / total pixels. Returns float64, sums to 1."""
    raise NotImplementedError("TODO (D): implement pdf()")


def cdf(p: np.ndarray) -> np.ndarray:
    """cdf[i] = pdf[0] + ... + pdf[i]. Returns float64, ends at 1.0."""
    raise NotImplementedError("TODO (D): implement cdf()")


def equalize(img: np.ndarray) -> np.ndarray:
    """Histogram equalization, per channel. Returns uint8, same shape as input.

    lut = round(cdf * (L - 1)), result = lut[channel].
    """
    raise NotImplementedError("TODO (D): implement equalize()")


def normalize_minmax(
    arr: np.ndarray, out_min: float = 0, out_max: float = 255
) -> np.ndarray:
    """Min-max stretch: (x - min) / (max - min) * (out_max - out_min) + out_min. Returns uint8.

    Must work on float and signed input. If max == min, return a constant image
    (no division by zero).
    """
    raise NotImplementedError("TODO (D): implement normalize_minmax()")


def channel_stats(img: np.ndarray) -> dict[str, Any]:
    """Statistics for each channel ("gray", or "r", "g", "b").

    Returns {<channel>: {"hist": [256 ints], "pdf": [...], "cdf": [...],
                         "min", "max", "mean", "std"}}.
    Lists must be plain Python lists (.tolist()) so they can be sent as JSON.
    The frontend charts read these keys directly — do not rename them.
    """
    raise NotImplementedError("TODO (D): implement channel_stats()")
