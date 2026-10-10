# Owner: Lead — health check endpoint
"""GET /api/health — simple health check."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}
