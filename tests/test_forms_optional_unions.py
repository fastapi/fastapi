from typing import Annotated, Literal, Optional

import pytest
from fastapi import Depends, FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    Tag,
    model_validator,
)

app = FastAPI()


class TextForm(BaseModel):
    kind: Literal["text"]
    value: str
    enabled: bool = True


class ListForm(BaseModel):
    kind: Literal["list"]
    value: list[str]


@app.post("/union")
def read_union(data: Annotated[TextForm | ListForm | None, Form()] = None):
    return data


@app.post("/discriminated")
def read_discriminated(
    data: Annotated[TextForm | ListForm | None, Form(discriminator="kind")] = None,
):
    return data


client = TestClient(app)


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
def test_absent_union(path):
    response = client.post(path)
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post(path, data={"unknown": "ignored"})
    assert response.status_code == 200, response.text
    assert response.json() is None


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
def test_supplied_union(path):
    response = client.post(path, data={"kind": "text", "value": "hello"})
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "text", "value": "hello", "enabled": False}
    response = client.post(path, data={"kind": "list", "value": ["", "blue"]})
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "list", "value": ["", "blue"]}


@pytest.mark.parametrize(
    "path,branch", [("/union", "TextForm"), ("/discriminated", "text")]
)
@pytest.mark.parametrize("data", [{"kind": "text"}, {"kind": "text", "value": ""}])
def test_partial_and_empty_fields(path, branch, data):
    response = client.post(path, data=data)
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", branch, "value"]


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
def test_multipart_union(path):
    response = client.post(path, files={"unknown": (None, "ignored")})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post(
        path,
        files=[
            ("kind", (None, "list")),
            ("value", (None, "")),
            ("value", (None, "blue")),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "list", "value": ["", "blue"]}
    response = client.post(path, files={"kind": (None, "text"), "value": (None, "")})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


@pytest.mark.parametrize(
    "data,error_type",
    [
        ({"value": "hello"}, "union_tag_not_found"),
        ({"value": ""}, "union_tag_not_found"),
        ({"enabled": "false"}, "union_tag_not_found"),
        ({"kind": ""}, "union_tag_invalid"),
        ({"kind": "unknown"}, "union_tag_invalid"),
    ],
)
def test_discriminator_errors(data, error_type):
    response = client.post("/discriminated", data=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == error_type
    assert response.json()["detail"][0]["loc"] == ["body"]


def test_nullable_union_without_default_is_required():
    app = FastAPI()

    class Count(BaseModel):
        count: int = 1

    class Label(BaseModel):
        label: str = "default"

    @app.post("/")
    def read(data: Annotated[Count | Label | None, Form()]):
        return data

    client = TestClient(app)
    for fields in ({}, {"unknown": "ignored"}):
        response = client.post("/", data=fields)
        assert response.status_code == 422
        assert response.json()["detail"] == [
            {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
        ]
    response = client.post("/", data={"count": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"count": 2}
    schema = app.openapi()
    assert schema["paths"]["/"]["post"]["requestBody"]["required"] is True
    assert schema["components"]["schemas"]["Body_read__post"]["allOf"] == [
        {"not": {"not": {"anyOf": [{"required": ["count"]}, {"required": ["label"]}]}}},
        {
            "anyOf": [
                {"$ref": "#/components/schemas/Count"},
                {"$ref": "#/components/schemas/Label"},
            ],
            "title": "Data",
        },
    ]


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
def test_unknown_fields(extra):
    app = FastAPI()

    class Count(BaseModel):
        model_config = ConfigDict(extra=extra)
        count: int = 1

    class Label(BaseModel):
        model_config = ConfigDict(extra=extra)
        label: str = "default"

    @app.post("/")
    def read(
        data: Annotated[Count | Label | None, Form(union_mode="left_to_right")] = None,
    ):
        return data

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"unknown": ["a", "b"]})
    if extra == "forbid":
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["body", "Count", "unknown"],
            ["body", "Label", "unknown"],
        ]
        assert all(
            error["type"] == "extra_forbidden" for error in response.json()["detail"]
        )
    else:
        assert response.status_code == 200, response.text
        assert response.json() == (
            {"count": 1, "unknown": ["a", "b"]} if extra == "allow" else None
        )
    schema = app.openapi()
    assert "required" not in schema["paths"]["/"]["post"]["requestBody"]
    absent = (
        {"maxProperties": 0}
        if extra in ("allow", "forbid")
        else {"not": {"anyOf": [{"required": ["count"]}, {"required": ["label"]}]}}
    )
    assert schema["components"]["schemas"]["Body_read__post"]["allOf"] == [
        {
            "anyOf": [
                absent,
                {
                    "anyOf": [
                        {"$ref": "#/components/schemas/Count"},
                        {"$ref": "#/components/schemas/Label"},
                    ],
                    "title": "Data",
                },
            ]
        }
    ]


def test_mixed_extra_configurations_activate_union():
    app = FastAPI()

    class Ignored(BaseModel):
        name: str

    class Allowed(BaseModel):
        model_config = ConfigDict(extra="allow")
        count: int = 1

    @app.post("/")
    def read(data: Annotated[Ignored | Allowed | None, Form()] = None):
        return data

    response = TestClient(app).post("/", data={"unknown": "value"})
    assert response.status_code == 200, response.text
    assert response.json() == {"count": 1, "unknown": "value"}


@pytest.mark.parametrize("name", ["full_name", "name"])
def test_aliases_activate_union(name):
    app = FastAPI()

    class AliasedForm(BaseModel):
        name: str = Field(validation_alias=AliasChoices("full_name", "name"))

    @app.post("/")
    def read(data: Annotated[AliasedForm | ListForm | None, Form()] = None):
        return data

    client = TestClient(app)
    response = client.post("/", data={"unknown": "ignored"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={name: "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick"}


@pytest.mark.parametrize("name", ["full_name", "name"])
def test_aliases_and_forbidden_extras(name):
    app = FastAPI()

    class Person(BaseModel):
        model_config = ConfigDict(extra="forbid")
        kind: Literal["person"] = Field(alias="type")
        name: str = Field(validation_alias=AliasChoices("full_name", "name"))

    class Company(BaseModel):
        model_config = ConfigDict(extra="forbid")
        kind: Literal["company"] = Field(alias="type")
        company_name: str

    @app.post("/")
    def read(
        data: Annotated[Person | Company | None, Form(discriminator="kind")] = None,
    ):
        return data

    client = TestClient(app)
    response = client.post("/", data={name: "Rick"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "union_tag_not_found"
    response = client.post("/", data={"type": "person", name: "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"type": "person", "name": "Rick"}
    response = client.post(
        "/", data={"type": "person", name: "Rick", "company_name": "Acme"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "extra_forbidden"
    assert response.json()["detail"][0]["loc"] == ["body", "person", "company_name"]


def test_branch_tags_and_before_validator():
    app = FastAPI()
    calls = []

    def copy_input(data):
        calls.append(data.copy())
        return data.copy()

    @app.post("/")
    def read(
        data: Annotated[
            Annotated[TextForm, Tag("text")] | Annotated[ListForm, Tag("list")] | None,
            BeforeValidator(copy_input),
            Form(),
        ] = None,
    ):
        return data

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    assert calls == []
    response = client.post("/", data={"kind": "list", "value": ["", "blue"]})
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "list", "value": ["", "blue"]}
    assert calls == [{"kind": "list", "value": ["", "blue"]}]
    response = client.post("/", data={"kind": "text", "value": ""})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["body", "text", "value"],
        ["body", "list", "kind"],
    ]


def test_defaults_factories_and_validators():
    app = FastAPI()
    calls = []

    class Defaults(BaseModel):
        kind: Literal["defaults"] = "defaults"
        tags: list[str] = Field(default_factory=list)
        enabled: bool = True

        @model_validator(mode="after")
        def record_validation(self):
            calls.append("validated")
            return self

    default = Defaults()

    def factory():
        calls.append("factory")
        return Defaults()

    @app.post("/default")
    def read_default(data: Annotated[Defaults | TextForm | None, Form()] = default):
        assert isinstance(data, Defaults)
        data.tags.append("new")
        return data

    @app.post("/factory")
    def read_factory(
        data: Annotated[Defaults | TextForm | None, Form(default_factory=factory)],
    ):
        return data

    @app.post("/validated-default")
    def read_validated_default(
        data: Annotated[
            Defaults | TextForm | None, Form(validate_default=True)
        ] = default,
    ):
        return data

    client = TestClient(app)
    calls.clear()
    for _ in range(2):
        response = client.post("/default")
        assert response.status_code == 200, response.text
        assert response.json() == {"kind": "defaults", "tags": ["new"], "enabled": True}
    assert default.tags == []
    assert calls == []
    response = client.post("/factory")
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "defaults", "tags": [], "enabled": True}
    assert calls == ["factory", "validated"]
    calls.clear()
    response = client.post("/factory", data={"kind": "defaults"})
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "defaults", "tags": [], "enabled": False}
    assert calls == ["validated"]
    calls.clear()
    response = client.post("/validated-default")
    assert response.status_code == 200, response.text
    assert calls == ["validated"]
    schema = app.openapi()
    for path in ("/default", "/factory", "/validated-default"):
        assert "required" not in schema["paths"][path]["post"]["requestBody"]
    assert calls == ["validated"]


def test_optional_union_in_dependency():
    app = FastAPI()

    def get_form(
        data: Optional[TextForm | ListForm] = Form(default=None),  # noqa: UP045
    ):
        return data

    @app.post("/")
    def read(data: Annotated[TextForm | ListForm | None, Depends(get_form)]):
        return data

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"kind": "text", "value": "hello"})
    assert response.status_code == 200, response.text
    assert response.json() == {"kind": "text", "value": "hello", "enabled": False}


def test_openapi():
    schema = app.openapi()
    schemas = schema["components"]["schemas"]
    absent = {
        "not": {
            "anyOf": [
                {"required": ["enabled"]},
                {"required": ["kind"]},
                {"required": ["value"]},
            ]
        }
    }
    assert schema["paths"]["/union"]["post"]["requestBody"] == {
        "content": {
            "application/x-www-form-urlencoded": {
                "schema": {"$ref": "#/components/schemas/Body_read_union_union_post"}
            }
        }
    }
    assert schemas["Body_read_union_union_post"]["allOf"] == [
        {
            "anyOf": [
                absent,
                {
                    "anyOf": [
                        {"$ref": "#/components/schemas/TextForm"},
                        {"$ref": "#/components/schemas/ListForm"},
                    ],
                    "title": "Data",
                },
            ]
        }
    ]
    assert schema["paths"]["/discriminated"]["post"]["requestBody"] == {
        "content": {
            "application/x-www-form-urlencoded": {
                "schema": {
                    "$ref": "#/components/schemas/Body_read_discriminated_discriminated_post"
                }
            }
        }
    }
    assert schemas["Body_read_discriminated_discriminated_post"]["allOf"] == [
        {
            "anyOf": [
                absent,
                {
                    "anyOf": [
                        {
                            "oneOf": [
                                {"$ref": "#/components/schemas/TextForm"},
                                {"$ref": "#/components/schemas/ListForm"},
                            ],
                            "discriminator": {
                                "propertyName": "kind",
                                "mapping": {
                                    "text": "#/components/schemas/TextForm",
                                    "list": "#/components/schemas/ListForm",
                                },
                            },
                        },
                    ],
                    "title": "Data",
                },
            ]
        }
    ]
    assert schemas["TextForm"] == TextForm.model_json_schema()
    assert schemas["ListForm"] == ListForm.model_json_schema()
