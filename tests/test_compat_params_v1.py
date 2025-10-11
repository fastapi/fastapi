import sys
from typing import List, Optional

import pytest

from tests.utils import pydantic_snapshot, skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

from fastapi import FastAPI
from fastapi._compat.v1 import BaseModel
from fastapi.temp_pydantic_v1_params import (
    Body,
    Cookie,
    File,
    Form,
    Header,
    Path,
    Query,
)
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from typing_extensions import Annotated


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


app = FastAPI()


@app.get("/items/{item_id}")
def get_item_with_path(
    item_id: Annotated[int, Path(title="The ID of the item", ge=1, le=1000)],
):
    return {"item_id": item_id}


@app.get("/items/")
def get_items_with_query(
    q: Annotated[
        Optional[str], Query(min_length=3, max_length=50, pattern="^[a-zA-Z0-9 ]+$")
    ] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100, examples=[5])] = 10,
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/users/")
def get_user_with_header(
    x_custom: Annotated[Optional[str], Header()] = None,
    x_token: Annotated[Optional[str], Header(convert_underscores=True)] = None,
):
    return {"x_custom": x_custom, "x_token": x_token}


@app.get("/cookies/")
def get_cookies(
    session_id: Annotated[Optional[str], Cookie()] = None,
    tracking_id: Annotated[Optional[str], Cookie(min_length=10)] = None,
):
    return {"session_id": session_id, "tracking_id": tracking_id}


@app.post("/items/")
def create_item(
    item: Annotated[
        Item,
        Body(examples=[{"name": "Foo", "price": 35.4, "description": "The Foo item"}]),
    ],
):
    return {"item": item}


@app.post("/items-embed/")
def create_item_embed(
    item: Annotated[Item, Body(embed=True)],
):
    return {"item": item}


@app.put("/items/{item_id}")
def update_item(
    item_id: Annotated[int, Path(ge=1)],
    item: Annotated[Item, Body()],
    importance: Annotated[int, Body(gt=0, le=10)],
):
    return {"item": item, "importance": importance}


@app.post("/form-data/")
def submit_form(
    username: Annotated[str, Form(min_length=3, max_length=50)],
    password: Annotated[str, Form(min_length=8)],
    email: Annotated[Optional[str], Form()] = None,
):
    return {"username": username, "password": password, "email": email}


@app.post("/upload/")
def upload_file(
    file: Annotated[bytes, File()],
    description: Annotated[Optional[str], Form()] = None,
):
    return {"file_size": len(file), "description": description}


@app.post("/upload-multiple/")
def upload_multiple_files(
    files: Annotated[List[bytes], File()],
    note: Annotated[str, Form()] = "",
):
    return {
        "file_count": len(files),
        "total_size": sum(len(f) for f in files),
        "note": note,
    }


client = TestClient(app)


# Path parameter tests
def test_path_param_valid():
    response = client.get("/items/50")
    assert response.status_code == 200
    assert response.json() == {"item_id": 50}


def test_path_param_too_large():
    response = client.get("/items/1001")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["path", "item_id"]


def test_path_param_too_small():
    response = client.get("/items/0")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["path", "item_id"]


# Query parameter tests
def test_query_params_valid():
    response = client.get("/items/?q=test search&skip=5&limit=20")
    assert response.status_code == 200
    assert response.json() == {"q": "test search", "skip": 5, "limit": 20}


def test_query_params_defaults():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"q": None, "skip": 0, "limit": 10}


def test_query_param_too_short():
    response = client.get("/items/?q=ab")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "q"]


def test_query_param_invalid_pattern():
    response = client.get("/items/?q=test@#$")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "q"]


def test_query_param_limit_too_large():
    response = client.get("/items/?limit=101")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "limit"]


