# Owner: C — POST /api/hybrid
"""Hybrid image generation endpoint."""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.frequency import FrequencyFilter
from app.core.hybrid import HybridImage

router = APIRouter()


class HybridRequest(BaseModel):
    image_a: str
    image_b: str
    low_cutoff: float = 30.0
    high_cutoff: float = 30.0
    shape: str = "gaussian"  # "ideal" | "gaussian" | "butterworth"


@router.post("/hybrid", response_model=ProcessingResponse)
def hybrid(req: HybridRequest):
    try:
        img_a = decode_image(req.image_a)
        img_b = decode_image(req.image_b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        low_filter = FrequencyFilter(kind="lowpass", shape=req.shape, cutoff=req.low_cutoff)
        high_filter = FrequencyFilter(kind="highpass", shape=req.shape, cutoff=req.high_cutoff)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    hybrid_gen = HybridImage(low_filter, high_filter)
    result = hybrid_gen.make(img_a, img_b)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return ProcessingResponse(
        images={
            "hybrid": encode_image(result["hybrid"]),
            "low_component": encode_image(result["low_component"]),
            "high_component": encode_image(result["high_component"]),
        },
        meta={"time_ms": round(elapsed, 2)},
    )
