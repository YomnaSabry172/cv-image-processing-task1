# Owner: Lead — POST /api/images (upload once, get an id to reuse in every other endpoint)
"""Stores an uploaded image on the server so later requests can send a short id instead."""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import IMAGE_REF_PREFIX, store_image

router = APIRouter()


class StoreImageRequest(BaseModel):
    image: str


@router.post("/images", response_model=ProcessingResponse)
def upload_image(req: StoreImageRequest):
    t0 = time.perf_counter()
    try:
        image_id = store_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    elapsed = (time.perf_counter() - t0) * 1000.0
    return ProcessingResponse(
        data={"image_id": image_id, "ref": IMAGE_REF_PREFIX + image_id},
        meta={"time_ms": round(elapsed, 2)},
    )
