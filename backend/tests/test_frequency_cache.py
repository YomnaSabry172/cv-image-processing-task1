# Owner: C — the forward-FFT cache must give the same answers as computing from scratch
import numpy as np

from app.core import frequency
from app.core.frequency import FrequencyFilter, centered_spectrum


def _fresh_spectrum(img2d):
    return np.fft.fftshift(np.fft.fft2(img2d.astype(np.float64)))


def _image(seed, shape=(64, 80)):
    return np.random.default_rng(seed).integers(0, 256, shape, dtype=np.uint8)


def test_same_image_reuses_spectrum():
    img = _image(1)
    assert centered_spectrum(img) is centered_spectrum(img.copy())


def test_changed_image_gets_new_spectrum():
    img = _image(2)
    first = centered_spectrum(img)
    img[10, 10] ^= 1  # change a single pixel
    second = centered_spectrum(img)
    assert second is not first
    np.testing.assert_array_equal(second, _fresh_spectrum(img))


def test_cutoff_changes_match_uncached_math():
    img = _image(3)
    for cutoff in (5.0, 12.0, 30.0):
        filt = FrequencyFilter("highpass", "butterworth", cutoff, order=3)
        out = filt.apply_raw(img)  # second+ iterations hit the cache
        expected = np.real(
            np.fft.ifft2(np.fft.ifftshift(_fresh_spectrum(img) * filt.build_mask(*img.shape)))
        )
        np.testing.assert_array_equal(out["result"], expected)


def test_rgb_channels_do_not_mix():
    img = np.stack([_image(4), _image(5), _image(6)], axis=-1)
    out = FrequencyFilter("lowpass", "gaussian", 10.0).apply(img)
    again = FrequencyFilter("lowpass", "gaussian", 10.0).apply(img)
    for key in out:
        np.testing.assert_array_equal(out[key], again[key])
    np.testing.assert_array_equal(centered_spectrum(img[:, :, 1]), _fresh_spectrum(img[:, :, 1]))


def test_cache_is_bounded_and_read_only():
    for seed in range(100, 100 + frequency._SPECTRUM_CACHE_SIZE + 5):
        spec = centered_spectrum(_image(seed, (16, 16)))
    assert len(frequency._spectrum_cache) == frequency._SPECTRUM_CACHE_SIZE
    assert not spec.flags.writeable
