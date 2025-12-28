from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Model(BaseModel):
    param: str

    model_config = {"extra": "allow"}


@app.get("/query")
async def query_model_with_extra(data: Model = Query()):
    return data


@app.get("/header")
async def header_model_with_extra(data: Model = Header()):
    return data


@app.get("/cookie")
async def cookies_model_with_extra(data: Model = Cookie()):
    return data


def test_query_pass_extra_list():
    client = TestClient(app)
    resp = client.get(
        "/query",
        params={
            "param": "123",
            "param2": ["456", "789"],  # Pass a list of values as extra parameter
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "param": "123",
        "param2": ["456", "789"],
    }


def test_query_pass_extra_single():
    client = TestClient(app)
    resp = client.get(
        "/query",
        params={
            "param": "123",
            "param2": "456",
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "param": "123",
        "param2": "456",
    }


def test_header_pass_extra_list():
    client = TestClient(app)

    resp = client.get(
        "/header",
        headers=[
            ("param", "123"),
            ("param2", "456"),  # Pass a list of values as extra parameter
            ("param2", "789"),
        ],
    )
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "param2" in resp_json
    assert resp_json["param2"] == ["456", "789"]


def test_header_pass_extra_single():
    client = TestClient(app)

    resp = client.get(
        "/header",
        headers=[
            ("param", "123"),
            ("param2", "456"),
        ],
    )
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "param2" in resp_json
    assert resp_json["param2"] == "456"


def test_cookie_pass_extra_list():
    client = TestClient(app)
    client.cookies = [
        ("param", "123"),
        ("param2", "456"),  # Pass a list of values as extra parameter
        ("param2", "789"),
    ]
    resp = client.get("/cookie")
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "param2" in resp_json
    assert resp_json["param2"] == "789"  # Cookies only keep the last value
