# Owner: D — POST /api/equalize
"""Histogram equalization endpoint."""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.histogram import equalize, channel_stats

router = APIRouter()


class EqualizeRequest(BaseModel):
    image: str


@router.post("/equalize", response_model=ProcessingResponse)
def equalize_endpoint(req: EqualizeRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    before_stats = channel_stats(img)
    result = equalize(img)
    after_stats = channel_stats(result)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return ProcessingResponse(
        images={"result": encode_image(result)},
        data={
            "before": before_stats,
            "after": after_stats,
        },
        meta={"time_ms": round(elapsed, 2)},
    )
