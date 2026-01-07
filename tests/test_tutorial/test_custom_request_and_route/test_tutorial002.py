import importlib

import pytest
from dirty_equals import IsOneOf
from fastapi.testclient import TestClient

from tests.utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
        pytest.param("tutorial002_an_py39"),
        pytest.param("tutorial002_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.custom_request_and_route.{request.param}")

    client = TestClient(mod.app)
    return client


def test_endpoint_works(client: TestClient):
    response = client.post("/", json=[1, 2, 3])
    assert response.json() == 6


def test_exception_handler_body_access(client: TestClient):
    response = client.post("/", json={"numbers": [1, 2, 3]})
    assert response.json() == {
        "detail": {
            "errors": [
                {
                    "type": "list_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid list",
                    "input": {"numbers": [1, 2, 3]},
                }
            ],
            # httpx 0.28.0 switches to compact JSON https://github.com/encode/httpx/issues/3363
            "body": IsOneOf('{"numbers": [1, 2, 3]}', '{"numbers":[1,2,3]}'),
        }
    }
