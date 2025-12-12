import importlib
from types import ModuleType

import pytest
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial008c_py39"),
        pytest.param("tutorial008c_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dependencies.{request.param}")

    return mod


def test_get_no_item(mod: ModuleType):
    client = TestClient(mod.app)
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found, there's only a plumbus here"}


def test_get(mod: ModuleType):
    client = TestClient(mod.app)
    response = client.get("/items/plumbus")
    assert response.status_code == 200, response.text
    assert response.json() == "plumbus"


def test_fastapi_error(mod: ModuleType):
    client = TestClient(mod.app)
    with pytest.raises(FastAPIError) as exc_info:
        client.get("/items/portal-gun")
    assert "raising an exception and a dependency with yield" in exc_info.value.args[0]


def test_internal_server_error(mod: ModuleType):
    client = TestClient(mod.app, raise_server_exceptions=False)
    response = client.get("/items/portal-gun")
    assert response.status_code == 500, response.text
    assert response.text == "Internal Server Error"
