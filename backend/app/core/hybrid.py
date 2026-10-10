# Owner: C — hybrid image generation
"""
Hybrid images: low frequencies of image A + high frequencies of image B. See CLAUDE.md §6.10.
MUST reuse FrequencyFilter — no mask or FFT code in this file.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from app.core.frequency import FrequencyFilter


class HybridImage:
    """Combines two images: low-pass of A + high-pass of B."""

    def __init__(self, low_filter: FrequencyFilter, high_filter: FrequencyFilter):
        self.low_filter = low_filter
        self.high_filter = high_filter

    def make(self, img_a: np.ndarray, img_b: np.ndarray) -> dict[str, Any]:
        """Create a hybrid image.

        Steps:
            1. Resize B to A's size (cv2.resize).
            2. Match color mode (both gray if either is gray).
            3. low  = low_filter.apply_raw(A)["result"]   (per channel for color)
            4. high = high_filter.apply_raw(B)["result"]  (per channel for color)
            5. hybrid = clip(low + high)   — add BEFORE clipping, high is signed.

        Returns display-ready uint8 images with keys:
            hybrid, low_component, high_component
        """
        raise NotImplementedError("TODO (C): implement HybridImage.make()")
