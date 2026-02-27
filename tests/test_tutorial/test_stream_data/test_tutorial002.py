import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial002_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    return importlib.import_module(f"docs_src.stream_data.{request.param}")


@pytest.fixture(name="client")
def get_client(mod):
    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    "path",
    [
        "/image/stream",
        "/image/stream-no-async",
        "/image/stream-no-annotation",
        "/image/stream-no-async-no-annotation",
    ],
)
def test_stream_image(mod, client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content == mod.binary_image


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/image/stream": {
                    "get": {
                        "summary": "Stream Image",
                        "operationId": "stream_image_image_stream_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "image/png": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/image/stream-no-async": {
                    "get": {
                        "summary": "Stream Image No Async",
                        "operationId": "stream_image_no_async_image_stream_no_async_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "image/png": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/image/stream-no-annotation": {
                    "get": {
                        "summary": "Stream Image No Annotation",
                        "operationId": "stream_image_no_annotation_image_stream_no_annotation_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "image/png": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/image/stream-no-async-no-annotation": {
                    "get": {
                        "summary": "Stream Image No Async No Annotation",
                        "operationId": "stream_image_no_async_no_annotation_image_stream_no_async_no_annotation_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "image/png": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
            },
        }
    )
