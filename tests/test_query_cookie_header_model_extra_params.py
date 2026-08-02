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


def test_header_model_extra_forbid_with_uppercase_aliases():
    from pydantic import ConfigDict, Field

    class ForbiddenHeaderModel(BaseModel):
        model_config = ConfigDict(extra="forbid")
        api_key: str = Field(..., alias="X-API-Key")
        user_agent: str = Field(..., alias="User-Agent")
        host: str
        accept: str
        accept_encoding: str = Field(..., alias="accept-encoding")
        connection: str

    app_forbid = FastAPI()

    @app_forbid.get("/test")
    def endpoint(headers: ForbiddenHeaderModel = Header()):
        return headers

    client = TestClient(app_forbid)
    response = client.get("/test", headers={"X-API-Key": "secret123"})
    assert response.status_code == 200
    assert response.json()["X-API-Key"] == "secret123"


def test_header_model_lowercase_aliases_and_convert_underscores():
    from pydantic import ConfigDict, Field

    class HeaderModelConvertTrue(BaseModel):
        model_config = ConfigDict(extra="forbid")
        custom_header: str = Field(..., alias="x-custom-header")
        user_token: str
        host: str
        user_agent: str = Field(..., alias="user-agent")
        accept: str
        accept_encoding: str = Field(..., alias="accept-encoding")
        connection: str

    class HeaderModelConvertFalse(BaseModel):
        model_config = ConfigDict(extra="forbid")
        custom_header: str = Field(..., alias="x-custom-header")
        user_token: str
        host: str
        user_agent: str = Field(..., alias="user-agent")
        accept: str
        accept_encoding: str = Field(..., alias="accept-encoding")
        connection: str

    app_convert = FastAPI()

    @app_convert.get("/convert-true")
    def endpoint_true(
        headers: HeaderModelConvertTrue = Header(convert_underscores=True),
    ):
        return headers

    @app_convert.get("/convert-false")
    def endpoint_false(
        headers: HeaderModelConvertFalse = Header(convert_underscores=False),
    ):
        return headers

    client = TestClient(app_convert)

    res_true = client.get(
        "/convert-true",
        headers={"X-Custom-Header": "val1", "User-Token": "val2"},
    )
    assert res_true.status_code == 200
    assert res_true.json()["x-custom-header"] == "val1"
    assert res_true.json()["user_token"] == "val2"

    res_false = client.get(
        "/convert-false",
        headers={"X-Custom-Header": "val1", "user_token": "val2"},
    )
    assert res_false.status_code == 200
    assert res_false.json()["x-custom-header"] == "val1"
    assert res_false.json()["user_token"] == "val2"


def test_header_model_repeated_values():
    from pydantic import ConfigDict, Field

    class MultiHeaderModel(BaseModel):
        model_config = ConfigDict(extra="forbid")
        x_keys: list[str] = Field(..., alias="X-Keys")
        host: str
        user_agent: str = Field(..., alias="user-agent")
        accept: str
        accept_encoding: str = Field(..., alias="accept-encoding")
        connection: str

    app_multi = FastAPI()

    @app_multi.get("/multi")
    def endpoint_multi(headers: MultiHeaderModel = Header()):
        return headers

    client = TestClient(app_multi)
    response = client.get(
        "/multi",
        headers=[("X-Keys", "key1"), ("X-Keys", "key2")],
    )
    assert response.status_code == 200
    assert response.json()["X-Keys"] == ["key1", "key2"]
