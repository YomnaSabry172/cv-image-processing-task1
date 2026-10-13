# Owner: C — edge detection (Sobel, Prewitt, Roberts from scratch + Canny via cv2)
"""
Edge detection using first-derivative operators. See CLAUDE.md §6.7.
Sobel/Prewitt/Roberts: one shared EdgeDetector class, kernels from core.kernels,
convolution from core.convolution.apply_kernel. Canny: cv2.Canny (allowed).
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import cv2

from app.core.spatial import smooth
from app.core.color import to_grayscale
from app.core.convolution import apply_kernel
from app.core.kernels import sobel, prewitt, roberts


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
                # Edges are calculated from brightness, so use grayscale.
        gray = to_grayscale(img)

        # Measure brightness changes using the two kernels.
        gx = apply_kernel(gray, self.kx, implementation=implementation)
        gy = apply_kernel(gray, self.ky, implementation=implementation)

        # Combine both responses into an edge-strength image.
        magnitude = np.sqrt(gx ** 2 + gy ** 2)

        # Calculate the gradient angle in radians, preserving signs.
        direction = np.arctan2(gy, gx)

        return {
            "gx": gx,
            "gy": gy,
            "magnitude": magnitude,
            "direction": direction,
        }


# TODO (C): register one EdgeDetector per operator, using the kernels from core.kernels:
#   "sobel": EdgeDetector("sobel", *sobel()), "prewitt": ..., "roberts": ...
# The /api/edges route returns 501 for a method that is not registered here yet.
DETECTORS: dict[str, EdgeDetector] = {
    "sobel": EdgeDetector("sobel", *sobel()),
    "prewitt": EdgeDetector("prewitt", *prewitt()),
    "roberts": EdgeDetector("roberts", *roberts()),
}


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
    if low is None or high is None or not (0 <= low <= high):
        raise ValueError("Thresholds must satisfy 0 <= low <= high")

    # Canny operates on a single-channel uint8 image.
    gray = to_grayscale(img)

    if blur_sigma is not None:
        if not np.isfinite(blur_sigma) or blur_sigma <= 0:
            raise ValueError("blur_sigma must be finite and greater than 0")

        # Cover roughly three standard deviations on each side.
        radius = int(np.ceil(3.0 * blur_sigma))
        kernel_size = 2 * radius + 1

        # Reduce noise before detecting edges.
        gray = smooth(
            gray,
            method="gaussian",
            k=kernel_size,
            sigma=blur_sigma,
            implementation="builtin",
        )

    return cv2.Canny(gray.astype(np.uint8), low, high)
