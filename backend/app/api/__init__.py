# Owner: Lead — API router registration (pre-wired for all features)
"""
Registers every feature router under the /api prefix.
"""
from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.images import router as images_router
from app.api.grayscale import router as grayscale_router
from app.api.noise import router as noise_router
from app.api.filters import router as filters_router
from app.api.edges import router as edges_router
from app.api.frequency import router as frequency_router
from app.api.hybrid import router as hybrid_router
from app.api.histogram import router as histogram_router
from app.api.equalize import router as equalize_router
from app.api.normalize import router as normalize_router

router = APIRouter()

router.include_router(health_router)
router.include_router(images_router)
router.include_router(grayscale_router)
router.include_router(filters_router)
router.include_router(noise_router)
router.include_router(edges_router)
router.include_router(frequency_router)
router.include_router(hybrid_router)
router.include_router(histogram_router)
router.include_router(equalize_router)
router.include_router(normalize_router)
