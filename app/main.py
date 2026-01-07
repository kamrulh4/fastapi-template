from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.db import init_tortoise
from app.routers import api_router


settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Routers
    app.include_router(api_router)

    # DB
    init_tortoise(app)

    return app


app = create_app()
