# Owner: D — POST /api/histogram
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

LEVELS = 256


def histogram(channel: np.ndarray, levels: int = LEVELS) -> np.ndarray:
    """Count how many pixels have each value 0..levels-1. Returns int array of length levels.

    Use np.add.at (or a loop over levels). No np.histogram / np.bincount.
    """
    hist = np.zeros(levels, dtype=np.int64)
    # Each pixel value is used as an index into the histogram, and np.add.at adds 1
    # at that index. Unlike hist[values] += 1, it counts repeated values correctly.
    np.add.at(hist, channel.ravel().astype(np.int64), 1)
    return hist


def pdf(hist: np.ndarray) -> np.ndarray:
    """pdf[i] = hist[i] / total pixels. Returns float64, sums to 1."""
    total = hist.sum()
    if total == 0:
        return np.zeros(hist.shape, dtype=np.float64)
    # Dividing by the pixel count turns counts into probabilities.
    return hist.astype(np.float64) / total


def cdf(p: np.ndarray) -> np.ndarray:
    """cdf[i] = pdf[0] + ... + pdf[i]. Returns float64, ends at 1.0."""
    # Running total of the probabilities: the fraction of pixels <= level i.
    return np.cumsum(p, dtype=np.float64)


def _equalize_channel(channel: np.ndarray) -> np.ndarray:
    """Equalize one 2-D uint8 channel with a lookup table."""
    c = cdf(pdf(histogram(channel)))
    # Map each level to round(cdf * (L-1)), so the output CDF is close to a diagonal line.
    lut = np.rint(c * (LEVELS - 1)).astype(np.uint8)
    # Indexing the LUT with the image replaces every pixel by its new level at once.
    return lut[channel]


def equalize(img: np.ndarray) -> np.ndarray:
    """Histogram equalization, per channel. Returns uint8, same shape as input.

    lut = round(cdf * (L - 1)), result = lut[channel].
    """
    img = img.astype(np.uint8)
    if img.ndim == 2:
        return _equalize_channel(img)
    # Color: each channel is equalized separately (this can shift colors).
    return np.stack(
        [_equalize_channel(img[:, :, c]) for c in range(img.shape[2])], axis=-1
    )


def normalize_minmax(
    arr: np.ndarray, out_min: float = 0, out_max: float = 255
) -> np.ndarray:
    """Min-max stretch: (x - min) / (max - min) * (out_max - out_min) + out_min. Returns uint8.

    Must work on float and signed input. If max == min, return a constant image
    (no division by zero).
    """
    # Use floating-point arithmetic to support signed filter outputs.
    values = arr.astype(np.float64)

    # Find the lowest and highest values in this array.
    minimum = values.min()
    maximum = values.max()

    # A constant image has no range to stretch; avoid division by zero.
    if maximum == minimum:
        return np.full(values.shape, out_min, dtype=np.uint8)

    # Shift the minimum to 0, then scale the maximum to 1.
    normalized = (values - minimum) / (maximum - minimum)

    # Map the 0–1 values into the requested output range.
    stretched = normalized * (out_max - out_min) + out_min

    # Round (not truncate) and keep the result in valid pixel range.
    return np.clip(np.rint(stretched), 0, 255).astype(np.uint8)


def channel_stats(img: np.ndarray) -> dict[str, Any]:
    """Statistics for each channel ("gray", or "r", "g", "b").

    Returns {<channel>: {"hist": [256 ints], "pdf": [...], "cdf": [...],
                         "min", "max", "mean", "std"}}.
    Lists must be plain Python lists (.tolist()) so they can be sent as JSON.
    The frontend charts read these keys directly — do not rename them.
    """
    if img.ndim == 2:
        channels = {"gray": img}
    else:
        channels = {"r": img[:, :, 0], "g": img[:, :, 1], "b": img[:, :, 2]}

    stats: dict[str, Any] = {}
    for name, ch in channels.items():
        h = histogram(ch)
        p = pdf(h)
        stats[name] = {
            "hist": h.tolist(),
            "pdf": p.tolist(),
            "cdf": cdf(p).tolist(),
            "min": int(ch.min()),
            "max": int(ch.max()),
            "mean": float(ch.mean()),
            "std": float(ch.std()),
        }
    return stats