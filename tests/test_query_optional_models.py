from typing import Annotated, Optional

import pytest
from fastapi import Depends, FastAPI, Query, WebSocket
from fastapi.testclient import TestClient
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


def test_optional_query_model():
    app = FastAPI()

    class Filters(BaseModel):
        start: int
        end: int
        tags: list[str] = Field(default_factory=list)
        enabled: bool = True
        label: str = "default"

        @model_validator(mode="after")
        def check_range(self):
            if self.start > self.end:
                raise ValueError("start must not exceed end")
            return self

    @app.get("/")
    def read(filters: Annotated[Filters | None, Query()] = None):
        return filters

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.get(
        "/", params={"start": "0", "end": "10", "tags": ["a", "b"], "label": ""}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "start": 0,
        "end": 10,
        "tags": ["a", "b"],
        "enabled": True,
        "label": "",
    }
    response = client.get("/", params={"start": "", "end": "10"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "start"]
    assert response.json()["detail"][0]["type"] == "int_parsing"
    for fields in ({"label": ""}, {"tags": "a"}, {"enabled": "false"}):
        response = client.get("/", params=fields)
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["query", "start"],
            ["query", "end"],
        ]
    response = client.get("/", params={"start": "20", "end": "10"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query"]
    assert response.json()["detail"][0]["type"] == "value_error"


def test_optional_models_with_dependencies_and_individual_parameters():
    app = FastAPI()

    class Range(BaseModel):
        start: int
        end: int

    class Filters(BaseModel):
        tags: list[str]

    def get_filters(filters: Annotated[Filters | None, Query()] = None):
        return filters

    @app.get("/")
    def read(
        filters: Annotated[Filters | None, Depends(get_filters)],
        date_range: Annotated[Range | None, Query()] = None,
        limit: int = 10,
    ):
        return {"range": date_range, "filters": filters, "limit": limit}

    client = TestClient(app)
    response = client.get("/", params={"limit": "5"})
    assert response.status_code == 200, response.text
    assert response.json() == {"range": None, "filters": None, "limit": 5}
    response = client.get("/", params={"start": "0", "end": "10"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "range": {"start": 0, "end": 10},
        "filters": None,
        "limit": 10,
    }
    response = client.get("/", params={"tags": ["a", "b"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "range": None,
        "filters": {"tags": ["a", "b"]},
        "limit": 10,
    }
    response = client.get("/", params={"start": "0", "end": "10", "tags": "a"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "range": {"start": 0, "end": 10},
        "filters": {"tags": ["a"]},
        "limit": 10,
    }
    response = client.get("/", params={"start": "0", "tags": "a"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "end"]
    parameters = app.openapi()["paths"]["/"]["get"]["parameters"]
    assert {param["name"]: param["required"] for param in parameters} == {
        "start": False,
        "end": False,
        "tags": False,
        "limit": False,
    }


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
@pytest.mark.parametrize(
    "fields", [{"limit": "5"}, {"limit": "5", "unknown": ["a", "b"]}]
)
def test_unknown_parameters(extra, fields):
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra=extra)
        term: str = "default"

    @app.get("/")
    def read(filters: Annotated[Filters | None, Query()] = None, limit: int = 10):
        return filters

    client = TestClient(app)
    assert client.get("/").json() is None
    response = client.get("/", params=fields)
    if extra == "forbid":
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["query", name] for name in fields
        ]
        assert all(
            error["type"] == "extra_forbidden" for error in response.json()["detail"]
        )
    else:
        assert response.status_code == 200, response.text
        assert response.json() == (
            {"term": "default", **fields} if extra == "allow" else None
        )


def test_allowed_extras_require_model_fields():
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="allow")
        term: str

    @app.get("/")
    def read(filters: Annotated[Filters | None, Query()] = None):
        return filters

    client = TestClient(app)
    response = client.get("/", params={"unknown": "value"})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "type": "missing",
            "loc": ["query", "term"],
            "msg": "Field required",
            "input": {"unknown": "value"},
        }
    ]
    response = client.get("/", params={"term": "search", "unknown": "value"})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "search", "unknown": "value"}


def test_nullable_model_without_default_is_required():
    app = FastAPI()

    class Filters(BaseModel):
        term: str = "default"

    @app.get("/")
    def read(filters: Annotated[Filters | None, Query()]):
        return filters

    @app.get("/plain")
    def read_plain(filters: Annotated[Filters, Query()]):
        return filters

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"type": "missing", "loc": ["query"], "msg": "Field required", "input": None}
    ]
    response = client.get("/", params={"term": ""})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": ""}
    response = client.get("/plain")
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "default"}


def test_defaults_factories_and_validators():
    app = FastAPI()
    calls = []

    class Filters(BaseModel):
        term: str
        tags: list[str] = Field(default_factory=list)

        @model_validator(mode="after")
        def validate_term(self):
            calls.append(self.term)
            return self

    default = Filters(term="parameter default")

    def factory():
        calls.append("factory")
        return Filters(term="factory default")

    @app.get("/")
    def read(filters: Annotated[Filters | None, Query()] = default):
        assert filters is not None
        filters.tags.append("new")
        return filters

    @app.get("/factory")
    def read_factory(
        filters: Annotated[Filters | None, Query(default_factory=factory)],
    ):
        return filters

    @app.get("/validated-default")
    def read_validated_default(
        filters: Annotated[Filters | None, Query(validate_default=True)] = default,
    ):
        return filters

    client = TestClient(app)
    calls.clear()
    for _ in range(2):
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == {"term": "parameter default", "tags": ["new"]}
    assert default.tags == []
    assert calls == []
    for _ in range(2):
        response = client.get("/factory")
        assert response.status_code == 200, response.text
        assert response.json() == {"term": "factory default", "tags": []}
    assert calls == ["factory", "factory default", "factory", "factory default"]
    calls.clear()
    response = client.get("/factory", params={"term": "submitted"})
    assert response.status_code == 200, response.text
    assert calls == ["submitted"]
    calls.clear()
    response = client.get("/validated-default")
    assert response.status_code == 200, response.text
    assert calls == ["parameter default"]
    for operation in app.openapi()["paths"].values():
        assert not any(param["required"] for param in operation["get"]["parameters"])


