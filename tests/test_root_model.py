from datetime import date
from typing import Any, Dict, Generic, List, Optional, Sequence, Type, TypeVar, Union

import pytest
from dirty_equals import IsDict
from fastapi import Body, FastAPI, Header, Path, Query
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .utils import needs_pydanticv2

app = FastAPI()

if PYDANTIC_V2:
    from pydantic import RootModel
else:
    from pydantic import BaseModel

    T = TypeVar("T")

    class RootModel(Generic[T]):
        def __class_getitem__(cls, type_):
            class Inner(BaseModel):
                __root__: type_

            return Inner


Basic = RootModel[int]


class DictWrap(RootModel[Dict[str, int]]):
    pass


if PYDANTIC_V2:
    from pydantic import ConfigDict, Field, field_validator, model_serializer

    class FieldWrap(RootModel[str]):
        model_config = ConfigDict(
            json_schema_extra={"description": "parameter starts with bar_"}
        )
        root: str = Field(pattern=r"^bar_.*$")

    class CustomParsed(RootModel[str]):
        model_config = ConfigDict(
            json_schema_extra={"description": "parameter starts with foo_"}
        )

        @field_validator("root")
        @classmethod
        def validator(cls, v: str) -> str:
            if not v.startswith("foo_"):
                raise ValueError("must start with foo_")
            return v

        @model_serializer
        def serialize(self):
            return (
                self.root
                if self.root.endswith("_serialized")
                else f"{self.root}_serialized"
            )

        def parse(self):
            return self.root[len("foo_") :]  # removeprefix
else:
    from pydantic import validator

    class FieldWrap(BaseModel):
        class Config:
            schema_extra = {"description": "parameter starts with bar_"}

        __root__: str = Field(regex=r"^bar_.*$")

    class CustomParsed(BaseModel):
        class Config:
            schema_extra = {"description": "parameter starts with foo_"}

        __root__: str

        @validator("__root__")
        @classmethod
        def validator(cls, v: str) -> str:
            if not v.startswith("foo_"):
                raise ValueError("must start with foo_")
            return v

        def dict(self, **kwargs: Any) -> Dict[str, Any]:
            return {
                "__root__": self.__root__
                if self.__root__.endswith("_serialized")
                else f"{self.__root__}_serialized"
            }

        def parse(self):
            return self.__root__[len("foo_") :]  # removeprefix


@app.get("/query/basic")
def query_basic(q: Annotated[Basic, Query()]):
    return {"q": q}


@app.get("/query/fieldwrap")
def query_fieldwrap(q: Annotated[FieldWrap, Query()]):
    return {"q": q}


@app.get("/query/customparsed")
def query_customparsed(q: Annotated[CustomParsed, Query()]):
    return {"q": q.parse()}


@app.get("/path/basic/{p}")
def path_basic(p: Annotated[Basic, Path()]):
    return {"p": p}


@app.get("/path/fieldwrap/{p}")
def path_fieldwrap(p: Annotated[FieldWrap, Path()]):
    return {"p": p}


@app.get("/path/customparsed/{p}")
def path_customparsed(p: Annotated[CustomParsed, Path()]):
    return {"p": p.parse()}


@app.post("/body/basic")
def body_basic(b: Annotated[Basic, Body()]):
    return {"b": b}


@app.post("/body/fieldwrap")
def body_fieldwrap(b: Annotated[FieldWrap, Body()]):
    return {"b": b}


@app.post("/body/customparsed")
def body_customparsed(b: Annotated[CustomParsed, Body()]):
    return {"b": b.parse()}


@app.post("/body_default/basic")
def body_default_basic(b: Basic):
    return {"b": b}


@app.post("/body_default/fieldwrap")
def body_default_fieldwrap(b: FieldWrap):
    return {"b": b}


@app.post("/body_default/customparsed")
def body_default_customparsed(b: CustomParsed):
    return {"b": b.parse()}


@app.get("/echo/basic")
def echo_basic(q: Annotated[Basic, Query()]) -> Basic:
    return q


@app.get("/echo/fieldwrap")
def echo_fieldwrap(q: Annotated[FieldWrap, Query()]) -> FieldWrap:
    return q


@app.get("/echo/customparsed")
def echo_customparsed(q: Annotated[CustomParsed, Query()]) -> CustomParsed:
    return q


@app.post("/echo/dictwrap")
def echo_dictwrap(b: DictWrap) -> DictWrap:
    return b.model_dump() if PYDANTIC_V2 else b.dict()["__root__"]


client = TestClient(app)


