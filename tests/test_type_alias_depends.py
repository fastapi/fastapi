import importlib

import pytest
from fastapi.testclient import TestClient

from .utils import needs_py312


@pytest.fixture
def client():
    mod = importlib.import_module("tests._test_type_alias_depends")
    return TestClient(mod.app)


@needs_py312
def test_type_alias_depends(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "foo1": "foo1",
        "foo2": "foo2_x",
        "bar1": "bar1",
        "bar2": "bar2_y",
    }
