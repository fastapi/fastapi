from typing import Annotated

import pytest
from fastapi import APIRouter, Depends, FastAPI, Path, WebSocket
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import AliasChoices, AliasPath

app = FastAPI()
router = APIRouter()
identifier_path = Path(
    alias="unused",
    validation_alias=AliasChoices("item_id", "id"),
    ge=1,
)
Identifier = Annotated[int, identifier_path]


def get_identifier(value: Identifier):
    return value


@router.get("/")
def read_item(value: Annotated[int, Depends(get_identifier)]):
    return value


app.include_router(router, prefix="/items/{item_id}")
app.include_router(router, prefix="/legacy-items/{id}")


@app.websocket("/ws/{id}")
async def read_websocket(
    websocket: WebSocket, value: Annotated[int, Depends(get_identifier)]
):
    await websocket.accept()
    await websocket.send_json(value)
    await websocket.close()


client = TestClient(app)


@pytest.mark.parametrize("prefix", ["/items", "/legacy-items"])
def test_dependency_alias_choices_follow_router_prefix(prefix: str):
    response = client.get(f"{prefix}/1/")
    assert response.status_code == 200
    assert response.json() == 1
    assert identifier_path.validation_alias == AliasChoices("item_id", "id")
    assert identifier_path.alias == "unused"


@pytest.mark.parametrize(
    "prefix, alias", [("/items", "item_id"), ("/legacy-items", "id")]
)
def test_invalid_value_uses_route_parameter_name(prefix: str, alias: str):
    response = client.get(f"{prefix}/invalid/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", alias],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }


def test_selected_alias_preserves_constraints():
    response = client.get("/legacy-items/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["path", "id"],
                "msg": "Input should be greater than or equal to 1",
                "input": "0",
                "ctx": {"ge": 1},
            }
        ]
    }


@pytest.mark.parametrize("alias", ["first", "second"])
def test_individual_path_alias_choices(alias: str):
    app = FastAPI()

    @app.get("/{" + alias + "}")
    def read(
        value: Annotated[int, Path(validation_alias=AliasChoices("first", "second"))],
    ):
        return value

    client = TestClient(app)
    response = client.get("/1")
    assert response.status_code == 200
    assert response.json() == 1


def test_multiple_matching_choices_follow_declaration_order():
    app = FastAPI()

    @app.get("/{second}/{first}")
    def read(
        value: Annotated[
            int, Path(alias="second", validation_alias=AliasChoices("first", "second"))
        ],
        second: str,
    ):
        return {"value": value, "second": second}

    client = TestClient(app)
    response = client.get("/2/1")
    assert response.status_code == 200
    assert response.json() == {"value": 1, "second": "2"}
    response = client.get("/2/invalid")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "first"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }


def test_unmatched_choices_preserve_explicit_alias():
    app = FastAPI()

    @app.get("/{legacy}")
    def read(
        value: Annotated[
            int, Path(alias="legacy", validation_alias=AliasChoices("first", "second"))
        ],
    ):
        return value

    client = TestClient(app)
    response = client.get("/1")
    assert response.status_code == 200
    assert response.json() == 1


@pytest.mark.parametrize(
    "validation_alias",
    [AliasPath("value"), AliasChoices("first", AliasPath("value"))],
)
def test_alias_path_extraction_is_unchanged(validation_alias):
    app = FastAPI()

    @app.get("/{first}/{value}")
    def read(
        value: Annotated[int, Path(validation_alias=validation_alias)], first: int
    ):
        return {"value": value, "first": first}

    client = TestClient(app)
    response = client.get("/1/2")
    assert response.status_code == 200
    assert response.json() == {"value": 2, "first": 1}


def test_websocket_dependency_uses_matching_alias():
    with client.websocket_connect("/ws/1") as websocket:
        assert websocket.receive_json() == 1


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/{item_id}/": {
                    "get": {
                        "summary": "Read Item",
                        "operationId": "read_item_items__item_id___get",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "title": "Item Id",
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
                    }
                },
                "/legacy-items/{id}/": {
                    "get": {
                        "summary": "Read Item",
                        "operationId": "read_item_legacy_items__id___get",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "title": "Id",
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
