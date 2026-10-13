# Owner: C — frequency-domain filters (low-pass, high-pass)
"""
Frequency-domain filtering. See CLAUDE.md §6.9.
np.fft is allowed for fft2 / ifft2 / fftshift / ifftshift only. Masks are built FROM SCRATCH.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from app.utils.channels import to_display


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
        # Cutoff is used as a divisor, so it must be finite and positive.
        if not np.isfinite(cutoff) or cutoff <= 0:
            raise ValueError("cutoff must be a finite number greater than 0")

        # Butterworth needs a positive integer order.
        if (
            not isinstance(order, int)
            or isinstance(order, bool)
            or order < 1
        ):
            raise ValueError("order must be a positive integer")
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
                # Measure each row and column relative to the shifted FFT center.
        rows = np.arange(h, dtype=np.float64) - h // 2
        cols = np.arange(w, dtype=np.float64) - w // 2

        # Broadcasting creates the distance at every spectrum position.
        distance = np.sqrt(rows[:, None] ** 2 + cols[None, :] ** 2)

        # Construct the low-pass mask using the selected formula.
        if self.shape == "ideal":
            low_mask = (distance <= self.cutoff).astype(np.float64)

        elif self.shape == "gaussian":
            low_mask = np.exp(
                -(distance ** 2) / (2.0 * self.cutoff ** 2)
            )

        else:  # Butterworth
            low_mask = 1.0 / (
                1.0 + (distance / self.cutoff) ** (2 * self.order)
            )

        # High-pass keeps the complementary frequencies.
        if self.kind == "highpass":
            return 1.0 - low_mask

        return low_mask

    
    def apply_raw(self, img2d: np.ndarray) -> dict[str, np.ndarray]:
        """Filter one 2-D channel.

        F = fftshift(fft2(img)), G = F * mask, g = real(ifft2(ifftshift(G))).

        Returns float64 arrays:
            result            — g (unclipped, may be negative)
            spectrum          — log(1 + |F|)
            mask              — the mask
            filtered_spectrum — log(1 + |G|)
        """
         # This function processes one channel at a time.
        if img2d.ndim != 2:
            raise ValueError("apply_raw expects a 2-D image channel")

        # Floating-point arithmetic preserves signed and fractional values.
        image = img2d.astype(np.float64)

        # Convert the image into frequencies, then center zero frequency.
        spectrum = np.fft.fftshift(np.fft.fft2(image))

        # Build a mask with the same height and width as the image.
        h, w = image.shape
        mask = self.build_mask(h, w)

        # Keep or reduce each frequency according to its mask weight.
        filtered = spectrum * mask

        # Undo the shift before converting frequencies back to an image.
        result = np.real(
            np.fft.ifft2(np.fft.ifftshift(filtered))
        )

        # Log compression makes weaker frequencies visible in previews.
        return {
            "result": result,
            "spectrum": np.log1p(np.abs(spectrum)),
            "mask": mask,
            "filtered_spectrum": np.log1p(np.abs(filtered)),
        }

    def apply(self, img: np.ndarray) -> dict[str, Any]:
        """Filter a full image (gray or color, per channel).

        Returns display-ready uint8 images with keys:
            result, spectrum, mask, filtered_spectrum
        (high-pass result via to_display(mode="offset") or "minmax"; spectra via min-max).
        """
        if img.ndim == 2:
            # Grayscale contains one channel, so filter it directly.
            raw = self.apply_raw(img)

        elif img.ndim == 3 and img.shape[2] == 3:
            # Filter R, G, and B separately to avoid mixing their colours.
            channels = [
                self.apply_raw(img[:, :, c])
                for c in range(3)
            ]

            # Combine each type of output into an RGB image.
            raw = {
                key: np.stack(
                    [channel[key] for channel in channels],
                    axis=-1,
                )
                for key in ("result", "spectrum", "filtered_spectrum")
            }

            # The mask depends on image size, so all channels share it.
            raw["mask"] = channels[0]["mask"]

        else:
            raise ValueError("Expected a grayscale or RGB image")

        # Low-pass preserves brightness; high-pass needs signed display.
        if self.kind == "lowpass":
            result = np.clip(raw["result"], 0, 255).astype(np.uint8)
        else:
            result = to_display(raw["result"], mode="offset")

        return {
            "result": result,
            "spectrum": to_display(raw["spectrum"], mode="minmax"),
            "mask": (raw["mask"] * 255).astype(np.uint8),
            "filtered_spectrum": to_display(
                raw["filtered_spectrum"], mode="minmax"
            ),
        }
