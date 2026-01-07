from typing import Optional
from uuid import UUID

from app.core.security import get_password_hash
from app.crud import user as user_crud
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_email(email: str) -> Optional[User]:
    """
    Fetch a non-deleted user by email.
    """
    return await user_crud.get_by_email(email)


async def get_user_by_uid(uid: UUID) -> Optional[User]:
    """
    Fetch a non-deleted user by UID.
    """
    return await user_crud.get_by_uid(uid)


async def create_user(user_in: UserCreate, *, is_superuser: bool = False) -> User:
    """
    Create a user after hashing the password.
    """
    hashed_password = get_password_hash(user_in.password)
    return await user_crud.create_user_record(
        email=user_in.email,
        hashed_password=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        is_superuser=is_superuser,
        kind=user_in.kind,
    )


async def update_user(user: User, user_in: UserUpdate) -> User:
    if user_in.first_name is not None:
        user.first_name = user_in.first_name
    if user_in.last_name is not None:
        user.last_name = user_in.last_name
    if user_in.kind is not None:
        user.kind = user_in.kind
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    await user.save()
    return user


async def list_users_paginated(page: int, page_size: int) -> tuple[list[User], int]:
    """
    Return paginated users (non-deleted) and total count.
    """
    total = await user_crud.count_users()
    offset = (page - 1) * page_size
    users = await user_crud.list_users(offset=offset, limit=page_size)
    return users, total


async def soft_delete_user(user: User) -> None:
    """
    Soft delete a user by flipping the is_deleted flag.
    """
    await user.soft_delete()
