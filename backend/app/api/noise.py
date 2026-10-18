# Owner: B — POST /api/noise
"""Noise generation endpoint: uniform, Gaussian, salt & pepper."""
import time
from typing import Optional
import math

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.noise import make_noise

router = APIRouter()


class NoiseRequest(BaseModel):
    image: str
    type: str  # "uniform" | "gaussian" | "salt_pepper"
    # Uniform params
    low: Optional[float] = -50
    high: Optional[float] = 50
    # Gaussian params
    mean: Optional[float] = 0
    sigma: Optional[float] = 25
    # Salt & pepper params
    density: Optional[float] = 0.05
    salt_ratio: Optional[float] = 0.5
    # Reproducibility
    seed: Optional[int] = None


@router.post("/noise", response_model=ProcessingResponse)
def noise(req: NoiseRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if req.type == "uniform":
        if (
                req.low is None
                or req.high is None
                or not math.isfinite(req.low)
                or not math.isfinite(req.high)
                or req.low > req.high
            ):
            raise HTTPException(
                    status_code=400,
                    detail="Uniform noise requires finite low <= high",
                )

    elif req.type == "gaussian":
        if (
                req.mean is None
                or req.sigma is None
                or not math.isfinite(req.mean)
                or not math.isfinite(req.sigma)
                or req.sigma < 0
            ):
         raise HTTPException(
                    status_code=400,
                    detail="Gaussian noise requires a finite mean and finite sigma >= 0",
                )

    # Build params for the specific noise type
    params: dict = {}
    if req.seed is not None:
        params["seed"] = req.seed

    if req.type == "uniform":
        params["low"] = req.low
        params["high"] = req.high
    elif req.type == "gaussian":
        params["mean"] = req.mean
        params["sigma"] = req.sigma
    elif req.type == "salt_pepper":
        params["density"] = req.density
        params["salt_ratio"] = req.salt_ratio
    else:
        raise HTTPException(status_code=400, detail=f"Unknown noise type: {req.type}")

    try:
        gen = make_noise(req.type, **params)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    t0 = time.perf_counter()
    result = gen.apply(img)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return ProcessingResponse(
        images={"result": encode_image(result)},
        meta={"time_ms": round(elapsed, 2)},
    )
