from typing import Annotated

import pytest
from fastapi import APIRouter, Cookie, Depends, FastAPI, Header, Query, WebSocket
from fastapi.testclient import TestClient
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, Json, model_validator


def get_with_parameters(client, path, location, parameters):
    if location == "query":
        return client.get(path, params=parameters)
    if location == "header":
        return client.get(path, headers=parameters)
    return client.get(
        path,
        headers={
            "cookie": "; ".join(f"{key}={value}" for key, value in parameters.items())
        },
    )


@pytest.mark.parametrize(
    "marker, location", [(Query, "query"), (Header, "header"), (Cookie, "cookie")]
)
@pytest.mark.parametrize("path", ["/", "/dependency"])
def test_composed_parameter_models_allow_extras(marker, location, path):
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="allow")
        term: str

    class Pagination(BaseModel):
        model_config = ConfigDict(extra="allow")
        limit: int = Field(10, ge=1, description="Page size")

    @app.get("/")
    def read(
        filters: Annotated[Filters, marker()],
        pagination: Annotated[Pagination, marker()],
        host: Annotated[str, marker()] = "testserver",
    ):
        return {"filters": filters, "pagination": pagination, "host": host}

    def filters_dependency(filters: Annotated[Filters, marker()]):
        return filters

    @app.get("/dependency")
    def read_dependency(
        filters: Annotated[Filters, Depends(filters_dependency)],
        pagination: Annotated[Pagination, marker()],
        host: Annotated[str, marker()] = "testserver",
    ):
        return {"filters": filters, "pagination": pagination, "host": host}

    client = TestClient(app)
    client.headers.clear()
    response = get_with_parameters(
        client, path, location, {"term": "hello", "limit": "2", "host": "example.com"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "filters": {"term": "hello", "limit": "2", "host": "example.com"},
        "pagination": {"limit": 2, "term": "hello", "host": "example.com"},
        "host": "example.com",
    }
    response = get_with_parameters(client, path, location, {"term": "hello"})
    assert response.status_code == 200, response.text
    assert response.json()["pagination"]["limit"] == 10
    assert response.json()["pagination"]["term"] == "hello"
    assert response.json()["host"] == "testserver"
    response = get_with_parameters(
        client, path, location, {"term": "hello", "limit": "0"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == [location, "limit"]
    response = get_with_parameters(
        client,
        path,
        location,
        {"term": "hello", "typo": "unexpected", "host": "example.com"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "filters": {"term": "hello", "typo": "unexpected", "host": "example.com"},
        "pagination": {
            "limit": 10,
            "term": "hello",
            "typo": "unexpected",
            "host": "example.com",
        },
        "host": "example.com",
    }
    parameters = app.openapi()["paths"][path]["get"]["parameters"]
    assert {(p["in"], p["name"]) for p in parameters} == {
        (location, "term"),
        (location, "limit"),
        (location, "host"),
    }
    limit = next(p for p in parameters if p["name"] == "limit")
    assert limit["schema"]["minimum"] == 1
    assert limit["schema"]["default"] == 10
    assert limit["description"] == "Page size"
    assert limit["required"] is False


@pytest.mark.parametrize(
    "marker, location", [(Query, "query"), (Header, "header"), (Cookie, "cookie")]
)
@pytest.mark.parametrize("path", ["/", "/dependency"])
def test_composed_parameter_models_forbid_extras(marker, location, path):
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="forbid")
        term: str

    class Pagination(BaseModel):
        model_config = ConfigDict(extra="forbid")
        limit: int = 10

    @app.get("/")
    def read(
        filters: Annotated[Filters, marker()],
        pagination: Annotated[Pagination, marker()],
        host: Annotated[str, marker()] = "testserver",
    ):
        pytest.fail("Invalid parameters reached the endpoint")  # pragma: no cover

    def filters_dependency(filters: Annotated[Filters, marker()]):
        pytest.fail("Invalid parameters reached the dependency")  # pragma: no cover

    @app.get("/dependency")
    def read_dependency(
        filters: Annotated[Filters, Depends(filters_dependency)],
        pagination: Annotated[Pagination, marker()],
        host: Annotated[str, marker()] = "testserver",
    ):
        pytest.fail("Invalid parameters reached the endpoint")  # pragma: no cover

    client = TestClient(app)
    client.headers.clear()
    response = get_with_parameters(
        client, path, location, {"term": "hello", "limit": "2", "host": "example.com"}
    )
    assert response.status_code == 422
    assert {error["loc"][-1] for error in response.json()["detail"]} == {
        "limit",
        "host",
        "term",
    }
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )


def test_parameter_shapes_and_aliases_are_independent():
    app = FastAPI()

    class Many(BaseModel):
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("names", "legacy"))
        ]

    class One(BaseModel):
        text: str = Field(alias="legacy")

    @app.get("/")
    def read(many: Annotated[Many, Query()], one: Annotated[One, Query()], legacy: str):
        return {"many": many, "one": one, "last": legacy}

    response = TestClient(app).get(
        "/", params=[("legacy", "first"), ("legacy", "last")]
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "many": {"names": ["first", "last"]},
        "one": {"legacy": "last"},
        "last": "last",
    }