# Header parameter tests
def test_header_params():
    response = client.get(
        "/users/",
        headers={"X-Custom": "Plumbus", "X-Token": "secret-token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "x_custom": "Plumbus",
        "x_token": "secret-token",
    }


def test_header_underscore_conversion():
    response = client.get(
        "/users/",
        headers={"x-token": "secret-token-with-dash"},
    )
    assert response.status_code == 200
    assert response.json()["x_token"] == "secret-token-with-dash"


def test_header_params_none():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {"x_custom": None, "x_token": None}


# Cookie parameter tests
def test_cookie_params():
    with TestClient(app) as client:
        client.cookies.set("session_id", "abc123")
        client.cookies.set("tracking_id", "1234567890abcdef")
        response = client.get("/cookies/")
    assert response.status_code == 200
    assert response.json() == {
        "session_id": "abc123",
        "tracking_id": "1234567890abcdef",
    }


def test_cookie_tracking_id_too_short():
    with TestClient(app) as client:
        client.cookies.set("tracking_id", "short")
        response = client.get("/cookies/")
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["cookie", "tracking_id"],
                    "msg": "ensure this value has at least 10 characters",
                    "type": "value_error.any_str.min_length",
                    "ctx": {"limit_value": 10},
                }
            ]
        }
    )


def test_cookie_params_none():
    response = client.get("/cookies/")
    assert response.status_code == 200
    assert response.json() == {"session_id": None, "tracking_id": None}


# Body parameter tests
def test_body_param():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 29.99, "description": "A test item"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "item": {
            "name": "Test Item",
            "price": 29.99,
            "description": "A test item",
        }
    }


def test_body_param_minimal():
    response = client.post(
        "/items/",
        json={"name": "Minimal", "price": 9.99},
    )
    assert response.status_code == 200
    assert response.json() == {
        "item": {"name": "Minimal", "price": 9.99, "description": None}
    }


def test_body_param_missing_required():
    response = client.post(
        "/items/",
        json={"name": "Incomplete"},
    )
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "price"]


def test_body_embed():
    response = client.post(
        "/items-embed/",
        json={"item": {"name": "Embedded", "price": 15.0}},
    )
    assert response.status_code == 200
    assert response.json() == {
        "item": {"name": "Embedded", "price": 15.0, "description": None}
    }


def test_body_embed_wrong_structure():
    response = client.post(
        "/items-embed/",
        json={"name": "Not Embedded", "price": 15.0},
    )
    assert response.status_code == 422


# Multiple body parameters test
def test_multiple_body_params():
    response = client.put(
        "/items/5",
        json={
            "item": {"name": "Updated Item", "price": 49.99},
            "importance": 8,
        },
    )
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "item": {"name": "Updated Item", "price": 49.99, "description": None},
            "importance": 8,
        }
    )


def test_multiple_body_params_importance_too_large():
    response = client.put(
        "/items/5",
        json={
            "item": {"name": "Item", "price": 10.0},
            "importance": 11,
        },
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "importance"],
                    "msg": "ensure this value is less than or equal to 10",
                    "type": "value_error.number.not_le",
                    "ctx": {"limit_value": 10},
                }
            ]
        }
    )


def test_multiple_body_params_importance_too_small():
    response = client.put(
        "/items/5",
        json={
            "item": {"name": "Item", "price": 10.0},
            "importance": 0,
        },
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "importance"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ]
        }
    )


# Form parameter tests
def test_form_data_valid():
    response = client.post(
        "/form-data/",
        data={
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com",
    }


def test_form_data_optional_field():
    response = client.post(
        "/form-data/",
        data={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "password": "password123",
        "email": None,
    }


def test_form_data_username_too_short():
    response = client.post(
        "/form-data/",
        data={"username": "ab", "password": "password123"},
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "username"],
                    "msg": "ensure this value has at least 3 characters",
                    "type": "value_error.any_str.min_length",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_form_data_password_too_short():
    response = client.post(
        "/form-data/",
        data={"username": "testuser", "password": "short"},
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "password"],
                    "msg": "ensure this value has at least 8 characters",
                    "type": "value_error.any_str.min_length",
                    "ctx": {"limit_value": 8},
                }
            ]
        }
    )


