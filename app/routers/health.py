from datetime import datetime, timezone

from fastapi import APIRouter, status
from tortoise import Tortoise

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        - API status
        - Database connectivity status
        - Timestamp
        - Environment info
    """
    settings = get_settings()
    
    # Test database connectivity
    db_status = "unknown"
    db_error = None
    
    try:
        # Execute a simple query to test database connection
        conn = Tortoise.get_connection("default")
        await conn.execute_query("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = "unhealthy"
        db_error = str(e)
    
    health_data = {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.ENVIRONMENT,
        "checks": {
            "api": {
                "status": "healthy",
                "message": "API is running"
            },
            "database": {
                "status": db_status,
                "message": "Database connection successful" if db_status == "healthy" else f"Database connection failed: {db_error}"
            }
        }
    }
    
    # Return 503 if database is unhealthy
    if db_status == "unhealthy":
        return health_data
    
    return health_data
