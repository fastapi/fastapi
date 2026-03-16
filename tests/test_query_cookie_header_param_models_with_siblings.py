from typing import Annotated

from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class QueryModel(BaseModel):
    limit: int
    q: str


class HeaderModel(BaseModel):
    x_token: str
    x_trace: list[str] = []


class CookieModel(BaseModel):
    session_id: str
    tracker: str


@app.get("/query/only")
def read_query_only(m: Annotated[QueryModel, Query()]):
    return {"m": m.model_dump()}


@app.get("/query/mixed")
def read_query_mixed(
    m: Annotated[QueryModel, Query()],
    extra: Annotated[int, Query()],
):
    return {"m": m.model_dump(), "extra": extra}


@app.get("/query/openapi-metadata")
def read_query_openapi_metadata(
    m: Annotated[QueryModel, Query()],
    documented_query: Annotated[
        str | None,
        Query(description="Documented query", deprecated=True),
    ] = None,
):
    return {"m": m.model_dump(), "documented_query": documented_query}


@app.get("/header/only")
def read_header_only(h: Annotated[HeaderModel, Header()]):
    return {"h": h.model_dump()}


@app.get("/header/mixed")
def read_header_mixed(
    h: Annotated[HeaderModel, Header()],
    extra: Annotated[str, Header()],
):
    return {"h": h.model_dump(), "extra": extra}


@app.get("/header/mixed-no-convert")
def read_header_mixed_no_convert(
    h: Annotated[HeaderModel, Header(convert_underscores=False)],
    extra: Annotated[str, Header()],
):
    return {"h": h.model_dump(), "extra": extra}


@app.get("/header/openapi-metadata")
def read_header_openapi_metadata(
    h: Annotated[HeaderModel, Header()],
    hidden_header: Annotated[str | None, Header(include_in_schema=False)] = None,
    documented_header: Annotated[
        str | None,
        Header(
            description="Documented header",
            openapi_examples={"demo": {"summary": "Demo", "value": "abc"}},
            deprecated=True,
        ),
    ] = None,
):
    return {
        "h": h.model_dump(),
        "hidden_header": hidden_header,
        "documented_header": documented_header,
    }


@app.get("/cookie/only")
def read_cookie_only(c: Annotated[CookieModel, Cookie()]):
    return {"c": c.model_dump()}


@app.get("/cookie/mixed")
def read_cookie_mixed(
    c: Annotated[CookieModel, Cookie()],
    extra: Annotated[str, Cookie()],
):
    return {"c": c.model_dump(), "extra": extra}


client = TestClient(app)


def get_parameter_names(path: str) -> list[str]:
    return [
        param["name"] for param in app.openapi()["paths"][path]["get"]["parameters"]
    ]


def test_query_model_only_still_flattens():
    response = client.get("/query/only", params={"limit": 10, "q": "hello"})
    assert response.status_code == 200
    assert response.json() == {"m": {"limit": 10, "q": "hello"}}


def test_query_model_with_sibling_param():
    response = client.get(
        "/query/mixed", params={"limit": 10, "q": "hello", "extra": 5}
    )
    assert response.status_code == 200
    assert response.json() == {"m": {"limit": 10, "q": "hello"}, "extra": 5}


def test_query_model_with_sibling_param_missing_fields():
    response = client.get("/query/mixed", params={"extra": 5})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["query", "limit"],
        ["query", "q"],
    ]


def test_query_model_with_sibling_param_openapi():
    parameter_names = get_parameter_names("/query/mixed")
    assert parameter_names == ["limit", "q", "extra"]
    assert "m" not in parameter_names


def test_query_openapi_metadata():
    parameters = app.openapi()["paths"]["/query/openapi-metadata"]["get"]["parameters"]
    documented_query = next(
        param for param in parameters if param["name"] == "documented_query"
    )
    assert documented_query["description"] == "Documented query"
    assert documented_query["deprecated"] is True