# File upload tests
def test_upload_file():
    response = client.post(
        "/upload/",
        files={"file": ("test.txt", b"Hello, World!", "text/plain")},
        data={"description": "A test file"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "file_size": 13,
        "description": "A test file",
    }


def test_upload_file_without_description():
    response = client.post(
        "/upload/",
        files={"file": ("test.txt", b"Hello!", "text/plain")},
    )
    assert response.status_code == 200
    assert response.json() == {
        "file_size": 6,
        "description": None,
    }


def test_upload_multiple_files():
    response = client.post(
        "/upload-multiple/",
        files=[
            ("files", ("file1.txt", b"Content 1", "text/plain")),
            ("files", ("file2.txt", b"Content 2", "text/plain")),
            ("files", ("file3.txt", b"Content 3", "text/plain")),
        ],
        data={"note": "Multiple files uploaded"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "file_count": 3,
        "total_size": 27,
        "note": "Multiple files uploaded",
    }


def test_upload_multiple_files_empty_note():
    response = client.post(
        "/upload-multiple/",
        files=[
            ("files", ("file1.txt", b"Test", "text/plain")),
        ],
    )
    assert response.status_code == 200
    assert response.json()["file_count"] == 1
    assert response.json()["note"] == ""


# __repr__ tests
def test_query_repr():
    query_param = Query(default=None, min_length=3)
    assert repr(query_param) == "Query(None)"


def test_body_repr():
    body_param = Body(default=None)
    assert repr(body_param) == "Body(None)"


# Deprecation warning tests for regex parameter
def test_query_regex_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="`regex` has been deprecated"):
        Query(regex="^test$")


def test_body_regex_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="`regex` has been deprecated"):
        Body(regex="^test$")


# Deprecation warning tests for example parameter
def test_query_example_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="`example` has been deprecated"):
        Query(example="test example")


