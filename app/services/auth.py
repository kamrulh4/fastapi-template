from typing import Optional, Tuple

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User
from app.services.user import get_user_by_email


async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


async def create_tokens_for_user(user: User) -> Tuple[str, str]:
    access_token = create_access_token(user.uid)
    refresh_token = create_refresh_token(user.uid)
    return access_token, refresh_token
