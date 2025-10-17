"""Application configuration."""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Basic settings
    PROJECT_NAME: str = "Mars Landing Backend"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: str = "development"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    # Security settings
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Get allowed hosts as a list."""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]
    
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "marslanding"
    MONGODB_MAX_CONNECTIONS: int = 10
    MONGODB_MIN_CONNECTIONS: int = 1
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10
    
    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Email settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = "Mars Landing"
    
    # Monitoring settings
    ENABLE_METRICS: bool = True
    SENTRY_DSN: Optional[HttpUrl] = None
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Cache settings
    CACHE_TTL: int = 300  # 5 minutes
    CACHE_ENABLED: bool = True
    
    # Testing settings
    TESTING: bool = False
    TEST_DATABASE_URL: str = "mongodb://localhost:27017/marslanding_test"
    
    class Config:
        """Pydantic config."""
        
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
