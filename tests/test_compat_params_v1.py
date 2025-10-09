from typing import Annotated, Optional

from fastapi import FastAPI
from fastapi._compat._params_v1 import Body, Cookie, Header, Path, Query
from fastapi._compat.v1 import BaseModel
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


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
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
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
