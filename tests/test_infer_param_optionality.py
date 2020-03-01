from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


user_router = APIRouter()
item_router = APIRouter()


@user_router.get("/")
def get_users():
    return [{"user_id": "u1"}, {"user_id": "u2"}]


@user_router.get("/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}


@item_router.get("/")
def get_items(user_id: str = None):
    if user_id is None:
        return [{"item_id": "i1", "user_id": "u1"}, {"item_id": "i2", "user_id": "u2"}]
    else:
        return [{"item_id": "i2", "user_id": user_id}]


@item_router.get("/{item_id}")
def get_item(item_id: str, user_id: str = None):
    if user_id is None:
        return {"item_id": item_id}
    else:
        return {"item_id": item_id, "user_id": user_id}


app.include_router(user_router, prefix="/users")
app.include_router(item_router, prefix="/items")

app.include_router(item_router, prefix="/users/{user_id}/items")


client = TestClient(app)


def test_get_users():
    """Check that /users returns expected data"""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"user_id": "u1"}, {"user_id": "u2"}]


def test_get_user():
    """Check that /users/{user_id} returns expected data"""
    response = client.get("/users/abc123")
    assert response.status_code == 200
    assert response.json() == {"user_id": "abc123"}


def test_get_items_1():
    """Check that /items returns expected data"""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [
        {"item_id": "i1", "user_id": "u1"},
        {"item_id": "i2", "user_id": "u2"},
    ]


def test_get_items_2():
    """Check that /items returns expected data with user_id specified"""
    response = client.get("/items?user_id=abc123")
    assert response.status_code == 200
    assert response.json() == [{"item_id": "i2", "user_id": "abc123"}]


def test_get_item_1():
    """Check that /items/{item_id} returns expected data"""
    response = client.get("/items/item01")
    assert response.status_code == 200
    assert response.json() == {"item_id": "item01"}


def test_get_item_2():
    """Check that /items/{item_id} returns expected data with user_id specified"""
    response = client.get("/items/item01?user_id=abc123")
    assert response.status_code == 200
    assert response.json() == {"item_id": "item01", "user_id": "abc123"}


def test_get_users_items():
    """Check that /users/{user_id}/items returns expected data"""
    response = client.get("/users/abc123/items")
    assert response.status_code == 200
    assert response.json() == [{"item_id": "i2", "user_id": "abc123"}]


def test_get_users_item():
    """Check that /users/{user_id}/items returns expected data"""
    response = client.get("/users/abc123/items/item01")
    assert response.status_code == 200
    assert response.json() == {"item_id": "item01", "user_id": "abc123"}


def test_schema_1():
    """Check that the user_id is a required path parameter under /users"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    r = response.json()

    d = {
        "required": True,
        "schema": {"title": "User Id", "type": "string"},
        "name": "user_id",
        "in": "path",
    }

    assert d in r["paths"]["/users/{user_id}"]["get"]["parameters"]
    assert d in r["paths"]["/users/{user_id}/items/"]["get"]["parameters"]


def test_schema_2():
    """Check that the user_id is an optional query parameter under /items"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    r = response.json()

    d = {
        "required": False,
        "schema": {"title": "User Id", "type": "string"},
        "name": "user_id",
        "in": "query",
    }

    assert d in r["paths"]["/items/{item_id}"]["get"]["parameters"]
    assert d in r["paths"]["/items/"]["get"]["parameters"]
