from fastapi import FastAPI, Header
from fastapi.testclient import TestClient

app = FastAPI(
    servers=[
        {"url": "/", "description": "Default, relative server"},
        {
            "url": "http://staging.localhost.tiangolo.com:8000",
            "description": "Staging but actually localhost still",
        },
        {"url": "https://prod.example.com"},
    ]
)


@app.get("/foo")
def foo(
    hidden_header=Header(None, include_in_schema=False),
    visible_header=Header(None),
):
    return {
        "hidden_header": hidden_header,
        "visible_header": visible_header,
    }


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "servers": [
        {"url": "/", "description": "Default, relative server"},
        {
            "url": "http://staging.localhost.tiangolo.com:8000",
            "description": "Staging but actually localhost still",
        },
        {"url": "https://prod.example.com"},
    ],
    "paths": {
        "/foo": {
            "get": {
                "summary": "Foo",
                "operationId": "foo_foo_get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Visible-Header"},
                        "name": "visible-header",
                        "in": "header",
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi_servers():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_app():
    response = client.get(
        "/foo",
        headers={
            "Visible-Header": "Visible-Header-Value",
            "Hidden-Header": "Hidden-Header-Value",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "hidden_header": "Hidden-Header-Value",
        "visible_header": "Visible-Header-Value",
    }
