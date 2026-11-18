from typing import Annotated

import pytest
from fastapi import APIRouter, Depends, FastAPI, Form, Request
from fastapi._form_limits import _FormLimits
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


async def field(text: Annotated[str, Form()]):
    return text


def test_nested_and_reused_router_limits():
    # Each level contributes a different setting. Reusing the router must not
    # change the configuration of its other inclusions.
    child = APIRouter(form_limits={"max_fields": 1})
    child.post("/", form_limits={"max_part_size": 3})(field)
    parent = APIRouter()
    parent.include_router(child, form_limits={"max_fields": 4})
    app = FastAPI(form_limits={"max_part_size": 1})
    app.include_router(parent, prefix="/one", form_limits={"max_files": 0})
    app.include_router(parent, prefix="/two", form_limits={"max_files": 1})
    client = TestClient(app)
    payload = [("text", (None, "abc")), ("file", ("f", b"12345"))]
    assert client.post("/one/", files=payload).status_code == 400
    assert client.post("/two/", files=payload).json() == "abc"
    assert (
        client.post("/two/", files=[*payload, ("text", (None, "z"))]).status_code == 400
    )
    assert client.post("/two/", files={"text": (None, "abcd")}).status_code == 400
    assert client.post("/one/", files=payload).status_code == 400


def test_mounted_app_and_direct_route():
    route = APIRoute("/", field, methods=["POST"], form_limits={"max_fields": 1})
    child = FastAPI(routes=[route])
    app = FastAPI(form_limits={"max_part_size": 2, "max_fields": 0})
    app.mount("/child", child)
    client = TestClient(app)
    assert client.post("/child/", files={"text": (None, "ab")}).json() == "ab"
    assert client.post("/child/", files={"text": (None, "abc")}).status_code == 400


@pytest.mark.parametrize("included", [False, True])
def test_route_scope_preserves_inherited_form_limits(included):
    class RouteWithMetadata(APIRoute):
        def matches(self, scope):
            match, child_scope = super().matches(scope)
            child_scope["fastapi"] = {"custom": True}
            return match, child_scope

    async def endpoint(request: Request, text: Annotated[str, Form()]):
        return [text, request.scope["fastapi"]["custom"]]

    route = RouteWithMetadata("/", endpoint, methods=["POST"])
    app = FastAPI(form_limits={"max_fields": 1}, routes=[] if included else [route])
    if included:
        app.include_router(APIRouter(routes=[route]))
    client = TestClient(app)
    assert client.post("/", data={"text": "ok"}).json() == ["ok", True]
    assert client.post("/", data={"text": "ok", "extra": "v"}).status_code == 400


def test_dependency_parses_once_and_preserves_body_limit():
    app = FastAPI(form_limits={"max_fields": 1}, max_body_size=25)

    @app.post("/")
    async def endpoint(request: Request, text: Annotated[str, Depends(field)]):
        cached = await request.form(max_fields=0)
        return cached["text"] == text

    client = TestClient(app)
    assert client.post("/", data={"text": "ok"}).json() is True
    assert client.post("/", data={"text": "ok", "extra": "v"}).status_code == 400
    assert client.post("/", data={"text": "x" * 30}).status_code == 413


@pytest.mark.parametrize(
    "limits",
    [
        {"max_parts": 1},
        {"max_files": -1},
        {"max_fields": False},
        {"max_part_size": 1.5},
    ],
)
def test_invalid_configuration(limits):
    with pytest.raises(ValueError):
        FastAPI(form_limits=limits)


def test_invalid_route_and_inclusion_limits():
    with pytest.raises(ValueError, match="max_fields"):
        FastAPI().include_router(APIRouter(), form_limits={"max_fields": -1})
    with pytest.raises(ValueError, match="max_fields"):
        APIRoute("/", field, form_limits={"max_fields": -1})


def test_caller_settings_are_copied():
    limits: _FormLimits = {"max_fields": 1}
    app = FastAPI(form_limits=limits)
    limits["max_fields"] = 0
    app.post("/")(field)
    assert TestClient(app).post("/", data={"text": "ok"}).json() == "ok"


def test_manual_form_parsing_uses_explicit_limits():
    app = FastAPI(form_limits={"max_fields": 0})

    @app.post("/")
    async def manual(request: Request):
        async with request.form(max_fields=1) as form:
            return form["text"]

    client = TestClient(app)
    assert client.post("/", data={"text": "ok"}).json() == "ok"
    assert client.post("/", data={"text": "ok", "extra": "v"}).status_code == 400
