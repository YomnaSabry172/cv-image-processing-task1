# Test suite for Member B features: Noise and Filters
import numpy as np
import pytest

from app.core.noise import UniformNoise, GaussianNoise, SaltPepperNoise, make_noise
from app.core.spatial import smooth
from app.core.compare import run_both
from app.core.kernels import box, gaussian, laplacian


@pytest.fixture
def gray_image():
    rng = np.random.default_rng(123)
    return rng.integers(0, 256, size=(64, 64), dtype=np.uint8)


@pytest.fixture
def rgb_image():
    rng = np.random.default_rng(456)
    return rng.integers(0, 256, size=(64, 64, 3), dtype=np.uint8)


class TestNoise:
    def test_uniform_noise_gray(self, gray_image):
        noise = UniformNoise(low=-20, high=20, seed=1)
        res = noise.apply(gray_image)
        assert res.shape == gray_image.shape
        assert res.dtype == np.uint8
        assert not np.array_equal(res, gray_image)

    def test_uniform_noise_rgb(self, rgb_image):
        noise = UniformNoise(low=-20, high=20, seed=1)
        res = noise.apply(rgb_image)
        assert res.shape == rgb_image.shape
        assert res.dtype == np.uint8
        assert not np.array_equal(res, rgb_image)

    def test_gaussian_noise(self, gray_image, rgb_image):
        noise = GaussianNoise(mean=0, sigma=15, seed=2)
        res_gray = noise.apply(gray_image)
        assert res_gray.shape == gray_image.shape
        assert res_gray.dtype == np.uint8

        res_rgb = noise.apply(rgb_image)
        assert res_rgb.shape == rgb_image.shape
        assert res_rgb.dtype == np.uint8

    def test_salt_pepper_noise_scratch(self, gray_image, rgb_image):
        noise = SaltPepperNoise(density=0.1, salt_ratio=0.5, seed=3)
        res_gray = noise.apply(gray_image)
        assert res_gray.shape == gray_image.shape
        assert res_gray.dtype == np.uint8

        # In RGB, same pixels should be corrupted across channels
        noise_rgb = SaltPepperNoise(density=0.2, salt_ratio=0.5, seed=4)
        res_rgb = noise_rgb.apply(rgb_image)
        assert res_rgb.shape == rgb_image.shape
        assert res_rgb.dtype == np.uint8

        # Check that corrupted pixels are pure black (0,0,0) or pure white (255,255,255)
        # everywhere they were modified
        diff = np.any(res_rgb != rgb_image, axis=-1)
        corrupted_pixels = res_rgb[diff]
        # For each corrupted pixel, all 3 channels should be 0 or all 3 should be 255
        is_pure_salt = np.all(corrupted_pixels == 255, axis=-1)
        is_pure_pepper = np.all(corrupted_pixels == 0, axis=-1)
        assert np.all(is_pure_salt | is_pure_pepper)

    def test_salt_pepper_validation(self):
        with pytest.raises(ValueError):
            SaltPepperNoise(density=-0.1)
        with pytest.raises(ValueError):
            SaltPepperNoise(density=1.5)
        with pytest.raises(ValueError):
            SaltPepperNoise(salt_ratio=-0.1)
        with pytest.raises(ValueError):
            SaltPepperNoise(salt_ratio=1.1)

    def test_make_noise_factory(self):
        u = make_noise("uniform", low=-10, high=10)
        assert isinstance(u, UniformNoise)
        g = make_noise("gaussian", mean=0, sigma=10)
        assert isinstance(g, GaussianNoise)
        sp = make_noise("salt_pepper", density=0.05, salt_ratio=0.5)
        assert isinstance(sp, SaltPepperNoise)
        with pytest.raises(ValueError):
            make_noise("unknown_noise")


class TestSpatialFilters:
    def test_box_kernel(self):
        k3 = box(3)
        assert k3.shape == (3, 3)
        assert np.isclose(k3.sum(), 1.0)
        assert np.allclose(k3, 1.0 / 9.0)

        with pytest.raises(ValueError):
            box(2)  # Even
        with pytest.raises(ValueError):
            box(-1)

    def test_laplacian_kernel(self):
        lap = laplacian()
        assert lap.shape == (3, 3)
        assert lap.sum() == 0.0

    @pytest.mark.parametrize("method", ["average", "gaussian", "median"])
    def test_smooth_gray(self, gray_image, method):
        res_manual = smooth(gray_image, method, k=3, implementation="manual")
        res_builtin = smooth(gray_image, method, k=3, implementation="builtin")
        assert res_manual.shape == gray_image.shape
        assert res_builtin.shape == gray_image.shape
        assert res_manual.dtype == np.uint8
        assert res_builtin.dtype == np.uint8

        # Max difference should be small (within rounding error)
        max_diff = np.abs(res_manual.astype(int) - res_builtin.astype(int)).max()
        assert max_diff <= 1

    @pytest.mark.parametrize("method", ["average", "gaussian", "median"])
    def test_smooth_rgb(self, rgb_image, method):
        res_manual = smooth(rgb_image, method, k=3, implementation="manual")
        res_builtin = smooth(rgb_image, method, k=3, implementation="builtin")
        assert res_manual.shape == rgb_image.shape
        assert res_builtin.shape == rgb_image.shape
        assert res_manual.dtype == np.uint8
        assert res_builtin.dtype == np.uint8

        max_diff = np.abs(res_manual.astype(int) - res_builtin.astype(int)).max()
        assert max_diff <= 1

    def test_smooth_invalid(self, gray_image):
        with pytest.raises(ValueError):
            smooth(gray_image, "invalid_method")
        with pytest.raises(ValueError):
            smooth(gray_image, "average", k=4)  # even k
        with pytest.raises(ValueError):
            smooth(gray_image, "average", k=3, implementation="invalid")

    def test_run_both(self, gray_image):
        comp = run_both(
            lambda: smooth(gray_image, "average", k=3, implementation="manual"),
            lambda: smooth(gray_image, "average", k=3, implementation="builtin"),
        )
        assert "manual" in comp
        assert "builtin" in comp
        assert "difference" in comp
        assert "time_manual_ms" in comp
        assert "time_builtin_ms" in comp
        assert "speedup" in comp
        assert "max_abs_diff" in comp
        assert comp["difference"].dtype == np.uint8
        assert comp["max_abs_diff"] <= 1.0
