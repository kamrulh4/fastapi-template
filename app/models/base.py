from datetime import datetime

import uuid

from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    """Abstract base model with common fields and soft-delete support."""

    id: int = fields.IntField(pk=True)
    uid: uuid.UUID = fields.UUIDField(default=uuid.uuid4, unique=True, index=True)

    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)
    is_deleted: bool = fields.BooleanField(default=False)

    class Meta:
        abstract = True

    async def soft_delete(self) -> None:
        self.is_deleted = True
        await self.save(update_fields=["is_deleted"])
