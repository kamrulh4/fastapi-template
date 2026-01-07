from enum import StrEnum

from tortoise import fields

from app.models.base import BaseModel


class UserKind(StrEnum):
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    USER = "USER"
    OTHER = "OTHER"


class User(BaseModel):
    """User model storing authentication and profile data."""

    email: str = fields.CharField(max_length=255, unique=True, index=True)
    hashed_password: str = fields.CharField(max_length=255)

    first_name: str | None = fields.CharField(max_length=100, null=True)
    last_name: str | None = fields.CharField(max_length=100, null=True)

    kind: UserKind = fields.CharEnumField(UserKind, default=UserKind.USER)

    is_active: bool = fields.BooleanField(default=True)
    is_superuser: bool = fields.BooleanField(default=False)

    class Meta:
        table = "users"
