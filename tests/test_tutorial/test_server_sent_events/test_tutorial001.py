import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.server_sent_events.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    "path",
    [
        "/items/stream",
        "/items/stream-no-async",
        "/items/stream-no-annotation",
        "/items/stream-no-async-no-annotation",
    ],
)
def test_stream_items(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/stream": {
                    "get": {
                        "summary": "Sse Items",
                        "operationId": "sse_items_items_stream_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "$ref": "#/components/schemas/Item"
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/items/stream-no-async": {
                    "get": {
                        "summary": "Sse Items No Async",
                        "operationId": "sse_items_no_async_items_stream_no_async_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "$ref": "#/components/schemas/Item"
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/items/stream-no-annotation": {
                    "get": {
                        "summary": "Sse Items No Annotation",
                        "operationId": "sse_items_no_annotation_items_stream_no_annotation_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {"type": "string"},
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/items/stream-no-async-no-annotation": {
                    "get": {
                        "summary": "Sse Items No Async No Annotation",
                        "operationId": "sse_items_no_async_no_annotation_items_stream_no_async_no_annotation_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {"type": "string"},
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "Item": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "description": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "null"},
                                ],
                                "title": "Description",
                            },
                        },
                        "type": "object",
                        "required": ["name", "description"],
                        "title": "Item",
                    }
                }
            },
        }
    )
