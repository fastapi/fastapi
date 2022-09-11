from typing import List, Tuple

from fastapi import Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient

app = FastAPI()


def get_user(required_scopes: SecurityScopes):
    return "john", required_scopes.scopes


def get_user_override(required_scopes: SecurityScopes):
    return "alice", required_scopes.scopes


def get_data():
    return [1, 2, 3]


def get_data_override():
    return [3, 4, 5]


@app.get("/user")
def read_user(
    user_data: Tuple[str, List[str]] = Security(get_user, scopes=["foo", "bar"]),
    data: List[int] = Depends(get_data),
):
    return {"user": user_data[0], "scopes": user_data[1], "data": data}


client = TestClient(app)


def test_normal():
    response = client.get("/user")
    assert response.json() == {
        "user": "john",
        "scopes": ["foo", "bar"],
        "data": [1, 2, 3],
    }


def test_override_data():
    app.dependency_overrides[get_data] = get_data_override
    response = client.get("/user")
    assert response.json() == {
        "user": "john",
        "scopes": ["foo", "bar"],
        "data": [3, 4, 5],
    }
    app.dependency_overrides = {}


def test_override_security():
    app.dependency_overrides[get_user] = get_user_override
    response = client.get("/user")
    assert response.json() == {
        "user": "alice",
        "scopes": ["foo", "bar"],
        "data": [1, 2, 3],
    }
    app.dependency_overrides = {}