@pytest.mark.parametrize(
    "url, response_json, request_body",
    [
        ("/query/basic?q=42", {"q": 42}, None),
        ("/query/fieldwrap?q=bar_baz", {"q": "bar_baz"}, None),
        ("/query/customparsed?q=foo_bar", {"q": "bar"}, None),
        ("/path/basic/42", {"p": 42}, None),
        ("/path/fieldwrap/bar_baz", {"p": "bar_baz"}, None),
        ("/path/customparsed/foo_bar", {"p": "bar"}, None),
        ("/body/basic", {"b": 42}, "42"),
        ("/body/fieldwrap", {"b": "bar_baz"}, "bar_baz"),
        ("/body/customparsed", {"b": "bar"}, "foo_bar"),
        ("/body_default/basic", {"b": 42}, "42"),
        ("/body_default/fieldwrap", {"b": "bar_baz"}, "bar_baz"),
        ("/body_default/customparsed", {"b": "bar"}, "foo_bar"),
        ("/echo/basic?q=42", 42, None),
        ("/echo/fieldwrap?q=bar_baz", "bar_baz", None),
        ("/echo/customparsed?q=foo_bar", "foo_bar_serialized", None),
        ("/echo/dictwrap", {"test": 1}, {"test": 1}),
    ],
)
def test_root_model_200(url: str, response_json: Any, request_body: Any):
    response = client.post(url, json=request_body) if request_body else client.get(url)
    assert response.status_code == 200, response.text
    assert response.json() == response_json


@pytest.mark.parametrize("type_", [int, str, bytes, Optional[int]])
@pytest.mark.parametrize("outer", [None, List, Sequence])
def test2_root_model_200__basic(type_: Type, outer: Optional[Type]):
    inner = outer[type_] if outer else type_
    Model = RootModel[inner]

    app2 = FastAPI()

    if outer is None:

        @app2.get("/path/{p}")
        def path_basic2(p: Annotated[Model, Path()]) -> Model:
            return p
    else:
        with pytest.raises(
            AssertionError, match="Path params must be of one of the supported types"
        ):

            @app2.get("/path/{p}")
            def path_basic2(p: Annotated[Model, Path()]) -> Model:
                return p  # pragma: nocover

    @app2.get("/query")
    def query_basic2(q: Annotated[Model, Query()]) -> Model:
        return q

    @app2.get("/header")
    def path_basic2(h: Annotated[Model, Header()]) -> Model:
        return h

    @app2.post("/body")
    def body_basic2(b: Annotated[Model, Body()]) -> Model:
        return b

    client2 = TestClient(app2)

    if outer is None:
        expected = "42" if type_ in (str, bytes) else 42
    else:
        expected = ["42", "43"] if type_ in (str, bytes) else [42, 43]

    if outer is None:
        assert client2.get("/path/42").json() == expected
        assert client2.get("/query?q=42").json() == expected
        assert client2.get("/header", headers={"h": "42"}).json() == expected
    else:
        assert client2.get("/path/42").json()["detail"] == "Not Found"
        assert client2.get("/query?q=42&q=43").json() == expected
        assert (
            client2.get("/header", headers=[("h", "42"), ("h", "43")]).json()
            == expected
        )
    assert client2.post("/body", json=expected).json() == expected


@pytest.mark.parametrize("left", [RootModel[date], date])
@pytest.mark.parametrize("right", [RootModel[int], int])
@needs_pydanticv2
def test_root_model_union(left: Any, right: Any):
    Model = Union[left, right]

    app2 = FastAPI()

    @app2.get("/query")
    def handler1(q: Annotated[Model, Query()]):
        return {"q": q}

    @app2.post("/body")
    def handler2(b: Annotated[Model, Body()]):
        return {"b": b}

    client2 = TestClient(app2)
    for val in ["2025-01-02", 42]:
        response = client2.get(f"/query?q={val}")
        assert response.status_code == 200, response.text
        assert response.json() == {"q": val}
        response = client2.post("/body", json=val)
        assert response.status_code == 200, response.text
        assert response.json() == {"b": val}

    response = client2.get("/query?q=bad")
    assert response.status_code == 422, response.text
    assert {detail["msg"] for detail in response.json()["detail"]} == {
        "Input should be a valid date or datetime, input is too short",
        "Input should be a valid integer, unable to parse string as an integer",
    }


def test_root_model_wraps_root_model():
    if PYDANTIC_V2:

        class Model(RootModel[RootModel[int]]):
            pass
    else:

        class Inner(BaseModel):
            __root__: int

        class Model(BaseModel):
            __root__: Inner

    app2 = FastAPI()

    @app2.get("/query")
    def handler1(q: Annotated[Model, Query()]):
        return {"q": q}

    client2 = TestClient(app2)
    response = client2.get("/query?q=42")
    assert response.status_code == 200, response.text
    assert response.json() == {"q": 42}

    response = client2.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert (
        schema["paths"]["/query"]["get"]["parameters"][0]["schema"]["$ref"]
        == "#/components/schemas/Model"
    )
    if PYDANTIC_V2:
        assert (
            schema["components"]["schemas"]["Model"]["$ref"]
            == "#/components/schemas/RootModel_int_"
        )
        assert schema["components"]["schemas"]["RootModel_int_"]["type"] == "integer"
    else:
        assert (
            schema["components"]["schemas"]["Model"]["$ref"]
            == "#/components/schemas/Inner"
        )
        assert schema["components"]["schemas"]["Inner"]["type"] == "integer"