def test_header_conversion_is_per_model_and_does_not_mutate_cached_fields():
    app = FastAPI()

    class Headers(BaseModel):
        x_id: int
        tags: list[str] = Field(default_factory=list, alias="X-Tags")

    @app.get("/mixed")
    def read(
        converted: Annotated[Headers, Header()],
        literal: Annotated[Headers, Header(convert_underscores=False)],
    ):
        return {"converted": converted, "literal": literal}

    @app.get("/query")
    def read_query(data: Annotated[Headers, Query()]):
        return data

    client = TestClient(app)
    response = client.get(
        "/mixed",
        headers=[("X-Id", "1"), ("x_id", "2"), ("X-Tags", "a"), ("x-tags", "b")],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "converted": {"x_id": 1, "X-Tags": ["a", "b"]},
        "literal": {"x_id": 2, "X-Tags": ["a", "b"]},
    }
    schema = app.openapi()
    assert {p["name"] for p in schema["paths"]["/mixed"]["get"]["parameters"]} == {
        "x-id",
        "x_id",
        "X-Tags",
    }
    assert {p["name"] for p in schema["paths"]["/query"]["get"]["parameters"]} == {
        "x_id",
        "X-Tags",
    }
    response = client.get("/query", params={"x_id": "3", "X-Tags": ["c", "d"]})
    assert response.status_code == 200, response.text
    assert response.json() == {"x_id": 3, "X-Tags": ["c", "d"]}
    response = client.get("/mixed", headers={"x-id": "bad", "x_id": "also-bad"})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["header", "x-id"],
        ["header", "x_id"],
    ]
    assert Headers.model_fields["x_id"].alias is None


def test_model_validators_defaults_and_unknown_extras():
    app = FastAPI()

    class Range(BaseModel):
        model_config = ConfigDict(extra="allow")
        start: int = 0
        end: int = 10
        tags: list[str] = Field(default_factory=list)

        @model_validator(mode="after")
        def check_range(self):
            if self.start > self.end:
                raise ValueError("start must not exceed end")
            return self

    @app.get("/")
    def read(data: Annotated[Range, Query()], order: str = "asc"):
        return {
            "data": data,
            "fields_set": sorted(data.model_fields_set),
            "order": order,
        }

    client = TestClient(app)
    response = client.get("/", params={"order": "desc", "note": ["a", "b"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "data": {
            "start": 0,
            "end": 10,
            "tags": [],
            "note": ["a", "b"],
            "order": "desc",
        },
        "fields_set": ["note", "order"],
        "order": "desc",
    }
    response = client.get("/", params={"start": "20"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query"]


def test_dependency_overrides_and_router_parameters():
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="forbid")
        term: str

    def pagination(limit: int = 10):
        return limit

    def replacement(page: int = 1):
        return page

    def token(token: str = "secret"):
        return token

    router = APIRouter(dependencies=[Depends(token)])

    @router.get("/")
    def read(
        filters: Annotated[Filters, Query()],
        page: Annotated[int, Depends(pagination)],
    ):
        return {"filters": filters, "page": page}

    app.include_router(router)
    client = TestClient(app)
    response = client.get("/", params={"term": "a"})
    assert response.status_code == 200, response.text
    assert response.json() == {"filters": {"term": "a"}, "page": 10}
    response = client.get("/", params={"term": "a", "limit": "2", "token": "secret"})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["query", "limit"],
        ["query", "token"],
    ]
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )
    app.dependency_overrides[pagination] = replacement
    response = client.get("/", params={"term": "a", "page": "3", "token": "secret"})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["query", "page"],
        ["query", "token"],
    ]
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )


