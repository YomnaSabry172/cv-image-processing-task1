# Owner: B — noise generation (uniform, Gaussian, salt & pepper)
"""
Noise generators. See CLAUDE.md §6.5.
Uniform & Gaussian: library random is allowed. Salt & pepper: FROM SCRATCH.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class Noise(ABC):
    """Base class for noise generators.

    Template method: apply() converts to float64, calls _corrupt(),
    then clips to [0, 255] and returns uint8.
    """

    def __init__(self, seed: Optional[int] = None):
        # Optional seed so results are reproducible
        self._rng = np.random.default_rng(seed)

    def apply(self, img: np.ndarray) -> np.ndarray:
        """Apply noise to an image (gray or RGB uint8). Returns uint8."""
        # Work in float64 to avoid uint8 overflow/wrap-around.
        floating = img.astype(np.float64)
        # Delegate the actual corruption to the subclass.
        corrupted = self._corrupt(floating)
        # Clamp back to valid pixel range and return as uint8.
        return np.clip(corrupted, 0, 255).astype(np.uint8)

    @abstractmethod
    def _corrupt(self, img: np.ndarray) -> np.ndarray:
        """Corrupt a float64 image. Subclasses implement this."""
        ...


class UniformNoise(Noise):
    """Additive uniform noise: adds a value from U(low, high) to every pixel."""

    def __init__(self, low: float = -50, high: float = 50, seed: Optional[int] = None):
        super().__init__(seed)
        self.low = low
        self.high = high

    def _corrupt(self, img: np.ndarray) -> np.ndarray:
        # Generate a noise array matching the image shape, drawn from U(low, high).
        noise = self._rng.uniform(self.low, self.high, size=img.shape)
        return img + noise


class GaussianNoise(Noise):
    """Additive Gaussian noise with given mean and sigma."""

    def __init__(self, mean: float = 0, sigma: float = 25, seed: Optional[int] = None):
        super().__init__(seed)
        self.mean = mean
        self.sigma = sigma

    def _corrupt(self, img: np.ndarray) -> np.ndarray:
        # Generate normally distributed noise matching the image shape.
        noise = self._rng.normal(self.mean, self.sigma, size=img.shape)
        return img + noise


class SaltPepperNoise(Noise):
    """Salt & pepper noise — FROM SCRATCH.

    density:    fraction of pixels to corrupt, in [0, 1].
    salt_ratio: share of corrupted pixels set to 255 (salt); the rest are set to 0 (pepper).
    For color images, the same pixel position is corrupted in all channels.
    Raise ValueError if density or salt_ratio is outside [0, 1].
    """

    def __init__(
        self,
        density: float = 0.05,
        salt_ratio: float = 0.5,
        seed: Optional[int] = None,
    ):
        super().__init__(seed)
        if not (0 <= density <= 1):
            raise ValueError("density must be in [0, 1]")
        if not (0 <= salt_ratio <= 1):
            raise ValueError("salt_ratio must be in [0, 1]")
        self.density = density
        self.salt_ratio = salt_ratio

    def _corrupt(self, img: np.ndarray) -> np.ndarray:
        # Make a copy so we don't modify the original float64 image.
        out = img.copy()

        # Determine spatial dimensions (H, W) regardless of color or gray.
        if img.ndim == 2:
            h, w = img.shape
        else:
            h, w = img.shape[:2]

        # One random value per pixel POSITION so the same position is
        # corrupted across all channels in a color image.
        mask = self._rng.random((h, w))

        # Threshold for salt: pixels with mask < density * salt_ratio → 255.
        salt_thresh = self.density * self.salt_ratio
        # Threshold for pepper: pixels with mask < density but ≥ salt_thresh → 0.
        pepper_thresh = self.density

        salt_mask = mask < salt_thresh
        pepper_mask = (mask >= salt_thresh) & (mask < pepper_thresh)

        if img.ndim == 2:
            out[salt_mask] = 255.0
            out[pepper_mask] = 0.0
        else:
            # Apply the same spatial mask to every channel.
            out[salt_mask, :] = 255.0
            out[pepper_mask, :] = 0.0

        return out


def make_noise(noise_type: str, **params) -> Noise:
    """Factory: "uniform" | "gaussian" | "salt_pepper" → Noise instance.

    Raise ValueError for an unknown type.
    """
    factories = {
        "uniform": UniformNoise,
        "gaussian": GaussianNoise,
        "salt_pepper": SaltPepperNoise,
    }
    if noise_type not in factories:
        raise ValueError(f"Unknown noise type: {noise_type!r}")
    return factories[noise_type](**params)
