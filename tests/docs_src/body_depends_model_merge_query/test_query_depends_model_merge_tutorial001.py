import pytest
from fastapi import status

from tests.docs_src._loader import docs_src_test_client


@pytest.fixture(scope="module")
def client():
    return docs_src_test_client(
        "docs_src_body_depends_model_merge_query_tutorial001",
        "body_depends_model_merge_query",
        "tutorial001_an_py310.py",
    )


_CATEGORY = "books"


@pytest.mark.parametrize(
    ("path", "params"),
    [
        pytest.param(
            "/catalog/items/",
            {"category": _CATEGORY, "in_stock": False},
            id="items_full",
        ),
        pytest.param(
            "/catalog/basics/",
            {"category": _CATEGORY},
            id="basics",
        ),
        pytest.param(
            "/catalog/items-paginated/",
            {"category": _CATEGORY, "page": 2, "per_page": 5},
            id="paginated",
        ),
    ],
)
def test_query_depends_model_merge(client, path, params):
    response = client.get(path, params=params)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == params
