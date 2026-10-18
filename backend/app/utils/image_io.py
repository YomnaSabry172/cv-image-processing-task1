# Owner: Lead — image I/O: base64 <-> numpy, BGR<->RGB, downscale
"""
Handles conversion between base64 data-URLs and NumPy arrays.
All images inside the codebase are RGB (H×W×3) or grayscale (H×W).
BGR↔RGB conversion happens ONLY here.
"""
from __future__ import annotations

import base64
import re

import cv2
import numpy as np

MAX_SIDE = 1024  # longest side after downscale


def decode_image(data_url: str) -> np.ndarray:
    """Convert a base64 data-URL to a uint8 NumPy array (RGB or gray).

    Steps:
        1. Strip the data-URL header.
        2. Decode from base64 to bytes.
        3. Use cv2.imdecode (reads as BGR).
        4. Convert BGR → RGB exactly once.
        5. Downscale if the longest side exceeds MAX_SIDE.
        6. If all three channels are identical, return 2-D grayscale.
    """
    # Strip data-URL prefix (e.g. "data:image/png;base64,")
    header_match = re.match(r"data:[^;]+;base64,", data_url)
    if header_match:
        data_url = data_url[header_match.end():]

    raw = base64.b64decode(data_url)
    # Reject empty data before passing it to OpenCV.
    if not raw:
        raise ValueError("Image data is empty. Please upload a valid image.")
    buf = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)  # always BGR, 3-channel
    if img is None:
        raise ValueError("Could not decode image — invalid or unsupported format.")

    # BGR → RGB (the only place this conversion happens)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Downscale if too large
    h, w = img.shape[:2]
    longest = max(h, w)
    if longest > MAX_SIDE:
        scale = MAX_SIDE / longest
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Detect grayscale: if R == G == B for every pixel, return 2-D
    if img.ndim == 3 and np.array_equal(img[:, :, 0], img[:, :, 1]) and np.array_equal(img[:, :, 1], img[:, :, 2]):
        img = img[:, :, 0]

    return img


def encode_image(img: np.ndarray) -> str:
    """Convert a uint8 NumPy array (RGB or gray) to a base64 data-URL string.

    Steps:
        1. Ensure uint8.
        2. If 3-channel (RGB), convert to BGR for cv2.imencode.
        3. Encode to PNG bytes.
        4. Wrap in a data-URL.
    """
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)

    if img.ndim == 3:
        # RGB → BGR for OpenCV encoding
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    success, buf = cv2.imencode(".png", img)
    if not success:
        raise RuntimeError("Failed to encode image to PNG.")

    b64 = base64.b64encode(buf.tobytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"
