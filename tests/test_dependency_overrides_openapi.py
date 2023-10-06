from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

router = APIRouter()


async def common_parameters(q: str, skip: int = 0, limit: int = 100):
    pass  # pragma: no cover


@app.get("/main-depends/")
async def main_depends(commons: dict = Depends(common_parameters)):
    pass  # pragma: no cover


app.include_router(router)

client = TestClient(app)


async def overrider_dependency_simple(q: Optional[str] = None):
    pass  # pragma: no cover


async def overrider_sub_dependency(k: str):
    pass  # pragma: no cover


async def overrider_dependency_with_sub(msg: dict = Depends(overrider_sub_dependency)):
    pass  # pragma: no cover


override_simple_openapi_schema = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/main-depends/": {
            "get": {
                "summary": "Main Depends",
                "operationId": "main_depends_main_depends__get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Q",
                        },
                        "name": "q",
                        "in": "query",
                    },
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_override_simple_openapi():
    app.dependency_overrides[common_parameters] = overrider_dependency_simple
    app.openapi_schema = None
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == override_simple_openapi_schema


overrider_dependency_with_sub_schema = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/main-depends/": {
            "get": {
                "summary": "Main Depends",
                "operationId": "main_depends_main_depends__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "K", "type": "string"},
                        "name": "k",
                        "in": "query",
                    },
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_overrider_dependency_with_sub():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    app.openapi_schema = None
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == overrider_dependency_with_sub_schema


def test_overrider_dependency_with_overriden_sub():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    app.dependency_overrides[overrider_sub_dependency] = overrider_dependency_simple
    app.openapi_schema = None
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == override_simple_openapi_schema
