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
        raise NotImplementedError("TODO (B): implement Noise.apply()")

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
        raise NotImplementedError("TODO (B): implement UniformNoise._corrupt()")


class GaussianNoise(Noise):
    """Additive Gaussian noise with given mean and sigma."""

    def __init__(self, mean: float = 0, sigma: float = 25, seed: Optional[int] = None):
        super().__init__(seed)
        self.mean = mean
        self.sigma = sigma

    def _corrupt(self, img: np.ndarray) -> np.ndarray:
        raise NotImplementedError("TODO (B): implement GaussianNoise._corrupt()")


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
        self.density = density
        self.salt_ratio = salt_ratio

    def _corrupt(self, img: np.ndarray) -> np.ndarray:
        raise NotImplementedError("TODO (B): implement SaltPepperNoise._corrupt() from scratch")


def make_noise(noise_type: str, **params) -> Noise:
    """Factory: "uniform" | "gaussian" | "salt_pepper" → Noise instance.

    Raise ValueError for an unknown type.
    """
    raise NotImplementedError("TODO (B): implement make_noise()")
