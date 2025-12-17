import gzip
import importlib
import json

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from tests.utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.custom_request_and_route.{request.param}")

    @mod.app.get("/check-class")
    async def check_gzip_request(request: Request):
        return {"request_class": type(request).__name__}

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize("compress", [True, False])
def test_gzip_request(client: TestClient, compress):
    n = 1000
    headers = {}
    body = [1] * n
    data = json.dumps(body).encode()
    if compress:
        data = gzip.compress(data)
        headers["Content-Encoding"] = "gzip"
    headers["Content-Type"] = "application/json"
    response = client.post("/sum", content=data, headers=headers)
    assert response.json() == {"sum": n}


def test_request_class(client: TestClient):
    response = client.get("/check-class")
    assert response.json() == {"request_class": "GzipRequest"}
