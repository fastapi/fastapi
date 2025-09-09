import importlib
from types import ModuleType

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(
    name="mod",
    params=[
        "tutorial008f",
        "tutorial008f_an",
        pytest.param("tutorial008f_an_py39", marks=needs_py39),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dependencies.{request.param}")

    return mod


@pytest.mark.anyio
def test_os_error(mod: ModuleType):
    client = TestClient(mod.app)
    with pytest.raises(OSError) as exc_info:
        client.get("/me")
    assert "No such file or directory" in str(exc_info.value)


@pytest.mark.anyio
def test_internal_server_error(mod: ModuleType):
    client = TestClient(mod.app, raise_server_exceptions=False)
    response = client.get("/me")
    assert response.status_code == 500, response.text
    assert response.text == "Internal Server Error"