def test_query_openapi_metadata_runtime():
    response = client.get(
        "/query/openapi-metadata",
        params={"limit": 10, "q": "hello", "documented_query": "value"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "m": {"limit": 10, "q": "hello"},
        "documented_query": "value",
    }


def test_header_model_only_still_flattens():
    response = client.get(
        "/header/only",
        headers=[("x-token", "abc"), ("x-trace", "one"), ("x-trace", "two")],
    )
    assert response.status_code == 200
    assert response.json() == {"h": {"x_token": "abc", "x_trace": ["one", "two"]}}


def test_header_model_with_sibling_param():
    response = client.get(
        "/header/mixed",
        headers=[
            ("x-token", "abc"),
            ("x-trace", "one"),
            ("x-trace", "two"),
            ("extra", "value"),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "h": {"x_token": "abc", "x_trace": ["one", "two"]},
        "extra": "value",
    }


def test_header_model_with_sibling_param_openapi():
    parameter_names = get_parameter_names("/header/mixed")
    assert parameter_names == ["x-token", "x-trace", "extra"]
    assert "h" not in parameter_names


def test_header_model_with_sibling_param_convert_underscores_false():
    response = client.get(
        "/header/mixed-no-convert",
        headers=[
            ("x_token", "abc"),
            ("x_trace", "one"),
            ("x_trace", "two"),
            ("extra", "value"),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "h": {"x_token": "abc", "x_trace": ["one", "two"]},
        "extra": "value",
    }
    parameter_names = get_parameter_names("/header/mixed-no-convert")
    assert parameter_names == ["x_token", "x_trace", "extra"]


def test_header_openapi_metadata_and_hidden_params():
    parameters = app.openapi()["paths"]["/header/openapi-metadata"]["get"]["parameters"]
    parameter_names = [param["name"] for param in parameters]

    assert parameter_names == ["x-token", "x-trace", "documented-header"]

    documented_header = next(
        param for param in parameters if param["name"] == "documented-header"
    )
    assert documented_header["description"] == "Documented header"
    assert documented_header["deprecated"] is True
    assert documented_header["examples"] == {
        "demo": {"summary": "Demo", "value": "abc"}
    }
    assert "hidden-header" not in parameter_names


def test_header_openapi_metadata_runtime():
    response = client.get(
        "/header/openapi-metadata",
        headers=[
            ("x-token", "abc"),
            ("x-trace", "one"),
            ("x-trace", "two"),
            ("hidden-header", "secret"),
            ("documented-header", "shown"),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "h": {"x_token": "abc", "x_trace": ["one", "two"]},
        "hidden_header": "secret",
        "documented_header": "shown",
    }


def test_cookie_model_only_still_flattens():
    with client as c:
        c.cookies.clear()
        c.cookies.set("session_id", "123")
        c.cookies.set("tracker", "abc")
        response = c.get("/cookie/only")
    assert response.status_code == 200
    assert response.json() == {"c": {"session_id": "123", "tracker": "abc"}}


def test_cookie_model_with_sibling_param():
    with client as c:
        c.cookies.clear()
        c.cookies.set("session_id", "123")
        c.cookies.set("tracker", "abc")
        c.cookies.set("extra", "hello")
        response = c.get("/cookie/mixed")
    assert response.status_code == 200
    assert response.json() == {
        "c": {"session_id": "123", "tracker": "abc"},
        "extra": "hello",
    }


def test_cookie_model_with_sibling_param_missing_fields():
    with client as c:
        c.cookies.clear()
        c.cookies.set("extra", "hello")
        response = c.get("/cookie/mixed")
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["cookie", "session_id"],
        ["cookie", "tracker"],
    ]


def test_cookie_model_with_sibling_param_openapi():
    parameter_names = get_parameter_names("/cookie/mixed")
    assert parameter_names == ["session_id", "tracker", "extra"]
    assert "c" not in parameter_names
