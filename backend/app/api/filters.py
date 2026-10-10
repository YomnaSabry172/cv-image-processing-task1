# Owner: B — POST /api/filter
"""Low-pass filtering endpoint: average, Gaussian, median.
Supports manual, builtin, and compare modes."""
import time
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ProcessingResponse
from app.utils.image_io import decode_image, encode_image
from app.core.spatial import smooth
from app.core.compare import run_both

router = APIRouter()


class FilterRequest(BaseModel):
    image: str
    method: str  # "average" | "gaussian" | "median"
    kernel_size: int = 3
    sigma: Optional[float] = 1.0
    implementation: str = "builtin"  # "manual" | "builtin" | "compare"


@router.post("/filter", response_model=ProcessingResponse)
def filter_image(req: FilterRequest):
    try:
        img = decode_image(req.image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if req.kernel_size < 1 or req.kernel_size % 2 == 0:
        raise HTTPException(status_code=400, detail="Kernel size must be a positive odd integer")

    if req.method not in ("average", "gaussian", "median"):
        raise HTTPException(status_code=400, detail=f"Unknown filter method: {req.method}")

    t0 = time.perf_counter()

    if req.implementation == "compare":
        # Run both and return comparison results
        comparison = run_both(
            lambda: smooth(img, req.method, req.kernel_size, req.sigma, implementation="manual"),
            lambda: smooth(img, req.method, req.kernel_size, req.sigma, implementation="builtin"),
        )
        elapsed = (time.perf_counter() - t0) * 1000.0

        return ProcessingResponse(
            images={
                "manual": encode_image(comparison["manual"]),
                "builtin": encode_image(comparison["builtin"]),
                "difference": encode_image(comparison["difference"]),
            },
            data={
                "time_manual_ms": comparison["time_manual_ms"],
                "time_builtin_ms": comparison["time_builtin_ms"],
                "speedup": comparison["speedup"],
                "max_abs_diff": comparison["max_abs_diff"],
            },
            meta={"time_ms": round(elapsed, 2)},
        )
    else:
        result = smooth(img, req.method, req.kernel_size, req.sigma, implementation=req.implementation)
        elapsed = (time.perf_counter() - t0) * 1000.0

        return ProcessingResponse(
            images={"result": encode_image(result)},
            meta={"time_ms": round(elapsed, 2)},
        )
