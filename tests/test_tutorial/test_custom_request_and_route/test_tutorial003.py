import importlib

import pytest
from fastapi.testclient import TestClient

from tests.utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.custom_request_and_route.{request.param}")

    client = TestClient(mod.app)
    return client


def test_get(client: TestClient):
    response = client.get("/")
    assert response.json() == {"message": "Not timed"}
    assert "X-Response-Time" not in response.headers


def test_get_timed(client: TestClient):
    response = client.get("/timed")
    assert response.json() == {"message": "It's the time of my life"}
    assert "X-Response-Time" in response.headers
    assert float(response.headers["X-Response-Time"]) >= 0
