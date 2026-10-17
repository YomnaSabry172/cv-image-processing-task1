# Owner: D — tests for histogram, CDF, equalization, normalization
import numpy as np
import pytest

from app.core.histogram import (
    cdf, channel_stats, equalize, histogram, normalize_minmax, pdf,
)


@pytest.fixture
def gray():
    return np.random.default_rng(1).integers(40, 120, size=(80, 90), dtype=np.uint8)


@pytest.fixture
def rgb():
    return np.random.default_rng(2).integers(0, 256, size=(50, 60, 3), dtype=np.uint8)


def test_histogram_matches_numpy(gray):
    expected = np.histogram(gray, bins=256, range=(0, 256))[0]
    assert np.array_equal(histogram(gray), expected)


def test_pdf_sums_to_one_and_cdf_ends_at_one(gray):
    p = pdf(histogram(gray))
    assert p.sum() == pytest.approx(1.0)
    c = cdf(p)
    assert c[-1] == pytest.approx(1.0)
    assert np.all(np.diff(c) >= 0)  # CDF never decreases


def test_equalize_gray_keeps_shape_dtype_and_widens_range(gray):
    out = equalize(gray)
    assert out.shape == gray.shape and out.dtype == np.uint8
    assert int(out.max()) - int(out.min()) > int(gray.max()) - int(gray.min())
    assert out.max() == 255


def test_equalize_rgb_shape(rgb):
    out = equalize(rgb)
    assert out.shape == rgb.shape and out.dtype == np.uint8


def test_equalize_constant_image_does_not_crash():
    out = equalize(np.full((10, 10), 77, dtype=np.uint8))
    assert out.shape == (10, 10)


def test_normalize_stretches_to_full_range(gray):
    out = normalize_minmax(gray)
    assert out.min() == 0 and out.max() == 255


def test_normalize_constant_and_signed():
    assert np.all(normalize_minmax(np.full((4, 4), 9.0)) == 0)
    out = normalize_minmax(np.array([[-5.0, 0.0, 5.0]]))
    assert out.tolist() == [[0, 128, 255]]


def test_channel_stats_keys(gray, rgb):
    assert list(channel_stats(gray)) == ["gray"]
    s = channel_stats(rgb)
    assert list(s) == ["r", "g", "b"]
    for key in ("hist", "pdf", "cdf", "min", "max", "mean", "std"):
        assert key in s["r"]
    assert len(s["r"]["hist"]) == 256 and sum(s["r"]["hist"]) == 50 * 60