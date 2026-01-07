from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import RefreshRequest, Token
from app.schemas.common import ItemResponse
from app.schemas.user import UserMe
from app.services.auth import authenticate_user, create_tokens_for_user
from app.services.user import get_user_by_uid

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return access and refresh tokens.

    Compatible with Swagger UI "Authorize" using OAuth2 password flow.
    """
    user = await authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token, refresh_token = await create_tokens_for_user(user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_tokens(body: RefreshRequest):
    """
    Refresh tokens using a valid refresh token.
    """
    from app.core.security import decode_token

    try:
        payload = decode_token(body.refresh_token, refresh=True)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    uid = payload.get("sub")
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    user = await get_user_by_uid(uid)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    access_token, refresh_token = await create_tokens_for_user(user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=ItemResponse[UserMe])
async def read_me(current_user: User = Depends(get_current_user)):
    """
    Return the current authenticated user's details.
    """
    return ItemResponse(result=current_user, status_code=status.HTTP_200_OK)