def test_body_example_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="`example` has been deprecated"):
        Body(example={"test": "example"})


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/{item_id}": {
                    "get": {
                        "summary": "Get Item With Path",
                        "operationId": "get_item_with_path_items__item_id__get",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "title": "The ID of the item",
                                    "minimum": 1,
                                    "maximum": 1000,
                                    "type": "integer",
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
                    "put": {
                        "summary": "Update Item",
                        "operationId": "update_item_items__item_id__put",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "title": "Item Id",
                                    "minimum": 1,
                                    "type": "integer",
                                },
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": pydantic_snapshot(
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/Body_update_item_items__item_id__put"
                                            }
                                        ),
                                        v2=snapshot(
                                            {
                                                "title": "Body",
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Body_update_item_items__item_id__put"
                                                    }
                                                ],
                                            }
                                        ),
                                    ),
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
                    },
                },
                "/items/": {
                    "get": {
                        "summary": "Get Items With Query",
                        "operationId": "get_items_with_query_items__get",
                        "parameters": [
                            {
                                "name": "q",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "title": "Q",
                                    "maxLength": 50,
                                    "minLength": 3,
                                    "pattern": "^[a-zA-Z0-9 ]+$",
                                    "type": "string",
                                },
                            },
                            {
                                "name": "skip",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "title": "Skip",
                                    "default": 0,
                                    "minimum": 0,
                                    "type": "integer",
                                },
                            },
                            {
                                "name": "limit",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "title": "Limit",
                                    "default": 10,
                                    "minimum": 1,
                                    "maximum": 100,
                                    "examples": [5],
                                    "type": "integer",
                                },
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
                    },
                    "post": {
                        "summary": "Create Item",
                        "operationId": "create_item_items__post",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Item",
                                        "examples": [
                                            {
                                                "name": "Foo",
                                                "price": 35.4,
                                                "description": "The Foo item",
                                            }
                                        ],
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
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
                    },
                },
                "/users/": {
                    "get": {
                        "summary": "Get User With Header",
                        "operationId": "get_user_with_header_users__get",
                        "parameters": [
                            {
                                "name": "x-custom",
                                "in": "header",
                                "required": False,
                                "schema": {"title": "X-Custom", "type": "string"},
                            },
                            {
                                "name": "x-token",
                                "in": "header",
                                "required": False,
                                "schema": {"title": "X-Token", "type": "string"},
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
                },
                "/cookies/": {
                    "get": {
                        "summary": "Get Cookies",
                        "operationId": "get_cookies_cookies__get",
                        "parameters": [
                            {
                                "name": "session_id",
                                "in": "cookie",
                                "required": False,
                                "schema": {"title": "Session Id", "type": "string"},
                            },
                            {
                                "name": "tracking_id",
                                "in": "cookie",
                                "required": False,
                                "schema": {
                                    "title": "Tracking Id",
                                    "minLength": 10,
                                    "type": "string",
                                },
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
                },
                "/items-embed/": {
                    "post": {
                        "summary": "Create Item Embed",
                        "operationId": "create_item_embed_items_embed__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": pydantic_snapshot(
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/Body_create_item_embed_items_embed__post"
                                            }
                                        ),
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Body_create_item_embed_items_embed__post"
                                                    }
                                                ],
                                                "title": "Body",
                                            }
                                        ),
                                    ),
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
                "/form-data/": {
                    "post": {
                        "summary": "Submit Form",
                        "operationId": "submit_form_form_data__post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": pydantic_snapshot(
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/Body_submit_form_form_data__post"
                                            }
                                        ),
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Body_submit_form_form_data__post"
                                                    }
                                                ],
                                                "title": "Body",
                                            }
                                        ),
                                    ),
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
                "/upload/": {
                    "post": {
                        "summary": "Upload File",
                        "operationId": "upload_file_upload__post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": pydantic_snapshot(
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/Body_upload_file_upload__post"
                                            }
                                        ),
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Body_upload_file_upload__post"
                                                    }
                                                ],
                                                "title": "Body",
                                            }
                                        ),
                                    ),
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
                "/upload-multiple/": {
                    "post": {
                        "summary": "Upload Multiple Files",
                        "operationId": "upload_multiple_files_upload_multiple__post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": pydantic_snapshot(
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/Body_upload_multiple_files_upload_multiple__post"
                                            }
                                        ),
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Body_upload_multiple_files_upload_multiple__post"
                                                    }
                                                ],
                                                "title": "Body",
                                            }
                                        ),
                                    ),
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
            },
            "components": {
                "schemas": {
                    "Body_create_item_embed_items_embed__post": {
                        "properties": pydantic_snapshot(
                            v1=snapshot(
                                {"item": {"$ref": "#/components/schemas/Item"}}
                            ),
                            v2=snapshot(
                                {
                                    "item": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Item",
                                    }
                                }
                            ),
                        ),
                        "type": "object",
                        "required": ["item"],
                        "title": "Body_create_item_embed_items_embed__post",
                    },
                    "Body_submit_form_form_data__post": {
                        "properties": {
                            "username": {
                                "type": "string",
                                "maxLength": 50,
                                "minLength": 3,
                                "title": "Username",
                            },
                            "password": {
                                "type": "string",
                                "minLength": 8,
                                "title": "Password",
                            },
                            "email": {"type": "string", "title": "Email"},
                        },
                        "type": "object",
                        "required": ["username", "password"],
                        "title": "Body_submit_form_form_data__post",
                    },
                    "Body_update_item_items__item_id__put": {
                        "properties": {
                            "item": pydantic_snapshot(
                                v1=snapshot({"$ref": "#/components/schemas/Item"}),
                                v2=snapshot(
                                    {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Item",
                                    }
                                ),
                            ),
                            "importance": {
                                "type": "integer",
                                "maximum": 10.0,
                                "exclusiveMinimum": 0.0,
                                "title": "Importance",
                            },
                        },
                        "type": "object",
                        "required": ["item", "importance"],
                        "title": "Body_update_item_items__item_id__put",
                    },
                    "Body_upload_file_upload__post": {
                        "properties": {
                            "file": {
                                "type": "string",
                                "format": "binary",
                                "title": "File",
                            },
                            "description": {"type": "string", "title": "Description"},
                        },
                        "type": "object",
                        "required": ["file"],
                        "title": "Body_upload_file_upload__post",
                    },
                    "Body_upload_multiple_files_upload_multiple__post": {
                        "properties": {
                            "files": {
                                "items": {"type": "string", "format": "binary"},
                                "type": "array",
                                "title": "Files",
                            },
                            "note": {"type": "string", "title": "Note", "default": ""},
                        },
                        "type": "object",
                        "required": ["files"],
                        "title": "Body_upload_multiple_files_upload_multiple__post",
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
                    "Item": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "price": {"type": "number", "title": "Price"},
                            "description": {"type": "string", "title": "Description"},
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
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
