# Owner: B — manual vs builtin convolution equality tests
"""
Tests that the manual (from-scratch) convolution produces the same
results as the built-in (SciPy) implementation for various kernels.
"""
import numpy as np
import pytest

from app.core.convolution import correlate2d_manual, correlate2d_builtin
from app.core.kernels import box, gaussian, sobel, prewitt, roberts

# B's convolution and kernels are now implemented — tests are active.


@pytest.fixture
def sample_gray():
    """Create a small test image with varied pixel values."""
    rng = np.random.default_rng(42)
    return rng.integers(0, 256, size=(64, 64), dtype=np.uint8)


def _assert_close(manual_result, builtin_result, atol=1e-10):
    """Assert two results are nearly identical."""
    diff = np.abs(manual_result - builtin_result)
    assert diff.max() < atol, f"Max difference: {diff.max()}"


class TestConvolutionEquality:
    """Manual and builtin correlation must produce the same output."""

    def test_box_3x3(self, sample_gray):
        kernel = box(3)
        m = correlate2d_manual(sample_gray, kernel)
        b = correlate2d_builtin(sample_gray, kernel)
        _assert_close(m, b)

    def test_box_5x5(self, sample_gray):
        kernel = box(5)
        m = correlate2d_manual(sample_gray, kernel)
        b = correlate2d_builtin(sample_gray, kernel)
        _assert_close(m, b)

    def test_gaussian_3x3(self, sample_gray):
        kernel = gaussian(3, 1.0)
        m = correlate2d_manual(sample_gray, kernel)
        b = correlate2d_builtin(sample_gray, kernel)
        _assert_close(m, b)

    def test_gaussian_5x5(self, sample_gray):
        kernel = gaussian(5, 1.5)
        m = correlate2d_manual(sample_gray, kernel)
        b = correlate2d_builtin(sample_gray, kernel)
        _assert_close(m, b)

    def test_sobel_kx(self, sample_gray):
        kx, _ = sobel()
        m = correlate2d_manual(sample_gray, kx)
        b = correlate2d_builtin(sample_gray, kx)
        _assert_close(m, b)

    def test_sobel_ky(self, sample_gray):
        _, ky = sobel()
        m = correlate2d_manual(sample_gray, ky)
        b = correlate2d_builtin(sample_gray, ky)
        _assert_close(m, b)

    def test_prewitt_kx(self, sample_gray):
        kx, _ = prewitt()
        m = correlate2d_manual(sample_gray, kx)
        b = correlate2d_builtin(sample_gray, kx)
        _assert_close(m, b)

    def test_roberts_kx(self, sample_gray):
        """Roberts uses 2×2 kernels — tests asymmetric padding."""
        kx, _ = roberts()
        m = correlate2d_manual(sample_gray, kx)
        b = correlate2d_builtin(sample_gray, kx)
        _assert_close(m, b)

    def test_roberts_ky(self, sample_gray):
        _, ky = roberts()
        m = correlate2d_manual(sample_gray, ky)
        b = correlate2d_builtin(sample_gray, ky)
        _assert_close(m, b)
