#!/usr/bin/env python3
"""
Create initial superuser from environment variables.
Idempotent - won't create duplicate users.
"""
import asyncio
import sys

from tortoise import Tortoise

from app.core.config import get_settings
from app.models.user import User, UserKind
from app.core.security import get_password_hash


async def create_superuser():
    """Create the first superuser if it doesn't exist."""
    settings = get_settings()
    
    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user", "aerich.models"]},
    )
    await Tortoise.generate_schemas()
    
    try:
        # Check if user already exists
        existing_user = await User.filter(
            email=settings.FIRST_SUPERUSER_EMAIL
        ).first()
        
        if existing_user:
            print(f"✓ Superuser '{settings.FIRST_SUPERUSER_EMAIL}' already exists")
            return
        
        # Create superuser
        user = await User.create(
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            first_name=settings.FIRST_SUPERUSER_FIRST_NAME,
            last_name=settings.FIRST_SUPERUSER_LAST_NAME,
            kind=UserKind.SUPER_ADMIN,
            is_active=True,
            is_superuser=True,
        )
        
        print(f"✓ Created superuser: {user.email}")
        print(f"  → Email: {settings.FIRST_SUPERUSER_EMAIL}")
        print(f"  → Password: {settings.FIRST_SUPERUSER_PASSWORD}")
        print(f"  → Change password after first login!")
        
    except Exception as e:
        print(f"✗ Error creating superuser: {e}", file=sys.stderr)
        raise
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(create_superuser())