@pytest.mark.parametrize(
    "url, error_path, request_body",
    [
        ("/query/basic?q=my_bad_not_int", ["query", "q"], None),
        ("/path/basic/my_bad_not_int", ["path", "p"], None),
        ("/body/basic", ["body"], "my_bad_not_int"),
        ("/body_default/basic", ["body"], "my_bad_not_int"),
    ],
)
def test_root_model_basic_422(url: str, error_path: List[str], request_body: Any):
    response = client.post(url, json=request_body) if request_body else client.get(url)
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": error_path,
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "my_bad_not_int",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": [*error_path, "__root__"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "url, error_path, request_body",
    [
        ("/query/fieldwrap?q=my_bad_prefix_val", ["query", "q"], None),
        ("/path/fieldwrap/my_bad_prefix_val", ["path", "p"], None),
        ("/body/fieldwrap", ["body"], "my_bad_prefix_val"),
        ("/body_default/fieldwrap", ["body"], "my_bad_prefix_val"),
    ],
)
def test_root_model_fieldwrap_422(url: str, error_path: List[str], request_body: Any):
    response = client.post(url, json=request_body) if request_body else client.get(url)
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": error_path,
                    "msg": "String should match pattern '^bar_.*$'",
                    "input": "my_bad_prefix_val",
                    "ctx": {"pattern": "^bar_.*$"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": [*error_path, "__root__"],
                    "msg": 'string does not match regex "^bar_.*$"',
                    "type": "value_error.str.regex",
                    "ctx": {"pattern": "^bar_.*$"},
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "url, error_path, request_body",
    [
        ("/query/customparsed?q=my_bad_prefix_val", ["query", "q"], None),
        ("/path/customparsed/my_bad_prefix_val", ["path", "p"], None),
        ("/body/customparsed", ["body"], "my_bad_prefix_val"),
        ("/body_default/customparsed", ["body"], "my_bad_prefix_val"),
    ],
)
def test_root_model_customparsed_422(
    url: str, error_path: List[str], request_body: Any
):
    response = client.post(url, json=request_body) if request_body else client.get(url)
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "value_error",
                    "loc": error_path,
                    "msg": "Value error, must start with foo_",
                    "input": "my_bad_prefix_val",
                    "ctx": {"error": {}},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": [*error_path, "__root__"],
                    "msg": "must start with foo_",
                    "type": "value_error",
                }
            ]
        }
    )


def test_root_model_dictwrap_422():
    response = client.post("/echo/dictwrap", json={"test": "fail_not_int"})
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["body", "test"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "fail_not_int",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "__root__", "test"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "model, path_name, expected_model_schema",
    [
        (Basic, "basic", {"type": "integer"}),
        (
            FieldWrap,
            "fieldwrap",
            {
                "type": "string",
                "pattern": "^bar_.*$",
                "description": "parameter starts with bar_",
            },
        ),
        (
            CustomParsed,
            "customparsed",
            {
                "type": "string",
                "description": "parameter starts with foo_",
            },
        ),
    ],
)
def test_openapi_schema(
    model: Type, path_name: str, expected_model_schema: Dict[str, Any]
):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    paths = response.json()["paths"]
    ref_name = model.__name__.replace("[", "_").replace("]", "_")
    schema_ref = {"schema": {"$ref": f"#/components/schemas/{ref_name}"}}

    assert paths[f"/query/{path_name}"]["get"]["parameters"] == [
        {"in": "query", "name": "q", "required": True, **schema_ref}
    ]
    assert paths[f"/path/{path_name}/{{p}}"]["get"]["parameters"] == [
        {"in": "path", "name": "p", "required": True, **schema_ref}
    ]
    assert paths[f"/body/{path_name}"]["post"]["requestBody"] == {
        "content": {"application/json": schema_ref},
        "required": True,
    }
    assert paths[f"/body_default/{path_name}"]["post"]["requestBody"] == {
        "content": {"application/json": schema_ref},
        "required": True,
    }
    assert paths[f"/echo/{path_name}"]["get"]["responses"]["200"] == {
        "content": {"application/json": schema_ref},
        "description": "Successful Response",
    }

    model_schema = response.json()["components"]["schemas"][ref_name]
    model_schema.pop("title")
    assert model_schema == expected_model_schema


def test_openapi_schema_dictwrap():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    operation = response.json()["paths"]["/echo/dictwrap"]["post"]
    ref = {"schema": {"$ref": "#/components/schemas/DictWrap"}}
    assert operation["requestBody"] == {
        "content": {"application/json": ref},
        "required": True,
    }
    assert operation["responses"]["200"] == {
        "content": {"application/json": ref},
        "description": "Successful Response",
    }
    assert response.json()["components"]["schemas"]["DictWrap"] == {
        "title": "DictWrap",
        "type": "object",
        "additionalProperties": {"type": "integer"},
    }
