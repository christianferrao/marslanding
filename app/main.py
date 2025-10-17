"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.mongodb import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    setup_logging()
    logger = structlog.get_logger(__name__)
    logger.info("Starting Mars Landing Backend API", version=settings.VERSION)
    
    # Connect to MongoDB
    await connect_to_mongo()
    logger.info("Connected to MongoDB")
    
    yield
    
    # Shutdown
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")
    logger.info("Shutting down Mars Landing Backend API")


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Backend API for Mars Landing project",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # Set up CORS
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Set up trusted host middleware
    if settings.allowed_hosts_list:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.allowed_hosts_list,
        )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Add Prometheus metrics
    if settings.ENABLE_METRICS:
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse(
            content={
                "status": "healthy",
                "version": settings.VERSION,
                "environment": settings.ENVIRONMENT,
            }
        )

    return app


app = create_application()


def main() -> None:
    """Main entry point for the application."""
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
