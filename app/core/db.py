from tortoise.contrib.fastapi import register_tortoise

from app.core.config import get_settings


TORTOISE_ORM = {
    "connections": {"default": get_settings().DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


def init_tortoise(app):
    """
    Initialize Tortoise ORM with FastAPI.
    Uses TORTOISE_ORM config for consistency.
    generate_schemas=True works for development; use Aerich migrations for production.
    """
    settings = get_settings()
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models", "aerich.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
