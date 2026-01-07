from typing import Optional
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models.user import User, UserKind


async def get_by_email(email: str) -> Optional[User]:
    try:
        return await User.get(email=email, is_deleted=False)
    except DoesNotExist:
        return None


async def get_by_uid(uid: UUID) -> Optional[User]:
    try:
        return await User.get(uid=uid, is_deleted=False)
    except DoesNotExist:
        return None


async def create_user_record(
    *,
    email: str,
    hashed_password: str,
    first_name: str | None,
    last_name: str | None,
    is_superuser: bool,
    kind: UserKind,
) -> User:
    try:
        return await User.create(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            kind=kind,
        )
    except IntegrityError as exc:
        raise ValueError("User with this email already exists") from exc


async def list_users(offset: int, limit: int) -> list[User]:
    return await User.filter(is_deleted=False).offset(offset).limit(limit)


async def count_users() -> int:
    return await User.filter(is_deleted=False).count()
