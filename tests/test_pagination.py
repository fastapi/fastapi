from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.pagination import PaginatedResponse, Paginator, paginate
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str


class QueryLike:
    def __init__(self, items: list[Item]) -> None:
        self.items = items
        self.skip = 0
        self.take = len(items)

    def count(self) -> int:
        return len(self.items)

    def offset(self, skip: int) -> "QueryLike":
        query = QueryLike(self.items)
        query.skip = skip
        query.take = self.take
        return query

    def limit(self, take: int) -> "QueryLike":
        query = QueryLike(self.items)
        query.skip = self.skip
        query.take = take
        return query

    def all(self) -> list[Item]:
        return self.items[self.skip : self.skip + self.take]


ITEMS = [Item(id=index, name=f"item-{index}") for index in range(1, 26)]


def test_offset_pagination_calculates_skip_limit_and_metadata() -> None:
    paginator = Paginator(page=2, page_size=10)

    response = paginator.paginate(ITEMS)

    assert paginator.skip == 10
    assert paginator.limit == 10
    assert response.items == ITEMS[10:20]
    assert response.total == 25
    assert response.page == 2
    assert response.page_size == 10
    assert response.total_pages == 3
    assert response.has_next is True
    assert response.has_previous is True


def test_offset_pagination_sets_boundary_flags() -> None:
    first_page = Paginator(page=1, page_size=10).paginate(ITEMS)
    last_page = Paginator(page=3, page_size=10).paginate(ITEMS)

    assert first_page.has_previous is False
    assert first_page.has_next is True
    assert last_page.has_previous is True
    assert last_page.has_next is False


def test_empty_offset_pagination_returns_stable_metadata() -> None:
    response = Paginator(page=1, page_size=10).paginate([])

    assert response.items == []
    assert response.total == 0
    assert response.page == 1
    assert response.page_size == 10
    assert response.total_pages == 0
    assert response.has_next is False
    assert response.has_previous is False


def test_offset_pagination_supports_query_like_sources() -> None:
    response = Paginator(page=2, page_size=5).paginate(QueryLike(ITEMS))

    assert response.items == ITEMS[5:10]
    assert response.total == 25
    assert response.page == 2
    assert response.total_pages == 5


def test_paginator_rejects_invalid_page_and_page_size() -> None:
    with pytest.raises(ValueError, match="page"):
        Paginator(page=0)

    with pytest.raises(ValueError, match="page"):
        Paginator(page=-1)

    with pytest.raises(ValueError, match="page_size"):
        Paginator(page_size=0)


def test_cursor_pagination_returns_opaque_next_and_previous_cursors() -> None:
    first_page = Paginator(page_size=10).paginate_cursor(ITEMS)

    assert first_page.items == ITEMS[:10]
    assert first_page.has_next is True
    assert first_page.has_previous is False
    assert first_page.next_cursor is not None
    assert first_page.previous_cursor is None
    assert "10" not in first_page.next_cursor

    second_page = Paginator(page_size=10, cursor=first_page.next_cursor).paginate_cursor(
        ITEMS
    )

    assert second_page.items == ITEMS[10:20]
    assert second_page.has_next is True
    assert second_page.has_previous is True
    assert second_page.next_cursor is not None
    assert second_page.previous_cursor is not None


def test_cursor_pagination_sets_last_page_boundary_flags() -> None:
    first_page = Paginator(page_size=10).paginate_cursor(ITEMS)
    second_page = Paginator(page_size=10, cursor=first_page.next_cursor).paginate_cursor(
        ITEMS
    )
    last_page = Paginator(page_size=10, cursor=second_page.next_cursor).paginate_cursor(
        ITEMS
    )

    assert last_page.items == ITEMS[20:25]
    assert last_page.has_next is False
    assert last_page.has_previous is True
    assert last_page.next_cursor is None
    assert last_page.previous_cursor is not None


def test_cursor_pagination_rejects_invalid_cursor() -> None:
    with pytest.raises(ValueError, match="Invalid cursor"):
        Paginator(page_size=10, cursor="not-a-valid-cursor").paginate_cursor(ITEMS)


def test_paginated_response_is_generic_over_pydantic_models() -> None:
    response = PaginatedResponse[Item](
        items=[Item(id=1, name="one")],
        total=1,
        page=1,
        page_size=10,
        total_pages=1,
        has_next=False,
        has_previous=False,
    )

    assert response.items[0].name == "one"


def test_paginate_dependency_reads_query_parameters() -> None:
    app = FastAPI()

    @app.get("/items")
    def read_items(
        paginator: Annotated[Paginator, Depends(paginate)],
    ) -> dict[str, int]:
        return {"page": paginator.page, "page_size": paginator.page_size}

    client = TestClient(app)

    assert client.get("/items").json() == {"page": 1, "page_size": 100}
    assert client.get("/items?page=3&page_size=20").json() == {
        "page": 3,
        "page_size": 20,
    }
    assert client.get("/items?page=0").status_code == 422
    assert client.get("/items?page=-1").status_code == 422
    assert client.get("/items?page_size=0").status_code == 422
