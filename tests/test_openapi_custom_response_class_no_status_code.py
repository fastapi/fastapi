from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from starlette.responses import Response


class CustomResponse(Response):
    """A custom response class whose __init__ does not expose status_code
    as a parameter with an int default. This previously caused an
    UnboundLocalError during OpenAPI schema generation when the route
    did not specify an explicit status_code."""

    media_type = "text/plain"

    def __init__(self, content: str, **kwargs: object) -> None:
        super().__init__(content=content, status_code=200, **kwargs)


app = FastAPI()


@app.get("/items", response_class=CustomResponse)
async def get_items():
    return "ok"


client = TestClient(app)


def test_get_response():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.text == "ok"


def test_openapi_schema():
    """OpenAPI generation must not crash when the response class's __init__
    lacks a status_code parameter with an int default."""
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items": {
                    "get": {
                        "summary": "Get Items",
                        "operationId": "get_items_items_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                }
            },
        }
    )
