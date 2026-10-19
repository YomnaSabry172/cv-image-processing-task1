# Owner: Lead — FastAPI application entry point, CORS, router registration
"""
CV Task 1: Image Processing Web App — main application.
"""
import re

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import router as api_router
from app.utils.image_io import UnknownImageError

app = FastAPI(
    title="CV Task 1 — Image Processing",
    description="University Computer Vision assignment: classic image-processing operations.",
    version="1.0.0",
)

# CORS — allow the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.exception_handler(UnknownImageError)
async def unknown_image_handler(request: Request, exc: UnknownImageError):
    """Any route got an image id the server no longer has. 410 tells the frontend to upload again."""
    return JSONResponse(status_code=410, content={"detail": str(exc)})


@app.exception_handler(NotImplementedError)
async def not_implemented_handler(request: Request, exc: NotImplementedError):
    """Placeholders raise NotImplementedError("TODO (<role>): <what>").
    Turn that into 501 so the frontend can show its "Not implemented yet" card."""
    message = str(exc)
    match = re.match(r"TODO \((\w+)\):\s*(.*)", message)
    if match:
        detail = f"Not implemented yet (owner: {match.group(1)}): {match.group(2)}"
    else:
        detail = f"Not implemented yet: {message}"
    return JSONResponse(status_code=501, content={"detail": detail})
