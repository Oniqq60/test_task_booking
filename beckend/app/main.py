import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.middleware.logging import RequestLoggingMiddleware
from app.api.v1 import apartments, bookings, photos
from app.db.session import engine
from app.models.base import Base

setup_logging()
logger = logging.getLogger("app.main")

UPLOAD_PATH = Path(settings.UPLOAD_DIR)
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_PATH)), name="uploads")

app.include_router(apartments.router, prefix=f"{settings.API_V1_STR}/apartments", tags=["apartments"])
app.include_router(bookings.router, prefix=f"{settings.API_V1_STR}/bookings", tags=["bookings"])
app.include_router(photos.router, prefix=f"{settings.API_V1_STR}/photos", tags=["photos"])


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    logger.info("🚀 Application starting...")


@app.on_event("shutdown")
def on_shutdown():
    logger.info("👋 Application shutting down...")