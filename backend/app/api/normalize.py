# Owner: D — POST /api/normalize
"""Min-max normalization endpoint."""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.histogram import normalize_minmax, channel_stats

router = APIRouter()


class NormalizeRequest(BaseModel):
    image: str


@router.post("/normalize", response_model=ProcessingResponse)
def normalize_endpoint(req: NormalizeRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    before_stats = channel_stats(img)
    result = normalize_minmax(img)
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
