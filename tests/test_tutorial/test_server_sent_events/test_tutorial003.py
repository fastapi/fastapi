import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.server_sent_events.{request.param}")
    client = TestClient(mod.app)
    return client


def test_stream_logs(client: TestClient):
    response = client.get("/logs/stream")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3

    # raw_data is sent without JSON encoding (no quotes around the string)
    assert data_lines[0] == "data: 2025-01-01 INFO  Application started"
    assert data_lines[1] == "data: 2025-01-01 DEBUG Connected to database"
    assert data_lines[2] == "data: 2025-01-01 WARN  High memory usage detected"


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/logs/stream": {
                    "get": {
                        "summary": "Stream Logs",
                        "operationId": "stream_logs_logs_stream_get",
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
                }
            },
        }
    )
