from dataclasses import dataclass

from fastapi import Query


@dataclass
class PaginationParams:
    page: int
    page_size: int


async def get_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)
