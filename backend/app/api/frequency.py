# Owner: C — POST /api/frequency
"""Frequency-domain filtering endpoint."""
import time
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.frequency import FrequencyFilter

router = APIRouter()


class FrequencyRequest(BaseModel):
    image: str
    kind: str = "lowpass"  # "lowpass" | "highpass"
    shape: str = "ideal"  # "ideal" | "gaussian" | "butterworth"
    cutoff: float = 30.0
    order: Optional[int] = 2


@router.post("/frequency", response_model=ProcessingResponse)
def frequency(req: FrequencyRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        filt = FrequencyFilter(
            kind=req.kind, shape=req.shape, cutoff=req.cutoff, order=req.order
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    result = filt.apply(img)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return ProcessingResponse(
        images={
            "result": encode_image(result["result"]),
            "spectrum": encode_image(result["spectrum"]),
            "mask": encode_image(result["mask"]),
            "filtered_spectrum": encode_image(result["filtered_spectrum"]),
        },
        meta={"time_ms": round(elapsed, 2)},
    )