def test_parameter_models_keep_request_locations_separate():
    app = FastAPI()

    class Model(BaseModel):
        value: int

    @app.get("/")
    def read(
        query: Annotated[Model, Query()],
        header: Annotated[Model, Header()],
        cookie: Annotated[Model, Cookie()],
    ):
        return {"query": query, "header": header, "cookie": cookie}

    response = TestClient(app).get(
        "/", params={"value": "1"}, headers={"value": "2", "cookie": "value=3"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "query": {"value": 1},
        "header": {"value": 2},
        "cookie": {"value": 3},
    }
    parameters = app.openapi()["paths"]["/"]["get"]["parameters"]
    assert {(param["in"], param["name"]) for param in parameters} == {
        ("query", "value"),
        ("header", "value"),
        ("cookie", "value"),
    }


@pytest.mark.parametrize("marker", [Header, Cookie])
def test_other_locations_do_not_allow_extra_query_parameters(marker):
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="forbid")
        term: str

    @app.get("/")
    def read(
        filters: Annotated[Filters, Query()], limit: Annotated[int, marker()] = 10
    ):
        return filters

    client = TestClient(app)
    response = client.get("/", params={"term": "a"})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "a"}
    response = client.get("/", params={"term": "a", "limit": "2"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "limit"]
    assert response.json()["detail"][0]["type"] == "extra_forbidden"


def test_hidden_model_and_shared_required_parameter():
    app = FastAPI()

    class Optional(BaseModel):
        shared: int = 1

    class Required(BaseModel):
        shared: int

    class Hidden(BaseModel):
        secret: str

    @app.get("/")
    def read(
        optional: Annotated[Optional, Query()],
        required: Annotated[Required, Query()],
        hidden: Annotated[Hidden, Query(include_in_schema=False)],
    ):
        return [optional, required, hidden]

    client = TestClient(app)
    response = client.get("/", params={"shared": "2", "secret": "ok"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"shared": 2}, {"shared": 2}, {"secret": "ok"}]
    assert client.get("/", params={"secret": "ok"}).status_code == 422
    parameters = app.openapi()["paths"]["/"]["get"]["parameters"]
    assert len(parameters) == 1
    assert parameters[0]["name"] == "shared"
    assert parameters[0]["required"] is True


def test_shared_alias_choices_still_validate_unused_choices_as_extras():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: Annotated[int, Field(validation_alias=AliasChoices("first", "second"))]

    @app.get("/")
    def read(model: Annotated[Model, Query()], second: int = 0):
        return model

    client = TestClient(app)
    assert client.get("/", params={"second": "2"}).json() == {"value": 2}
    response = client.get("/", params={"first": "1", "second": "2"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "second"]


@pytest.mark.parametrize(
    "marker, location", [(Query, "query"), (Header, "header"), (Cookie, "cookie")]
)
def test_explicit_json_model_stays_a_single_parameter(marker, location):
    app = FastAPI()

    class Model(BaseModel):
        value: int

    @app.get("/")
    def read(
        data: Annotated[Json[Model], marker()], limit: Annotated[int, marker()] = 10
    ):
        return {"data": data, "limit": limit}

    client = TestClient(app)
    data = '{"value": 2}'
    if location == "query":
        response = client.get("/", params={"data": data})
    elif location == "header":
        response = client.get("/", headers={"data": data})
    else:
        response = client.get("/", headers={"cookie": f"data={data}"})
    assert response.status_code == 200, response.text
    assert response.json() == {"data": {"value": 2}, "limit": 10}
    assert {p["name"] for p in app.openapi()["paths"]["/"]["get"]["parameters"]} == {
        "data",
        "limit",
    }


def test_nested_dependencies_and_websocket_parameter_models():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        term: str
        limit: int = 10

    def filters(data: Annotated[Model, Query()]):
        return data

    def nested(data: Annotated[Model, Depends(filters)]):
        return data

    @app.websocket("/ws")
    async def read(
        websocket: WebSocket, data: Annotated[Model, Depends(nested)], limit: int = 10
    ):
        await websocket.accept()
        await websocket.send_json({"term": data.term, "limit": limit})
        await websocket.close()

    with TestClient(app).websocket_connect("/ws?term=a&limit=2") as websocket:
        assert websocket.receive_json() == {"term": "a", "limit": 2}
