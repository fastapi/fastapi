from collections.abc import Mapping
from typing import Annotated, Any, Literal

import pytest
from dirty_equals import IsOneOf
from fastapi import Depends, FastAPI, Form, UploadFile
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Discriminator,
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
def read_union(data: Annotated[TextForm | ListForm, Form()]):
    return data.model_dump(exclude_unset=True)


@app.post("/discriminated")
def read_discriminated(
    data: Annotated[TextForm | ListForm, Form(discriminator="kind")],
):
    return data.model_dump(exclude_unset=True)


@app.post("/json")
def read_json(data: TextForm | ListForm):
    return data


client = TestClient(app)


@pytest.mark.parametrize(
    "path,branch", [("/union", "TextForm"), ("/discriminated", "text")]
)
def test_empty_scalar_is_missing(path, branch):
    response = client.post(path, data={"kind": "text", "value": ""})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", branch, "value"]


@pytest.mark.parametrize(
    "path,branch", [("/union", "TextForm"), ("/discriminated", "text")]
)
def test_empty_multipart_scalar_is_missing(path, branch):
    response = client.post(path, files={"kind": (None, "text"), "value": (None, "")})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", branch, "value"]


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
@pytest.mark.parametrize("values", [[""], ["", "blue"], ["red"]])
def test_list_items_are_preserved(path, values):
    response = client.post(path, data={"kind": "list", "value": values})
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "value": values}


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
def test_multipart_list_items_are_preserved(path):
    response = client.post(
        path,
        files=[
            ("kind", (None, "list")),
            ("value", (None, "")),
            ("value", (None, "blue")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "value": ["", "blue"]}


def test_omitted_list_is_missing():
    response = client.post("/discriminated", data={"kind": "list"})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "list", "value"]


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
def test_omitted_boolean_is_explicit_false(path):
    response = client.post(path, data={"kind": "text", "value": "hello"})
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "value": "hello", "enabled": False}


@pytest.mark.parametrize("path", ["/union", "/discriminated"])
def test_checked_boolean_is_true(path):
    response = client.post(
        path, data={"kind": "text", "value": "hello", "enabled": "on"}
    )
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "value": "hello", "enabled": True}


def test_json_and_direct_model_validation_are_unchanged():
    response = client.post("/json", json={"kind": "text", "value": ""})
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "value": "", "enabled": True}
    model = TextForm.model_validate({"kind": "text", "value": ""})
    assert model.value == ""
    assert model.enabled is True
    assert model.model_fields_set == {"kind", "value"}


@pytest.mark.parametrize(
    "data,error_type",
    [
        ({"value": "hello"}, "union_tag_not_found"),
        ({"kind": "unknown", "value": "hello"}, "union_tag_invalid"),
    ],
)
def test_discriminator_errors_are_preserved(data, error_type):
    response = client.post("/discriminated", data=data)
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == error_type
    assert error["loc"] == ["body"]


@pytest.mark.parametrize("form", [Form(), Form(discriminator="kind")])
def test_missing_fields_use_model_defaults(form):
    app = FastAPI()

    class DefaultsForm(BaseModel):
        kind: Literal["defaults"]
        value: str = "default"
        items: Annotated[list[str], Field(default_factory=lambda: ["default"])]
        enabled: bool
        nullable: bool | None = None

    @app.post("/")
    def read_form(data: Annotated[DefaultsForm | ListForm, form]):
        return {
            "values": data.model_dump(),
            "set": data.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    response = client.post("/", data={"kind": "defaults", "value": ""})
    assert response.status_code == 200
    assert response.json() == {
        "values": {
            "kind": "defaults",
            "value": "default",
            "items": ["default"],
            "enabled": False,
            "nullable": False,
        },
        "set": {"kind": "defaults", "enabled": False, "nullable": False},
    }


@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 10),
    reason="Default factories with validated data require Pydantic 2.10",
)
def test_default_factory_receives_validated_data():
    app = FastAPI()

    class DefaultsForm(BaseModel):
        kind: Literal["defaults"]
        value: str = "default"
        derived: Annotated[str, Field(default_factory=lambda data: data["value"])]

    @app.post("/")
    def read_form(data: Annotated[DefaultsForm | ListForm, Form()]):
        return data

    client = TestClient(app)
    response = client.post("/", data={"kind": "defaults", "value": ""})
    assert response.status_code == 200
    assert response.json() == {
        "kind": "defaults",
        "value": "default",
        "derived": "default",
    }


