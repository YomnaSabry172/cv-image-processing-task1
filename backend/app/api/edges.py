# Owner: C — POST /api/edges
"""Edge detection endpoint: Sobel, Prewitt, Roberts, Canny."""
import time
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.utils.channels import to_display
from app.core.edges import DETECTORS, canny

router = APIRouter()


class EdgesRequest(BaseModel):
    image: str
    method: str  # "sobel" | "prewitt" | "roberts" | "canny"
    implementation: str = "builtin"  # for non-Canny
    # Canny params
    low: Optional[int] = 50
    high: Optional[int] = 150
    blur_sigma: Optional[float] = None


@router.post("/edges", response_model=ProcessingResponse)
def edges(req: EdgesRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()

    if req.method == "canny":
        try:
            result = canny(img, req.low, req.high, req.blur_sigma)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        elapsed = (time.perf_counter() - t0) * 1000.0
        return ProcessingResponse(
            images={"result": encode_image(result)},
            meta={"time_ms": round(elapsed, 2)},
        )

    if req.method not in ("sobel", "prewitt", "roberts"):
        raise HTTPException(status_code=400, detail=f"Unknown edge method: {req.method}")
    if req.method not in DETECTORS:
        raise NotImplementedError(f"TODO (C): register '{req.method}' in core.edges.DETECTORS")

    detector = DETECTORS[req.method]
    raw = detector.detect(img, implementation=req.implementation)
    elapsed = (time.perf_counter() - t0) * 1000.0

    # Convert raw float64 results to displayable uint8
    return ProcessingResponse(
        images={
            "gx": encode_image(to_display(raw["gx"], mode="abs")),
            "gy": encode_image(to_display(raw["gy"], mode="abs")),
            "magnitude": encode_image(to_display(raw["magnitude"], mode="minmax")),
            "direction": encode_image(to_display(raw["direction"], mode="minmax")),
        },
        meta={"time_ms": round(elapsed, 2)},
    )
