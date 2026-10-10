# Owner: Lead — shared Pydantic request/response models
"""
Shared schema definitions used across multiple routes.
"""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel


class ProcessingResponse(BaseModel):
    """Unified response envelope for all image-processing endpoints."""
    images: dict[str, str] = {}
    data: dict[str, Any] = {}
    meta: dict[str, Any] = {}
