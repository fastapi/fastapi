import importlib
from types import ModuleType

import pytest
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(
    name="mod",
    params=[
        "tutorial008e",
        "tutorial008e_an",
        pytest.param("tutorial008e_an_py39", marks=needs_py39),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dependencies.{request.param}")

    return mod


@pytest.mark.anyio
def test_fastapi_error(mod: ModuleType):
    client = TestClient(mod.app)
    with pytest.raises(FastAPIError) as exc_info:
        client.get("/me")
    assert (
        "Dependency get_username raised: generator didn't yield"
        in exc_info.value.args[0]
    )


@pytest.mark.anyio
def test_internal_server_error(mod: ModuleType):
    client = TestClient(mod.app, raise_server_exceptions=False)
    response = client.get("/me")
    assert response.status_code == 500, response.text
    assert response.text == "Internal Server Error"
