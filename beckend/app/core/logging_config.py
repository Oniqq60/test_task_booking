import logging
import sys
from app.core.config import settings


def setup_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    log_format = getattr(settings, "LOG_FORMAT", "%(levelname)-8s [%(name)s] %(message)s")
    date_format = getattr(settings, "LOG_DATE_FORMAT", "%H:%M:%S")
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)