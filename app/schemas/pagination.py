from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Información de paginación."""

    page: int
    size: int
    total: int
    pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica."""

    items: list[T]
    pagination: PaginationMeta