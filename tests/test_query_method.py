from typing import Annotated

from fastapi import APIRouter, Body, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel

app = FastAPI()

router = APIRouter()


class Search(BaseModel):
    term: str
    limit: int = 10


@app.query("/search")
def search(search: Search):
    return {"term": search.term, "limit": search.limit, "via": "app"}


@app.get("/search-multi")
def search_multi_get(q: str = "default"):
    return {"q": q, "via": "get"}


@app.query("/search-multi")
def search_multi_query(q: str = "default"):
    return {"q": q, "via": "query"}


@router.query("/router-search")
def router_search(term: Annotated[str, Body(embed=True)]):
    return {"term": term, "via": "router"}


def added_search(term: Annotated[str, Body(embed=True)]):
    return {"term": term, "via": "added"}


app.add_api_route("/added-search", added_search, methods=["QUERY"])

app.include_router(router)

client = TestClient(app)


def test_query_app_level():
    response = client.request("QUERY", "/search", json={"term": "fastapi", "limit": 5})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "fastapi", "limit": 5, "via": "app"}


def test_query_app_level_default_body_value():
    response = client.request("QUERY", "/search", json={"term": "fastapi"})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "fastapi", "limit": 10, "via": "app"}


def test_query_router_level():
    response = client.request("QUERY", "/router-search", json={"term": "routed"})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "routed", "via": "router"}


def test_query_via_add_api_route():
    response = client.request("QUERY", "/added-search", json={"term": "added"})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "added", "via": "added"}


def test_query_missing_body_returns_422():
    response = client.request("QUERY", "/search", json={"limit": 5})
    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["loc"] == ["body", "term"]


def test_query_wrong_method_returns_405():
    response = client.request("POST", "/search", json={"term": "x"})
    assert response.status_code == 405, response.text
    assert "QUERY" in response.headers["allow"]


def test_query_and_get_coexist_on_same_path():
    get_response = client.get("/search-multi", params={"q": "from-get"})
    assert get_response.status_code == 200, get_response.text
    assert get_response.json() == {"q": "from-get", "via": "get"}

    query_response = client.request(
        "QUERY", "/search-multi", params={"q": "from-query"}
    )
    assert query_response.status_code == 200, query_response.text
    assert query_response.json() == {"q": "from-query", "via": "query"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/search": {
                    "query": {
                        "summary": "Search",
                        "operationId": "search_search_query",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Search"}
                                }
                            },
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
                "/search-multi": {
                    "get": {
                        "summary": "Search Multi Get",
                        "operationId": "search_multi_get_search_multi_get",
                        "parameters": [
                            {
                                "name": "q",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "string",
                                    "default": "default",
                                    "title": "Q",
                                },
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
                    },
                    "query": {
                        "summary": "Search Multi Query",
                        "operationId": "search_multi_query_search_multi_query",
                        "parameters": [
                            {
                                "name": "q",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "string",
                                    "default": "default",
                                    "title": "Q",
                                },
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
                    },
                },
                "/added-search": {
                    "query": {
                        "summary": "Added Search",
                        "operationId": "added_search_added_search_query",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_added_search_added_search_query"
                                    }
                                }
                            },
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
                "/router-search": {
                    "query": {
                        "summary": "Router Search",
                        "operationId": "router_search_router_search_query",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_router_search_router_search_query"
                                    }
                                }
                            },
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
            },
            "components": {
                "schemas": {
                    "Body_added_search_added_search_query": {
                        "properties": {"term": {"type": "string", "title": "Term"}},
                        "type": "object",
                        "required": ["term"],
                        "title": "Body_added_search_added_search_query",
                    },
                    "Body_router_search_router_search_query": {
                        "properties": {"term": {"type": "string", "title": "Term"}},
                        "type": "object",
                        "required": ["term"],
                        "title": "Body_router_search_router_search_query",
                    },
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
                    "Search": {
                        "properties": {
                            "term": {"type": "string", "title": "Term"},
                            "limit": {
                                "type": "integer",
                                "title": "Limit",
                                "default": 10,
                            },
                        },
                        "type": "object",
                        "required": ["term"],
                        "title": "Search",
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
