from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.query("/items/")
def query_items(item: Item):
    return {"method": "QUERY", "item": item}


@app.api_route("/api-route/", methods=["QUERY"])
def api_route_query():
    return {"method": "QUERY", "source": "api_route"}


router = APIRouter()


@router.query("/router/")
def router_query():
    return {"method": "QUERY", "source": "router"}


app.include_router(router)

client = TestClient(app)


def test_app_query_with_body():
    body = {"name": "Foo", "price": 5.5}
    response = client.request("QUERY", "/items/", json=body)
    assert response.status_code == 200, response.text
    assert response.json() == {"method": "QUERY", "item": body}


def test_router_query():
    response = client.request("QUERY", "/router/")
    assert response.status_code == 200, response.text
    assert response.json() == {"method": "QUERY", "source": "router"}


def test_api_route_query():
    response = client.request("QUERY", "/api-route/")
    assert response.status_code == 200, response.text
    assert response.json() == {"method": "QUERY", "source": "api_route"}


def test_get_is_not_allowed():
    response = client.get("/items/")
    assert response.status_code == 405, response.text
    assert "QUERY" in response.headers["allow"]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.2.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "query": {
                        "summary": "Query Items",
                        "operationId": "query_items_items__query",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                }
                            },
                            "required": True,
                        },
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
                },
                "/api-route/": {
                    "query": {
                        "summary": "Api Route Query",
                        "operationId": "api_route_query_api_route__query",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                },
                "/router/": {
                    "query": {
                        "summary": "Router Query",
                        "operationId": "router_query_router__query",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "Item": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "price": {"type": "number", "title": "Price"},
                        },
                        "type": "object",
                        "required": ["name", "price"],
                        "title": "Item",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                            "input": {"title": "Input"},
                            "ctx": {"type": "object", "title": "Context"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
