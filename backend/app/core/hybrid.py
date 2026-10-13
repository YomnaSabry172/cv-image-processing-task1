# Owner: C — hybrid image generation
"""
Hybrid images: low frequencies of image A + high frequencies of image B. See CLAUDE.md §6.10.
MUST reuse FrequencyFilter — no mask or FFT code in this file.
"""
from __future__ import annotations

from typing import Any

import numpy as np
import cv2

from app.core.color import to_grayscale
from app.utils.channels import apply_per_channel, to_display

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
        # Match B's dimensions to A so their pixels can be added.
        h, w = img_a.shape[:2]
        if img_b.shape[:2] != (h, w):
            img_b = cv2.resize(img_b, (w, h))

        # If either input is grayscale, convert both to grayscale.
        if img_a.ndim == 2 or img_b.ndim == 2:
            img_a = to_grayscale(img_a)
            img_b = to_grayscale(img_b)

        # Keep A's broad shapes using the raw low-pass result.
        low = apply_per_channel(
            lambda channel: self.low_filter.apply_raw(channel)["result"],
            img_a,
        )

        # Keep B's details, preserving negative high-pass values.
        high = apply_per_channel(
            lambda channel: self.high_filter.apply_raw(channel)["result"],
            img_b,
        )

        # Add first, then clip and convert the final image for display.
        hybrid = np.clip(low + high, 0, 255).astype(np.uint8)

        return {
            "hybrid": hybrid,
            "low_component": np.clip(low, 0, 255).astype(np.uint8),
            "high_component": to_display(high, mode="minmax"),
        }