def test_validate_default_is_preserved():
    app = FastAPI()

    class DefaultsForm(BaseModel):
        kind: Literal["defaults"]
        value: Annotated[int, Field(default="invalid", validate_default=True)]

    @app.post("/")
    def read_form(
        data: Annotated[DefaultsForm | ListForm, Form(discriminator="kind")],
    ):
        return data

    client = TestClient(app)
    response = client.post("/", data={"kind": "defaults", "value": ""})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "int_parsing"
    assert error["loc"] == ["body", "defaults", "value"]
    response = client.post("/", data={"kind": "defaults", "value": "42"})
    assert response.status_code == 200
    assert response.json() == {"kind": "defaults", "value": 42}


@pytest.mark.parametrize("form", [Form(), Form(discriminator="kind")])
def test_alias_choices_and_forbidden_extras(form):
    app = FastAPI()

    class AliasedForm(BaseModel):
        model_config = ConfigDict(extra="forbid")
        kind: Literal["aliased"]
        value: Annotated[
            str, Field(validation_alias=AliasChoices("primary", "secondary"))
        ]
        enabled: Annotated[bool, Field(alias="accept-terms")] = True

    @app.post("/")
    def read_form(data: Annotated[AliasedForm | ListForm, form]):
        return data.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(
        "/", data={"kind": "aliased", "primary": "", "secondary": "hello"}
    )
    assert response.status_code == 200
    assert response.json() == {"kind": "aliased", "value": "hello", "enabled": False}
    response = client.post(
        "/", data={"kind": "aliased", "primary": "hello", "secondary": ""}
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        error["type"] == "extra_forbidden" and error["loc"][-1] == "secondary"
        for error in errors
    )


def test_aliased_discriminator():
    app = FastAPI()

    class AliasedTextForm(BaseModel):
        kind: Annotated[Literal["text"], Field(alias="form-kind")]
        value: str = "default"

    class AliasedListForm(BaseModel):
        kind: Annotated[Literal["list"], Field(alias="form-kind")]
        value: list[str]

    @app.post("/")
    def read_form(
        data: Annotated[AliasedTextForm | AliasedListForm, Form(discriminator="kind")],
    ):
        return data.model_dump()

    client = TestClient(app)
    response = client.post("/", data={"form-kind": "text", "value": ""})
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "value": "default"}
    response = client.post("/", data={"form-kind": "list", "value": ""})
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "value": [""]}


