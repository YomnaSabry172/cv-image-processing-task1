# Owner: Lead — upload-once image store: ids must give the same results as sending the full image
import numpy as np
from fastapi.testclient import TestClient

from app.main import app
from app.utils import image_io
from app.utils.image_io import IMAGE_REF_PREFIX, decode_image, encode_image, store_image

client = TestClient(app)


def _data_url(seed, shape=(40, 50, 3)):
    return encode_image(np.random.default_rng(seed).integers(0, 256, shape, dtype=np.uint8))


def test_upload_returns_reference_and_same_id_for_same_image():
    url = _data_url(1)
    first = client.post("/api/images", json={"image": url}).json()["data"]
    second = client.post("/api/images", json={"image": url}).json()["data"]
    assert first["ref"] == IMAGE_REF_PREFIX + first["image_id"]
    assert first["image_id"] == second["image_id"]


def test_reference_gives_same_result_as_full_image():
    url = _data_url(2)
    ref = client.post("/api/images", json={"image": url}).json()["data"]["ref"]
    body = {"kind": "lowpass", "shape": "gaussian", "cutoff": 8}
    by_url = client.post("/api/frequency", json={"image": url, **body}).json()
    by_ref = client.post("/api/frequency", json={"image": ref, **body}).json()
    assert by_ref["images"] == by_url["images"]


def test_hybrid_accepts_two_references():
    ref_a = client.post("/api/images", json={"image": _data_url(3)}).json()["data"]["ref"]
    ref_b = client.post("/api/images", json={"image": _data_url(4)}).json()["data"]["ref"]
    res = client.post("/api/hybrid", json={"image_a": ref_a, "image_b": ref_b, "low_cutoff": 5, "high_cutoff": 10})
    assert res.status_code == 200
    assert set(res.json()["images"]) == {"hybrid", "low_component", "high_component"}


def test_unknown_reference_is_410_on_every_kind_of_route():
    bad = IMAGE_REF_PREFIX + "does-not-exist"
    assert client.post("/api/grayscale", json={"image": bad}).status_code == 410
    assert client.post("/api/hybrid", json={"image_a": bad, "image_b": bad}).status_code == 410


def test_bad_upload_is_400():
    assert client.post("/api/images", json={"image": "data:image/png;base64,"}).status_code == 400


def test_stored_image_cannot_be_damaged_by_a_route():
    image_id = store_image(_data_url(5))
    img = decode_image(IMAGE_REF_PREFIX + image_id)
    img[:] = 0  # a route changing its input in place
    assert decode_image(IMAGE_REF_PREFIX + image_id).any()


def test_store_is_bounded():
    for seed in range(200, 200 + image_io._STORE_SIZE + 5):
        store_image(_data_url(seed, (8, 8, 3)))
    assert len(image_io._store) == image_io._STORE_SIZE
