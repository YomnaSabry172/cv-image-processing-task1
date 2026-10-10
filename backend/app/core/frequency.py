# Owner: C — frequency-domain filters (low-pass, high-pass)
"""
Frequency-domain filtering. See CLAUDE.md §6.9.
np.fft is allowed for fft2 / ifft2 / fftshift / ifftshift only. Masks are built FROM SCRATCH.
"""
from __future__ import annotations

from typing import Any

import numpy as np


class FrequencyFilter:
    """Frequency-domain filter.

    kind:   "lowpass" or "highpass"
    shape:  "ideal", "gaussian", or "butterworth"
    cutoff: D0 — cutoff distance from the spectrum center
    order:  n — Butterworth order (Butterworth only)
    """

    def __init__(
        self,
        kind: str = "lowpass",
        shape: str = "ideal",
        cutoff: float = 30.0,
        order: int = 2,
    ):
        if kind not in ("lowpass", "highpass"):
            raise ValueError(f"kind must be 'lowpass' or 'highpass', got {kind!r}")
        if shape not in ("ideal", "gaussian", "butterworth"):
            raise ValueError(f"shape must be 'ideal', 'gaussian', or 'butterworth', got {shape!r}")
        self.kind = kind
        self.shape = shape
        self.cutoff = cutoff
        self.order = order

    def build_mask(self, h: int, w: int) -> np.ndarray:
        """Build the h×w frequency mask (float64). FROM SCRATCH.

        D(u,v) = distance from the spectrum center.
            Ideal LP:       1 where D ≤ D0, else 0
            Gaussian LP:    exp(-D² / (2·D0²))
            Butterworth LP: 1 / (1 + (D/D0)^(2n))
            HP = 1 − LP
        """
        raise NotImplementedError("TODO (C): implement FrequencyFilter.build_mask()")

    def apply_raw(self, img2d: np.ndarray) -> dict[str, np.ndarray]:
        """Filter one 2-D channel.

        F = fftshift(fft2(img)), G = F * mask, g = real(ifft2(ifftshift(G))).

        Returns float64 arrays:
            result            — g (unclipped, may be negative)
            spectrum          — log(1 + |F|)
            mask              — the mask
            filtered_spectrum — log(1 + |G|)
        """
        raise NotImplementedError("TODO (C): implement FrequencyFilter.apply_raw()")

    def apply(self, img: np.ndarray) -> dict[str, Any]:
        """Filter a full image (gray or color, per channel).

        Returns display-ready uint8 images with keys:
            result, spectrum, mask, filtered_spectrum
        (high-pass result via to_display(mode="offset") or "minmax"; spectra via min-max).
        """
        raise NotImplementedError("TODO (C): implement FrequencyFilter.apply()")
