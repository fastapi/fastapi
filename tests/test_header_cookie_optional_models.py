from typing import Annotated

import pytest
from fastapi import Cookie, Depends, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


def test_optional_header_model():
    app = FastAPI()

    class RequestHeaders(BaseModel):
        x_request_id: str
        x_attempt: int
        x_tag: list[str] = Field(default_factory=list)
        enabled: bool = True

    @app.get("/")
    def read(headers: Annotated[RequestHeaders | None, Header()] = None):
        return headers

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.get(
        "/",
        headers=[
            ("X-Request-ID", ""),
            ("X-Attempt", "2"),
            ("X-Tag", "first"),
            ("x-tag", "second"),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "x_request_id": "",
        "x_attempt": 2,
        "x_tag": ["first", "second"],
        "enabled": True,
    }
    response = client.get("/", headers={"X-Request-ID": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", "x-attempt"]
    response = client.get("/", headers={"X-Request-ID": "request", "X-Attempt": "bad"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", "x-attempt"]
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_header_conversion_is_per_optional_model():
    app = FastAPI()

    class RequestHeaders(BaseModel):
        x_id: int

    @app.get("/")
    def read(
        converted: Annotated[RequestHeaders | None, Header()] = None,
        literal: Annotated[
            RequestHeaders | None, Header(convert_underscores=False)
        ] = None,
    ):
        return [converted, literal]

    client = TestClient(app)
    response = client.get("/", headers={"X-ID": "1"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"x_id": 1}, None]
    response = client.get("/", headers={"X_ID": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == [None, {"x_id": 2}]
    response = client.get("/", headers={"X-ID": "1", "X_ID": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"x_id": 1}, {"x_id": 2}]
    assert app.openapi()["paths"]["/"]["get"]["parameters"] == [
        {
            "name": "x-id",
            "in": "header",
            "required": False,
            "schema": {"type": "integer", "title": "X Id"},
        },
        {
            "name": "x_id",
            "in": "header",
            "required": False,
            "schema": {"type": "integer", "title": "X Id"},
        },
    ]
    assert RequestHeaders.model_fields["x_id"].alias is None


@pytest.mark.parametrize("name", ["x-request_id", "X-LEGACY_ID"])
def test_header_aliases_are_literal_and_case_insensitive(name):
    app = FastAPI()

    class RequestHeaders(BaseModel):
        request_id: str = Field(
            validation_alias=AliasChoices("X-Request_ID", "X-Legacy_ID")
        )
        x_attempt: int

    @app.get("/")
    def read(headers: Annotated[RequestHeaders | None, Header()] = None):
        return headers

    client = TestClient(app)
    response = client.get("/", headers={"X-Request-ID": "ignored"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.get("/", headers={name: "request"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", "x-attempt"]
    response = client.get("/", headers={name: "request", "X-Attempt": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"request_id": "request", "x_attempt": 2}


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
def test_automatic_headers_follow_extra_configuration(extra):
    app = FastAPI()

    class RequestHeaders(BaseModel):
        model_config = ConfigDict(extra=extra)
        x_tag: str = "default"

    @app.get("/")
    def read(headers: Annotated[RequestHeaders | None, Header()] = None):
        return headers

    client = TestClient(app)
    client.headers.clear()
    response = client.get("/")
    if extra == "forbid":
        assert response.status_code == 422
        assert response.json()["detail"] == [
            {
                "type": "extra_forbidden",
                "loc": ["header", "host"],
                "msg": "Extra inputs are not permitted",
                "input": "testserver",
            }
        ]
    else:
        assert response.status_code == 200, response.text
        assert response.json() == (
            {"x_tag": "default", "host": "testserver"} if extra == "allow" else None
        )


def test_allowed_header_extras_require_model_fields():
    app = FastAPI()

    class RequestHeaders(BaseModel):
        model_config = ConfigDict(extra="allow")
        x_id: int

    @app.get("/")
    def read(headers: Annotated[RequestHeaders | None, Header()] = None):
        return headers

    client = TestClient(app)
    client.headers.clear()
    response = client.get("/")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", "x-id"]
    response = client.get("/", headers={"X-ID": "1"})
    assert response.status_code == 200, response.text
    assert response.json() == {"x_id": 1, "host": "testserver"}


def test_optional_header_models_with_dependency_and_individual_header():
    app = FastAPI()

    class Trace(BaseModel):
        x_trace: str

    class ClientInfo(BaseModel):
        x_client: str

    def get_client_info(info: Annotated[ClientInfo | None, Header()] = None):
        return info

    @app.get("/")
    def read(
        host: Annotated[str, Header()],
        info: Annotated[ClientInfo | None, Depends(get_client_info)],
        trace: Annotated[Trace | None, Header()] = None,
    ):
        return [trace, info]

    client = TestClient(app)
    client.headers.clear()
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == [None, None]
    response = client.get("/", headers={"X-Trace": "trace"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"x_trace": "trace"}, None]
    response = client.get("/", headers={"X-Client": "client"})
    assert response.status_code == 200, response.text
    assert response.json() == [None, {"x_client": "client"}]
    response = client.get("/", headers={"X-Trace": "trace", "X-Client": "client"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"x_trace": "trace"}, {"x_client": "client"}]
    assert {
        p["name"]: p["required"]
        for p in app.openapi()["paths"]["/"]["get"]["parameters"]
    } == {"host": True, "x-trace": False, "x-client": False}


def test_header_model_parameter_default_and_required_group():
    app = FastAPI()

    class Trace(BaseModel):
        x_request_id: str

    @app.get("/default")
    def read_default(
        trace: Annotated[Trace | None, Header()] = Trace(x_request_id="default"),
    ):
        return trace

    @app.get("/required")
    def read_required(trace: Annotated[Trace | None, Header()]):
        return trace

    client = TestClient(app)
    response = client.get("/default")
    assert response.status_code == 200, response.text
    assert response.json() == {"x_request_id": "default"}
    response = client.get("/required")
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"type": "missing", "loc": ["header"], "msg": "Field required", "input": None}
    ]
    for path in ("/default", "/required"):
        response = client.get(path, headers={"X-Request-ID": "request"})
        assert response.status_code == 200, response.text
        assert response.json() == {"x_request_id": "request"}
    schema = app.openapi()
    assert schema["paths"]["/default"]["get"]["parameters"][0]["required"] is False
    assert schema["paths"]["/required"]["get"]["parameters"][0]["required"] is True


def test_optional_cookie_model():
    app = FastAPI()

    class Cookies(BaseModel):
        session_id: str
        counter: int
        enabled: bool = True

    @app.get("/")
    def read(cookies: Annotated[Cookies | None, Cookie()] = None):
        return cookies

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.get("/", headers={"cookie": "session_id=; counter=1; counter=2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"session_id": "", "counter": 2, "enabled": True}
    response = client.get("/", headers={"cookie": "session_id="})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["cookie", "counter"]
    response = client.get("/", headers={"cookie": "session_id=session; counter=bad"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["cookie", "counter"]
    assert response.json()["detail"][0]["type"] == "int_parsing"


@pytest.mark.parametrize("name", ["sessionId", "legacyId"])
def test_cookie_aliases_are_case_sensitive(name):
    app = FastAPI()

    class Cookies(BaseModel):
        session_id: int = Field(
            alias="sessionId", validation_alias=AliasChoices("sessionId", "legacyId")
        )

    @app.get("/")
    def read(cookies: Annotated[Cookies | None, Cookie()] = None):
        return cookies

    client = TestClient(app)
    response = client.get("/", headers={"cookie": f"{name.upper()}=1"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.get("/", headers={"cookie": f"{name}=1"})
    assert response.status_code == 200, response.text
    assert response.json() == {"sessionId": 1}
    response = client.get("/", headers={"cookie": f"{name}=bad"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["cookie", name]


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
@pytest.mark.parametrize(
    "cookies",
    [{"session_id": "session"}, {"session_id": "session", "tracking": "value"}],
)
def test_cookie_extras_and_declared_siblings(extra, cookies):
    app = FastAPI()

    class Preferences(BaseModel):
        model_config = ConfigDict(extra=extra)
        theme: str = "light"

    @app.get("/")
    def read(
        session_id: Annotated[str, Cookie()],
        preferences: Annotated[Preferences | None, Cookie()] = None,
    ):
        return preferences

    response = TestClient(app).get(
        "/",
        headers={
            "cookie": "; ".join(f"{key}={value}" for key, value in cookies.items())
        },
    )
    if extra == "forbid":
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["cookie", name] for name in cookies
        ]
        assert all(
            error["type"] == "extra_forbidden" for error in response.json()["detail"]
        )
    else:
        assert response.status_code == 200, response.text
        assert response.json() == (
            {"theme": "light", **cookies} if extra == "allow" else None
        )


def test_optional_cookie_models_with_dependency():
    app = FastAPI()

    class Preferences(BaseModel):
        theme: str

    class Session(BaseModel):
        session_id: str

    def get_session(session: Annotated[Session | None, Cookie()] = None):
        return session

    @app.get("/")
    def read(
        session: Annotated[Session | None, Depends(get_session)],
        preferences: Annotated[Preferences | None, Cookie()] = None,
    ):
        return [preferences, session]

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == [None, None]
    response = client.get("/", headers={"cookie": "session_id=session"})
    assert response.status_code == 200, response.text
    assert response.json() == [None, {"session_id": "session"}]
    response = client.get("/", headers={"cookie": "theme=dark"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"theme": "dark"}, None]
    response = client.get("/", headers={"cookie": "session_id=session; theme=dark"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"theme": "dark"}, {"session_id": "session"}]
    assert {
        p["name"]: p["required"]
        for p in app.openapi()["paths"]["/"]["get"]["parameters"]
    } == {"theme": False, "session_id": False}


def test_cookie_model_default_factory_and_required_group():
    app = FastAPI()
    calls = []

    class Preferences(BaseModel):
        theme: str

    def factory():
        calls.append("factory")
        return Preferences(theme="light")

    @app.get("/default")
    def read_default(
        preferences: Annotated[Preferences | None, Cookie(default_factory=factory)],
    ):
        return preferences

    @app.get("/required")
    def read_required(preferences: Annotated[Preferences | None, Cookie()]):
        return preferences

    client = TestClient(app)
    response = client.get("/default")
    assert response.status_code == 200, response.text
    assert response.json() == {"theme": "light"}
    assert calls == ["factory"]
    response = client.get("/required")
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"type": "missing", "loc": ["cookie"], "msg": "Field required", "input": None}
    ]
    for path in ("/default", "/required"):
        response = client.get(path, headers={"cookie": "theme=dark"})
        assert response.status_code == 200, response.text
        assert response.json() == {"theme": "dark"}
    assert calls == ["factory"]
    schema = app.openapi()
    assert schema["paths"]["/default"]["get"]["parameters"][0]["required"] is False
    assert schema["paths"]["/required"]["get"]["parameters"][0]["required"] is True


@pytest.mark.parametrize(
    "request_kwargs, expected",
    [
        ({}, [None, None, None]),
        ({"params": {"value": "1"}}, [{"value": 1}, None, None]),
        ({"headers": {"value": "2"}}, [None, {"value": 2}, None]),
        ({"headers": {"cookie": "value=3"}}, [None, None, {"value": 3}]),
        (
            {"params": {"value": "1"}, "headers": {"value": "2", "cookie": "value=3"}},
            [{"value": 1}, {"value": 2}, {"value": 3}],
        ),
    ],
)
def test_optional_models_keep_request_locations_separate(request_kwargs, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: int

    @app.get("/")
    def read(
        query: Annotated[Model | None, Query()] = None,
        header: Annotated[Model | None, Header()] = None,
        cookie: Annotated[Model | None, Cookie()] = None,
    ):
        return [query, header, cookie]

    response = TestClient(app).get("/", **request_kwargs)
    assert response.status_code == 200, response.text
    assert response.json() == expected
