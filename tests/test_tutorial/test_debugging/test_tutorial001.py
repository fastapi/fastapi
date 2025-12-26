import importlib
import runpy
import sys
import unittest

import pytest
from fastapi.testclient import TestClient

MOD_NAME = "docs_src.debugging.tutorial001_py39"


@pytest.fixture(name="client")
def get_client():
    mod = importlib.import_module(MOD_NAME)
    client = TestClient(mod.app)
    return client


def test_uvicorn_run_is_not_called_on_import():
    if sys.modules.get(MOD_NAME):
        del sys.modules[MOD_NAME]  # pragma: no cover
    with unittest.mock.patch("uvicorn.run") as uvicorn_run_mock:
        importlib.import_module(MOD_NAME)
    uvicorn_run_mock.assert_not_called()


def test_get_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello world": "ba"}


def test_uvicorn_run_called_when_run_as_main():  # Just for coverage
    if sys.modules.get(MOD_NAME):
        del sys.modules[MOD_NAME]
    with unittest.mock.patch("uvicorn.run") as uvicorn_run_mock:
        runpy.run_module(MOD_NAME, run_name="__main__")

    uvicorn_run_mock.assert_called_once_with(
        unittest.mock.ANY, host="0.0.0.0", port=8000
    )


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "get": {
                    "summary": "Root",
                    "operationId": "root__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                    },
                }
            }
        },
    }
