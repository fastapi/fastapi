from __future__ import annotations

import base64
import json
from collections.abc import Sequence
from math import ceil
from typing import Annotated, Any, Generic, TypeVar

from pydantic import BaseModel

from .param_functions import Query

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    next_cursor: str | None = None
    previous_cursor: str | None = None


class Paginator:
    def __init__(
        self,
        page: int = 1,
        page_size: int = 100,
        cursor: str | None = None,
    ) -> None:
        if page < 1:
            raise ValueError("page must be greater than or equal to 1")
        if page_size < 1:
            raise ValueError("page_size must be greater than or equal to 1")
        self.page = page
        self.page_size = page_size
        self.cursor = cursor

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

    def paginate(
        self,
        source: Sequence[T] | Any,
        *,
        total: int | None = None,
    ) -> PaginatedResponse[T]:
        if self._is_query_like(source):
            return self._paginate_query(source, total=total)
        items = list(source)
        item_total = len(items) if total is None else total
        page_items = items[self.skip : self.skip + self.limit]
        return self._response(
            items=page_items,
            total=item_total,
            page=self.page,
            page_size=self.page_size,
        )

    def paginate_cursor(
        self,
        source: Sequence[T],
        *,
        total: int | None = None,
    ) -> PaginatedResponse[T]:
        items = list(source)
        item_total = len(items) if total is None else total
        offset = self._decode_cursor(self.cursor) if self.cursor else self.skip
        if offset < 0:
            raise ValueError("Invalid cursor")
        page_items = items[offset : offset + self.page_size]
        page = (offset // self.page_size) + 1
        next_offset = offset + self.page_size
        previous_offset = max(offset - self.page_size, 0)
        has_next = next_offset < item_total
        has_previous = offset > 0
        return self._response(
            items=page_items,
            total=item_total,
            page=page,
            page_size=self.page_size,
            next_cursor=self._encode_cursor(next_offset) if has_next else None,
            previous_cursor=self._encode_cursor(previous_offset)
            if has_previous
            else None,
        )

    def _paginate_query(
        self,
        source: Any,
        *,
        total: int | None = None,
    ) -> PaginatedResponse[Any]:
        item_total = source.count() if total is None else total
        page_items = list(source.offset(self.skip).limit(self.limit).all())
        return self._response(
            items=page_items,
            total=item_total,
            page=self.page,
            page_size=self.page_size,
        )

    def _response(
        self,
        *,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
        next_cursor: str | None = None,
        previous_cursor: str | None = None,
    ) -> PaginatedResponse[T]:
        total_pages = ceil(total / page_size) if total else 0
        return PaginatedResponse[T](
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=next_cursor is not None or page < total_pages,
            has_previous=previous_cursor is not None or page > 1,
            next_cursor=next_cursor,
            previous_cursor=previous_cursor,
        )

    @staticmethod
    def _is_query_like(source: Any) -> bool:
        return all(
            callable(getattr(source, name, None))
            for name in ("count", "offset", "limit", "all")
        )

    @staticmethod
    def _encode_cursor(offset: int) -> str:
        payload = json.dumps({"offset": offset}, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(payload).decode().rstrip("=")

    @staticmethod
    def _decode_cursor(cursor: str | None) -> int:
        if cursor is None:
            return 0
        try:
            padding = "=" * (-len(cursor) % 4)
            decoded = base64.urlsafe_b64decode(f"{cursor}{padding}".encode())
            payload = json.loads(decoded)
            offset = payload["offset"]
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid cursor") from exc
        if not isinstance(offset, int):
            raise ValueError("Invalid cursor")
        return offset


def paginate(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=1000)] = 100,
    cursor: Annotated[str | None, Query()] = None,
) -> Paginator:
    return Paginator(page=page, page_size=page_size, cursor=cursor)


__all__ = ["PaginatedResponse", "Paginator", "paginate"]
