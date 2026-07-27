from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Model(BaseModel):
    param: str

    model_config = {"extra": "allow"}


class AuthHeaders(BaseModel):
    x_user_id: str


@app.get("/query")
async def query_model_with_extra(data: Model = Query()):
    return data


@app.get("/header")
async def header_model_with_extra(data: Model = Header()):
    return data


@app.get("/cookie")
async def cookies_model_with_extra(data: Model = Cookie()):
    return data


@app.get("/header-requires-hyphen")
async def header_model_requires_hyphen(data: AuthHeaders = Header()):
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


def test_header_model_prefers_hyphenated_header_with_convert_underscores():
    client = TestClient(app)

    resp = client.get(
        "/header-requires-hyphen",
        headers=[
            ("x-user-id", "hyphenated-value"),
            ("x_user_id", "underscore-value"),
        ],
    )

    assert resp.status_code == 200
    assert resp.json() == {"x_user_id": "hyphenated-value"}


def test_header_model_rejects_underscore_header_with_convert_underscores():
    client = TestClient(app)

    resp = client.get(
        "/header-requires-hyphen", headers={"x_user_id": "underscore-value"}
    )

    assert resp.status_code == 422
    assert resp.json()["detail"][0]["loc"] == ["header", "x_user_id"]


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