@pytest.mark.parametrize("path", ["/", "/composed"])
def test_callable_discriminator_preserves_tags(path):
    app = FastAPI()

    def get_kind(value: Any):
        assert isinstance(value, Mapping)
        return value.get("kind")

    def require_token(token: Annotated[str, Form()]):
        return token

    @app.post("/")
    @app.post("/composed", dependencies=[Depends(require_token)])
    def read_form(
        data: Annotated[
            Annotated[TextForm, Tag("text")] | Annotated[ListForm, Tag("list")],
            Discriminator(get_kind),
            Form(),
        ],
    ):
        return data.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data={"kind": "list", "value": "", "token": "secret"})
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "value": [""]}
    response = client.post(path, data={"kind": "text", "value": "", "token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "text", "value"]


@pytest.mark.parametrize(
    "mode,expected_model", [("smart", "DetailedForm"), ("left_to_right", "SimpleForm")]
)
@pytest.mark.parametrize("path", ["/field", "/form"])
def test_pydantic_selects_union_branch(mode, expected_model, path):
    app = FastAPI()

    class SimpleForm(BaseModel):
        value: str

    class DetailedForm(BaseModel):
        value: str
        count: int

    @app.post("/field")
    def read_field(
        data: Annotated[SimpleForm | DetailedForm, Field(union_mode=mode), Form()],
    ):
        return type(data).__name__

    @app.post("/form")
    def read_form(
        data: Annotated[SimpleForm | DetailedForm, Form(union_mode=mode)],
    ):
        return type(data).__name__

    client = TestClient(app)
    response = client.post(path, data={"value": "hello", "count": "2"})
    assert response.status_code == 200
    assert response.json() == expected_model


def test_model_validator_does_not_mutate_other_branches():
    app = FastAPI()

    class FirstForm(BaseModel):
        value: str

        @model_validator(mode="before")
        @classmethod
        def remove_value(cls, data):
            data.pop("value", None)
            return data

    class SecondForm(BaseModel):
        value: list[str]

    @app.post("/")
    def read_form(data: Annotated[FirstForm | SecondForm, Form()]):
        return data

    client = TestClient(app)
    response = client.post("/", data={"value": ["", "hello"]})
    assert response.status_code == 200
    assert response.json() == {"value": ["", "hello"]}


def test_union_with_another_form_parameter_requires_model_fields():
    app = FastAPI()

    @app.post("/")
    def read_form(
        data: Annotated[TextForm | ListForm, Form()],
        token: Annotated[str, Form()],
    ):
        pytest.fail("Invalid form data reached the endpoint")  # pragma: no cover

    client = TestClient(app)
    response = client.post("/", data={"data": "hello", "token": "example"})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["body", "TextForm", "kind"],
        ["body", "TextForm", "value"],
        ["body", "ListForm", "kind"],
        ["body", "ListForm", "value"],
    ]
    assert all(error["type"] == "missing" for error in response.json()["detail"])


def test_file_placeholders_and_selected_files():
    app = FastAPI()

    class FileForm(BaseModel):
        kind: Literal["file"]
        file: UploadFile | None = None
        files: Annotated[list[UploadFile], Field(default_factory=list)]

    @app.post("/")
    def read_form(
        data: Annotated[FileForm | TextForm, Form(discriminator="kind")],
    ):
        assert isinstance(data, FileForm)
        return {
            "file": data.file.size if data.file is not None else None,
            "files": [file.size for file in data.files],
            "set": sorted(data.model_fields_set),
        }

    client = TestClient(app)
    # HTTPX drops empty filenames, so send the browser representation directly.
    response = client.post(
        "/",
        content=(
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="kind"\r\n\r\n'
            b"file\r\n"
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="file"; filename=""\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"\r\n--boundary\r\n"
            b'Content-Disposition: form-data; name="files"; filename=""\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"\r\n--boundary--\r\n"
        ),
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == {"file": None, "files": [], "set": ["kind"]}

    response = client.post(
        "/",
        data={"kind": "file"},
        files={
            "file": ("empty.txt", b""),
            "files": ("hello.txt", b"hello"),
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "file": 0,
        "files": [5],
        "set": ["file", "files", "kind"],
    }


@pytest.mark.parametrize("path", ["/model", "/union"])
def test_before_validator_can_rename_form_fields(path):
    app = FastAPI()

    def rename_value(data):
        assert isinstance(data, dict)
        data["value"] = data.pop("legacy")
        return data

    @app.post("/model")
    def read_model(data: Annotated[TextForm, BeforeValidator(rename_value), Form()]):
        return data.model_dump(exclude_unset=True)

    @app.post("/union")
    def read_union(
        data: Annotated[TextForm | ListForm, BeforeValidator(rename_value), Form()],
    ):
        return data.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data={"kind": "text", "legacy": "hello"})
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "value": "hello", "enabled": False}


@pytest.mark.parametrize("form", [Form(), Form(discriminator="kind")])
def test_union_before_validator_can_copy_form_data(form):
    app = FastAPI()

    def copy_input(data):
        assert isinstance(data, dict)
        return data.copy()

    @app.post("/")
    def read_form(
        data: Annotated[TextForm | ListForm, BeforeValidator(copy_input), form],
    ):
        return data.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post("/", data={"kind": "list", "value": ["", "blue"]})
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "value": ["", "blue"]}

    response = client.post("/", data={"kind": "list", "value": ""})
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "value": [""]}

    response = client.post("/", data={"kind": "text", "value": "hello"})
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "value": "hello", "enabled": False}

    response = client.post("/", data={"kind": "text", "value": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"][-1] == "value"


def test_union_before_validator_can_supply_null_and_empty_list():
    app = FastAPI()

    class NullableForm(BaseModel):
        kind: Literal["nullable"]
        value: str | None = "default"
        items: list[str]
        enabled: bool | None = True

    def clear_fields(data):
        data["value"] = None
        data["items"] = []
        data["enabled"] = None
        return data

    @app.post("/")
    def read_form(
        data: Annotated[
            NullableForm | TextForm,
            BeforeValidator(clear_fields),
            Form(discriminator="kind"),
        ],
    ):
        return data.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post("/", data={"kind": "nullable"})
    assert response.status_code == 200
    assert response.json() == {
        "kind": "nullable",
        "value": None,
        "items": [],
        "enabled": None,
    }


def test_union_field_can_have_the_same_name_as_the_parameter():
    app = FastAPI()

    class TextData(BaseModel):
        kind: Literal["text"]
        data: str

    class ListData(BaseModel):
        kind: Literal["list"]
        data: list[str]

    @app.post("/")
    def read_form(data: Annotated[TextData | ListData, Form()]):
        return data

    client = TestClient(app)
    response = client.post("/", data={"kind": "list", "data": ["red", "blue"]})
    assert response.status_code == 200
    assert response.json() == {"kind": "list", "data": ["red", "blue"]}

    response = client.post("/", data={"kind": "text", "data": ["red", "blue"]})
    assert response.status_code == 200
    assert response.json() == {"kind": "text", "data": "blue"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/union": {
                    "post": {
                        "summary": "Read Union",
                        "operationId": "read_union_union_post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/TextForm"},
                                            {"$ref": "#/components/schemas/ListForm"},
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/discriminated": {
                    "post": {
                        "summary": "Read Discriminated",
                        "operationId": "read_discriminated_discriminated_post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/TextForm"},
                                            {"$ref": "#/components/schemas/ListForm"},
                                        ],
                                        "title": "Data",
                                        "discriminator": {
                                            "propertyName": "kind",
                                            "mapping": {
                                                "text": "#/components/schemas/TextForm",
                                                "list": "#/components/schemas/ListForm",
                                            },
                                        },
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/json": {
                    "post": {
                        "summary": "Read Json",
                        "operationId": "read_json_json_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/TextForm"},
                                            {"$ref": "#/components/schemas/ListForm"},
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "ListForm": {
                        "properties": {
                            "kind": IsOneOf(
                                {"type": "string", "const": "list", "title": "Kind"},
                                # Pydantic 2.9 also includes enum for a single Literal.
                                {
                                    "type": "string",
                                    "const": "list",
                                    "enum": ["list"],
                                    "title": "Kind",
                                },
                            ),
                            "value": {
                                "items": {"type": "string"},
                                "type": "array",
                                "title": "Value",
                            },
                        },
                        "type": "object",
                        "required": ["kind", "value"],
                        "title": "ListForm",
                    },
                    "TextForm": {
                        "properties": {
                            "kind": IsOneOf(
                                {"type": "string", "const": "text", "title": "Kind"},
                                # Pydantic 2.9 also includes enum for a single Literal.
                                {
                                    "type": "string",
                                    "const": "text",
                                    "enum": ["text"],
                                    "title": "Kind",
                                },
                            ),
                            "value": {"type": "string", "title": "Value"},
                            "enabled": {
                                "type": "boolean",
                                "title": "Enabled",
                                "default": True,
                            },
                        },
                        "type": "object",
                        "required": ["kind", "value"],
                        "title": "TextForm",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                            "input": {"title": "Input"},
                            "ctx": {"type": "object", "title": "Context"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
