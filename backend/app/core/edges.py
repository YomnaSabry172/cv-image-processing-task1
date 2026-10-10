# Owner: C — edge detection (Sobel, Prewitt, Roberts from scratch + Canny via cv2)
"""
Edge detection using first-derivative operators. See CLAUDE.md §6.7.
Sobel/Prewitt/Roberts: one shared EdgeDetector class, kernels from core.kernels,
convolution from core.convolution.apply_kernel. Canny: cv2.Canny (allowed).
"""
from __future__ import annotations

from typing import Optional

import numpy as np


class EdgeDetector:
    """Generic first-derivative edge detector, built from a pair of kernels (kx, ky).

    Sobel, Prewitt and Roberts are the same algorithm with different kernels,
    so they are three instances of this one class (no duplicated logic).
    """

    def __init__(self, name: str, kx: np.ndarray, ky: np.ndarray):
        self.name = name
        self.kx = kx
        self.ky = ky

    def detect(
        self, img: np.ndarray, implementation: str = "builtin"
    ) -> dict[str, np.ndarray]:
        """Run edge detection on the grayscale version of img.

        Returns float64 arrays (signed, NOT clipped):
            gx        — apply_kernel(gray, kx)
            gy        — apply_kernel(gray, ky)
            magnitude — sqrt(gx² + gy²)
            direction — arctan2(gy, gx), radians
        """
        raise NotImplementedError("TODO (C): implement EdgeDetector.detect()")


# TODO (C): register one EdgeDetector per operator, using the kernels from core.kernels:
#   "sobel": EdgeDetector("sobel", *sobel()), "prewitt": ..., "roberts": ...
# The /api/edges route returns 501 for a method that is not registered here yet.
DETECTORS: dict[str, EdgeDetector] = {}


def canny(
    img: np.ndarray,
    low: int = 50,
    high: int = 150,
    blur_sigma: Optional[float] = None,
) -> np.ndarray:
    """Canny edge detection on the grayscale version of img. Returns uint8 edge map.

    If blur_sigma is set, pre-blur with smooth(..., "gaussian") first,
    then call cv2.Canny(gray_uint8, low, high).
    """
    raise NotImplementedError("TODO (C): implement canny()")
