# Owner: D — POST /api/histogram
"""Histogram computation endpoint: returns histogram, PDF, CDF, stats."""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image
from app.core.histogram import channel_stats
from app.core.color import is_color

router = APIRouter()


class HistogramRequest(BaseModel):
    image: str


@router.post("/histogram", response_model=ProcessingResponse)
def histogram_endpoint(req: HistogramRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    stats = channel_stats(img)
    elapsed = (time.perf_counter() - t0) * 1000.0

    mode = "rgb" if is_color(img) else "gray"

    return ProcessingResponse(
        data={
            "mode": mode,
            "channels": stats,
        },
        meta={"time_ms": round(elapsed, 2)},
    )
