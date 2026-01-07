from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    page: int
    page_size: int
    next: str | None = None
    prev: str | None = None
    total: int | None = None


class ListResponse(BaseModel, Generic[T]):
    results: list[T]
    pagination: Pagination
    status_code: int = 200


class ItemResponse(BaseModel, Generic[T]):
    result: T
    status_code: int = 200


class ErrorResponse(BaseModel):
    detail: str
    status_code: int
