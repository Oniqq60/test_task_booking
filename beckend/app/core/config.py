from functools import lru_cache
from typing import List, Optional
from pydantic import PostgresDsn, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Production-ready application settings."""
    
    # Project
    PROJECT_NAME: str = "Apartments API"
    API_V1_STR: str = "/api/v1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelname)-8s [%(name)s] %(message)s"
    LOG_DATE_FORMAT: str = "%H:%M:%S"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    
    # File upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    
    # Database (individual fields for flexibility)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    
    # Optional direct DATABASE_URL override
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return [o.strip() for o in v.split(",") if o.strip()]
        return v
    
    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return str(self.DATABASE_URL)
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def async_database_url(self) -> str:
        url = self.sync_database_url
        if "postgresql+psycopg2://" in url:
            return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
        return url
    
    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()