# from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import get_settings


TORTOISE_ORM = {
    "connections": {"default": get_settings().DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


def init_tortoise(app):
    settings = get_settings()
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
