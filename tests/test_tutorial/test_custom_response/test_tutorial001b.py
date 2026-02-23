import warnings

import pytest
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FastAPIDeprecationWarning)
    from docs_src.custom_response.tutorial001b_py310 import app

client = TestClient(app)


@pytest.mark.filterwarnings("ignore::fastapi.exceptions.FastAPIDeprecationWarning")
def test_get_custom_response():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"item_id": "Foo"}]


@pytest.mark.filterwarnings("ignore::fastapi.exceptions.FastAPIDeprecationWarning")
def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "summary": "Read Items",
                        "operationId": "read_items_items__get",
                    }
                }
            },
        }
    )
