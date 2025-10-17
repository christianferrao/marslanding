"""Health check endpoints."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.mongodb import get_database

router = APIRouter()


@router.get("/")
async def health_check() -> JSONResponse:
    """Basic health check."""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }
    )


@router.get("/detailed")
async def detailed_health_check(db=Depends(get_database)) -> JSONResponse:
    """Detailed health check with database connectivity."""
    try:
        # Test database connection
        await db.command("ping")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return JSONResponse(
        content={
            "status": "healthy" if db_status == "healthy" else "unhealthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "database": db_status,
            "timestamp": "2024-01-01T00:00:00Z",  # You can use datetime.utcnow().isoformat()
        }
    )
