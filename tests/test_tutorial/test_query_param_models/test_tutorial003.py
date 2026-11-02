import importlib

import pytest
from fastapi.testclient import TestClient

from tests.utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_py310", marks=needs_py310),
        pytest.param("tutorial003_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.query_param_models.{request.param}")
    return TestClient(mod.app)


def test_combined_query_param_models(client: TestClient):
    response = client.get("/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt")
    assert response.status_code == 200
    assert response.json() == {
        "pagination": {"limit": 5, "offset": 10},
        "filters": {"tags": ["red", "blue"]},
        "search": "shirt",
    }


def test_combined_query_param_models_defaults(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "pagination": {"limit": 10, "offset": 0},
        "filters": {"tags": []},
        "search": None,
    }