@pytest.mark.parametrize("key", ["q", "search", "term"])
def test_aliases_and_shared_fields(key):
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="forbid", populate_by_name=True)
        term: str = Field(validation_alias=AliasChoices("q", "search"))

    class Other(BaseModel):
        term: str
        limit: int

    @app.get("/")
    def read(
        filters: Annotated[Filters | None, Query()] = None,
        other: Annotated[Other | None, Query()] = None,
    ):
        return [filters, other]

    client = TestClient(app)
    response = client.get("/", params={key: "value"})
    if key == "term":
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["query", "limit"]
    else:
        assert response.status_code == 200, response.text
        assert response.json() == [{"term": "value"}, None]
    response = client.get("/", params={key: "value", "term": "value", "limit": "5"})
    assert response.status_code == 422
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )
    assert response.json()["detail"][-1]["loc"] == ["query", "limit"]


def test_dependency_override_names():
    app = FastAPI()

    class Filters(BaseModel):
        model_config = ConfigDict(extra="forbid")
        term: str

    def pagination(limit: int = 10):
        return limit

    def replacement(page: int = 1):
        return page

    @app.get("/")
    def read(
        page: Annotated[int, Depends(pagination)],
        filters: Annotated[Filters | None, Query()] = None,
    ):
        return filters

    client = TestClient(app)
    assert client.get("/").json() is None
    response = client.get("/", params={"limit": "5"})
    assert response.status_code == 422
    assert response.json()["detail"][-1]["loc"] == ["query", "limit"]
    app.dependency_overrides[pagination] = replacement
    response = client.get("/", params={"page": "2"})
    assert response.status_code == 422
    assert response.json()["detail"][-1]["loc"] == ["query", "page"]
    assert response.json()["detail"][-1]["type"] == "extra_forbidden"


def test_openapi_required_fields_are_not_mutated():
    app = FastAPI()

    class Filters(BaseModel):
        term: str = Field(alias="q", description="Search term")
        limit: int = Field(10, ge=1)

    @app.get("/optional", response_model=Filters | None)
    def read_optional(filters: Annotated[Filters | None, Query()] = None):
        return filters

    @app.get("/required")
    def read_required(filters: Annotated[Filters | None, Query()]):
        return filters

    @app.get("/plain")
    def read_plain(filters: Annotated[Filters, Query()]):
        return filters

    schema = app.openapi()
    assert schema["paths"]["/optional"]["get"]["parameters"] == [
        {
            "name": "q",
            "in": "query",
            "required": False,
            "schema": {"type": "string", "description": "Search term", "title": "Q"},
            "description": "Search term",
        },
        {
            "name": "limit",
            "in": "query",
            "required": False,
            "schema": {
                "type": "integer",
                "minimum": 1,
                "default": 10,
                "title": "Limit",
            },
        },
    ]
    client = TestClient(app)
    response = client.get("/optional")
    assert response.status_code == 200, response.text
    assert response.json() is None
    for path in ("/required", "/plain"):
        assert schema["paths"][path]["get"]["parameters"][0]["required"] is True
        response = client.get(path)
        assert response.status_code == 422
        response = client.get(path, params={"q": "value"})
        assert response.status_code == 200, response.text
        assert response.json() == {"q": "value", "limit": 10}
    assert schema["components"]["schemas"]["Filters"]["required"] == ["q"]
    assert Filters.model_fields["term"].is_required()


def test_shared_required_parameter_and_hidden_model():
    app = FastAPI()

    class Filters(BaseModel):
        term: str
        limit: int

    @app.get("/")
    def read(term: str, filters: Annotated[Filters | None, Query()] = None):
        return filters

    @app.get("/hidden")
    def read_hidden(
        filters: Annotated[Filters | None, Query(include_in_schema=False)] = None,
    ):
        return filters

    schema = app.openapi()
    assert {
        p["name"]: p["required"] for p in schema["paths"]["/"]["get"]["parameters"]
    } == {
        "term": True,
        "limit": False,
    }
    assert "parameters" not in schema["paths"]["/hidden"]["get"]
    client = TestClient(app)
    response = client.get("/", params={"term": "value"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "limit"]
    response = client.get("/", params={"term": "value", "limit": "5"})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": "value", "limit": 5}
    response = client.get("/hidden")
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_typing_optional():
    app = FastAPI()

    class Filters(BaseModel):
        term: str

    @app.get("/")
    def read(filters: Optional[Filters] = Query(default=None)):  # noqa: UP045
        return filters

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.get("/", params={"term": ""})
    assert response.status_code == 200, response.text
    assert response.json() == {"term": ""}


def test_optional_query_model_in_websocket():
    app = FastAPI()

    class Filters(BaseModel):
        term: str

    @app.websocket("/ws")
    async def read(
        websocket: WebSocket,
        filters: Annotated[Filters | None, Query()] = None,
    ):
        await websocket.accept()
        await websocket.send_json(filters.model_dump() if filters is not None else None)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        assert websocket.receive_json() is None
    with client.websocket_connect("/ws?term=value") as websocket:
        assert websocket.receive_json() == {"term": "value"}
