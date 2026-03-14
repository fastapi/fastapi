from typing import Annotated, Any, Callable

import pytest
from fastapi import APIRouter, Cookie, FastAPI, Header, Query, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()
client = TestClient(app)


class NameModel(BaseModel):
    name: str


class AgeModel(BaseModel):
    age: int


def add_routes(
    in_: Callable[..., Any],
    prefix: str,
) -> None:
    router = APIRouter(prefix=prefix)

    @router.get("/models")
    async def route_models(
        name_model: Annotated[NameModel, in_()],
        age_model: Annotated[AgeModel, in_()],
    ):
        return {
            "name": name_model.name,
            "age": age_model.age,
        }

    @router.get("/mixed")
    async def route_mixed(
        name_model: Annotated[NameModel, in_()],
        age: Annotated[int, in_()],
    ):
        return {
            "name": name_model.name,
            "age": age,
        }

    app.include_router(router)


add_routes(Query, "/query")
add_routes(Header, "/header")
add_routes(Cookie, "/cookie")


@pytest.mark.parametrize(
    ("in_", "prefix", "call_arg"),
    [
        (Query, "/query", "params"),
        (Header, "/header", "headers"),
        (Cookie, "/cookie", "cookies"),
    ],
    ids=[
        "query",
        "header",
        "cookie",
    ],
)
@pytest.mark.parametrize(
    "type_",
    [
        "models",
        "mixed",
    ],
    ids=[
        "models",
        "mixed",
    ],
)
def test_multiple_params(in_, prefix, call_arg, type_):
    params = {"name": "John", "age": "42"}
    kwargs = {}

    if call_arg == "cookies":
        client.cookies = params
    else:
        kwargs[call_arg] = params

    response = client.get(f"{prefix}/{type_}", **kwargs)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "John", "age": 42}


@pytest.mark.parametrize(
    ("prefix", "in_"),
    [
        ("/query", "query"),
        ("/header", "header"),
        ("/cookie", "cookie"),
    ],
    ids=[
        "query",
        "header",
        "cookie",
    ],
)
@pytest.mark.parametrize(
    "type_",
    [
        "models",
        "mixed",
    ],
    ids=[
        "models",
        "mixed",
    ],
)
def test_openapi_schema(prefix, in_, type_):
    response = client.get("/openapi.json")

    assert response.status_code == status.HTTP_200_OK

    schema = response.json()
    assert schema["paths"][f"{prefix}/{type_}"]["get"]["parameters"] == [
        {
            "required": True,
            "in": in_,
            "name": "name",
            "schema": {"title": "Name", "type": "string"},
        },
        {
            "required": True,
            "in": in_,
            "name": "age",
            "schema": {"title": "Age", "type": "integer"},
        },
    ]
