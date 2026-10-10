# Owner: Lead — POST /api/grayscale
"""Grayscale conversion endpoint — the reference example for all features."""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.color import to_grayscale

router = APIRouter()


class GrayscaleRequest(BaseModel):
    image: str


@router.post("/grayscale", response_model=ProcessingResponse)
def grayscale(req: GrayscaleRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    result = to_grayscale(img)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return ProcessingResponse(
        images={"result": encode_image(result)},
        meta={"time_ms": round(elapsed, 2)},
    )
