from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.dependencies.auth import require_kinds
from app.dependencies.pagination import PaginationParams, get_pagination
from app.models.user import User, UserKind
from app.schemas.common import ItemResponse, ListResponse, Pagination
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import (
    create_user,
    get_user_by_email,
    get_user_by_uid,
    list_users_paginated,
    soft_delete_user,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    response_model=ItemResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user_in: UserCreate):
    """
    Public registration endpoint. Creates a regular USER (non-superuser).
    """
    existing = await get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    try:
        user = await create_user(user_in, is_superuser=False)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return ItemResponse(result=user, status_code=status.HTTP_201_CREATED)


@router.post(
    "/", response_model=ItemResponse[UserRead], status_code=status.HTTP_201_CREATED
)
async def create_new_user(
    user_in: UserCreate,
    _: User = Depends(require_kinds(UserKind.ADMIN, UserKind.SUPER_ADMIN)),
):
    """
    Create a new account. Admins/Super Admins only.
    """
    existing = await get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    user = await create_user(user_in)
    return ItemResponse(result=user, status_code=status.HTTP_201_CREATED)


@router.get("/", response_model=ListResponse[UserRead])
async def list_users(
    request: Request,
    _: User = Depends(require_kinds(UserKind.ADMIN, UserKind.SUPER_ADMIN)),
    pagination: PaginationParams = Depends(get_pagination),
):
    """
    List all non-deleted users with pagination metadata. Admins/Super Admins only.
    """
    users, total = await list_users_paginated(
        page=pagination.page, page_size=pagination.page_size
    )

    next_url = None
    if pagination.page * pagination.page_size < total:
        next_url = str(
            request.url.include_query_params(
                page=pagination.page + 1, page_size=pagination.page_size
            )
        )

    prev_url = None
    if pagination.page > 1:
        prev_url = str(
            request.url.include_query_params(
                page=pagination.page - 1, page_size=pagination.page_size
            )
        )

    pagination_meta = Pagination(
        page=pagination.page,
        page_size=pagination.page_size,
        next=next_url,
        prev=prev_url,
        total=total,
    )

    return ListResponse(
        results=users, pagination=pagination_meta, status_code=status.HTTP_200_OK
    )


@router.get("/{user_uid}", response_model=ItemResponse[UserRead])
async def get_user(
    user_uid: str,
    _: User = Depends(require_kinds(UserKind.ADMIN, UserKind.SUPER_ADMIN)),
):
    user = await get_user_by_uid(user_uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return ItemResponse(result=user, status_code=status.HTTP_200_OK)


@router.patch("/{user_uid}", response_model=ItemResponse[UserRead])
async def update_user_endpoint(
    user_uid: str,
    user_in: UserUpdate,
    _: User = Depends(require_kinds(UserKind.ADMIN, UserKind.SUPER_ADMIN)),
):
    user = await get_user_by_uid(user_uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user = await update_user(user, user_in)
    return ItemResponse(result=user, status_code=status.HTTP_200_OK)


@router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_uid: str,
    _: User = Depends(require_kinds(UserKind.ADMIN, UserKind.SUPER_ADMIN)),
):
    user = await get_user_by_uid(user_uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await soft_delete_user(user)
    return {"status_code": status.HTTP_204_NO_CONTENT}
