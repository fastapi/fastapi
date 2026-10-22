from typing import Annotated, Literal

import pytest
from fastapi import Body, Depends, FastAPI, File, Form, UploadFile
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    computed_field,
)


class Person(BaseModel):
    kind: Literal["person"] = Field(alias="contact_type")
    name: str
    tags: list[str] = Field(default_factory=list)
    enabled: bool = True


class Company(BaseModel):
    kind: Literal["company"] = Field(alias="contact_type")
    company_name: str


class Email(BaseModel):
    delivery: Literal["email"]
    address: str


class Pickup(BaseModel):
    delivery: Literal["pickup"]
    location: str


class Settings(BaseModel):
    priority: int = Field(default=1, ge=1)


app = FastAPI()


@app.post("/combined")
def combined(
    contact: Annotated[Person | Company, Form(discriminator="kind")],
    delivery: Annotated[Email | Pickup, Form(discriminator="delivery")],
    settings: Annotated[Settings, Form()],
    token: Annotated[str, Form()],
):
    return {
        "contact": contact,
        "delivery": delivery,
        "settings": settings,
        "token": token,
    }


@app.post("/optional")
def optional(
    token: Annotated[str, Form()],
    contact: Annotated[Person | Company | None, Form(discriminator="kind")] = None,
    delivery: Annotated[Email | Pickup | None, Form(discriminator="delivery")] = None,
):
    return {"contact": contact, "delivery": delivery}


@app.post("/ordinary")
def ordinary(
    contact: Annotated[Person | Company, Form()], token: Annotated[str, Form()]
):
    return contact


@app.post("/files")
async def files(
    contact: Annotated[Person | Company, Form(discriminator="kind")],
    avatar: Annotated[UploadFile, File()],
    content: Annotated[bytes, File(alias="avatar")],
    attachments: Annotated[list[bytes] | None, File()] = None,
):
    return {
        "contact": contact,
        "position": avatar.file.tell(),
        "avatar": await avatar.read(),
        "content": content,
        "attachments": attachments,
    }


@app.post("/json")
def json_body(contact: Person | Company, token: Annotated[str, Body()]):
    return contact


client = TestClient(app)


@pytest.mark.parametrize(
    "contact,expected_contact",
    [
        (
            {"contact_type": "person", "name": "Rick", "tags": ["", "blue"]},
            {
                "contact_type": "person",
                "name": "Rick",
                "tags": ["", "blue"],
                "enabled": False,
            },
        ),
        (
            {"contact_type": "company", "company_name": "Acme"},
            {"contact_type": "company", "company_name": "Acme"},
        ),
    ],
)
@pytest.mark.parametrize(
    "delivery",
    [
        {"delivery": "email", "address": "rick@example.com"},
        {"delivery": "pickup", "location": "Office"},
    ],
)
def test_multiple_unions_with_model_and_scalar(contact, expected_contact, delivery):
    response = client.post(
        "/combined", data={**contact, **delivery, "token": "secret", "priority": "2"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "contact": expected_contact,
        "delivery": delivery,
        "settings": {"priority": 2},
        "token": "secret",
    }


@pytest.mark.parametrize(
    "fields,expected",
    [
        ({"token": "secret"}, {"contact": None, "delivery": None}),
        (
            {"token": "secret", "contact_type": "company", "company_name": "Acme"},
            {
                "contact": {"contact_type": "company", "company_name": "Acme"},
                "delivery": None,
            },
        ),
        (
            {"token": "secret", "delivery": "pickup", "location": "Office"},
            {"contact": None, "delivery": {"delivery": "pickup", "location": "Office"}},
        ),
    ],
)
def test_optional_unions_are_independent(fields, expected):
    response = client.post("/optional", data=fields)
    assert response.status_code == 200, response.text
    assert response.json() == expected


def test_partial_and_empty_optional_union():
    response = client.post("/optional", data={"token": "secret", "name": ""})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("union_tag_not_found", ["body"])
    ]
    response = client.post(
        "/optional", data={"token": "secret", "contact_type": "person"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "person", "name"]


def test_forbid_union_branch_rejects_siblings_and_unselected_fields():
    app = FastAPI()

    class ClosedPerson(Person):
        model_config = ConfigDict(extra="forbid")

    @app.post("/")
    def submit(
        contact: Annotated[ClosedPerson | Company, Form(discriminator="kind")],
        token: Annotated[str | None, Form()] = None,
    ):
        return contact

    client = TestClient(app)
    fields = {"contact_type": "person", "name": "Rick"}
    assert client.post("/", data=fields).status_code == 200
    for extra in ({"token": "secret"}, {"company_name": "Acme"}):
        response = client.post("/", data={**fields, **extra})
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "extra_forbidden"
        assert response.json()["detail"][0]["loc"] == [
            "body",
            "person",
            next(iter(extra)),
        ]
    response = client.post(
        "/", data={"contact_type": "company", "company_name": "Acme", "token": "secret"}
    )
    assert response.status_code == 200, response.text
    schema = app.openapi()["components"]["schemas"]
    union = schema["Body_submit__post"]["allOf"][0]
    assert (
        union["discriminator"]["mapping"]["person"]
        == "#/components/schemas/ClosedPerson"
    )
    assert schema["ClosedPerson"]["additionalProperties"] is False
    assert "token" not in schema["ClosedPerson"]["properties"]


def test_optional_forbid_union_is_activated_by_sibling_fields():
    app = FastAPI()

    class ClosedPerson(Person):
        model_config = ConfigDict(extra="forbid")

    @app.post("/")
    def submit(
        token: Annotated[str | None, Form()] = None,
        contact: Annotated[
            ClosedPerson | Company | None, Form(discriminator="kind")
        ] = None,
    ):
        return contact

    client = TestClient(app)
    assert client.post("/").json() is None
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "union_tag_not_found"
    schema = app.openapi()["components"]["schemas"]["Body_submit__post"]
    assert schema["allOf"][0]["anyOf"][0] == {"maxProperties": 0}


def test_ordinary_union():
    response = client.post(
        "/ordinary",
        data={"token": "secret", "contact_type": "company", "company_name": "Acme"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"contact_type": "company", "company_name": "Acme"}


@pytest.mark.parametrize(
    "mode,expected", [("smart", "Detailed"), ("left_to_right", "Simple")]
)
def test_pydantic_selects_branch_with_sibling_fields(mode, expected):
    app = FastAPI()

    class Simple(BaseModel):
        name: str

    class Detailed(Simple):
        count: int

    @app.post("/")
    def submit(
        data: Annotated[Simple | Detailed, Form(union_mode=mode)],
        count: Annotated[int, Form()],
    ):
        return {"model": type(data).__name__, "count": count}

    response = TestClient(app).post("/", data={"name": "Rick", "count": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"model": expected, "count": 2}


def test_repeated_values_are_extracted_independently():
    app = FastAPI()

    class Text(BaseModel):
        value: str

    class Items(BaseModel):
        value: list[str]

    @app.post("/")
    def submit(
        text: Annotated[Text | Company, Form()],
        items: Annotated[Items | Company, Form()],
        value: Annotated[str, Form()],
    ):
        return {"text": text, "items": items, "value": value}

    response = TestClient(app).post("/", data={"value": ["", "blue"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "text": {"value": "blue"},
        "items": {"value": ["", "blue"]},
        "value": "blue",
    }


def test_union_with_files():
    response = client.post(
        "/files",
        data={"contact_type": "person", "name": "Rick", "tags": ["", "blue"]},
        files=[
            ("avatar", ("avatar.txt", b"hello")),
            ("attachments", ("empty.txt", b"")),
            ("attachments", ("other.txt", b"other")),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "contact": {
            "contact_type": "person",
            "name": "Rick",
            "tags": ["", "blue"],
            "enabled": False,
        },
        "position": 0,
        "avatar": "hello",
        "content": "hello",
        "attachments": ["", "other"],
    }
    response = client.post(
        "/files",
        data={"contact_type": "company", "company_name": "Acme"},
        files={"avatar": ("empty.txt", b"")},
    )
    assert response.status_code == 200, response.text
    assert response.json()["attachments"] is None


def test_union_upload_is_shared_with_file_parameter():
    app = FastAPI()

    class Uploaded(BaseModel):
        upload: UploadFile

    @app.post("/")
    async def submit(
        data: Annotated[Uploaded | Company, Form()],
        content: Annotated[bytes, File(alias="upload")],
    ):
        assert isinstance(data, Uploaded)
        return {
            "position": data.upload.file.tell(),
            "upload": await data.upload.read(),
            "content": content,
        }

    response = TestClient(app).post("/", files={"upload": ("hello.txt", b"hello")})
    assert response.status_code == 200, response.text
    assert response.json() == {"position": 0, "upload": "hello", "content": "hello"}


def test_optional_union_with_file_only():
    app = FastAPI()

    @app.post("/")
    def submit(
        attachment: Annotated[bytes, File()],
        contact: Annotated[Person | Company | None, Form(discriminator="kind")] = None,
    ):
        return contact

    response = TestClient(app).post("/", files={"attachment": ("file.txt", b"hello")})
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_multiple_unions_multipart():
    response = client.post(
        "/optional",
        files={
            "token": (None, "secret"),
            "contact_type": (None, "company"),
            "company_name": (None, "Acme"),
            "delivery": (None, "pickup"),
            "location": (None, "Office"),
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "contact": {"contact_type": "company", "company_name": "Acme"},
        "delivery": {"delivery": "pickup", "location": "Office"},
    }


def test_union_with_optional_model_and_defaults():
    app = FastAPI()
    default = Company(contact_type="company", company_name="Default")

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        contact: Annotated[
            Person | Company | None, Form(discriminator="kind")
        ] = default,
        settings: Annotated[Settings | None, Form()] = None,
    ):
        return {"contact": contact, "settings": settings}

    client = TestClient(app)
    response = client.post("/", data={"token": "secret", "priority": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "contact": {"contact_type": "company", "company_name": "Default"},
        "settings": {"priority": 2},
    }
    response = client.post(
        "/", data={"token": "secret", "contact_type": "company", "company_name": "Acme"}
    )
    assert response.status_code == 200, response.text
    assert response.json()["settings"] is None
    schema = app.openapi()["components"]["schemas"]["Body_submit__post"]
    assert len(schema["allOf"]) == 2
    assert schema["required"] == ["token"]


def test_required_nullable_union_with_defaulted_fields():
    app = FastAPI()

    class Count(BaseModel):
        count: int = 1

    class Label(BaseModel):
        label: str = "default"

    @app.post("/")
    def submit(
        data: Annotated[Count | Label | None, Form()], token: Annotated[str, Form()]
    ):
        return data

    client = TestClient(app)
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
    ]
    response = client.post("/", data={"token": "secret", "count": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"count": 2}
    schema = app.openapi()["components"]["schemas"]["Body_submit__post"]
    assert schema["allOf"][0] == {
        "not": {"not": {"anyOf": [{"required": ["count"]}, {"required": ["label"]}]}}
    }


def test_dependencies_with_same_parameter_name_and_overrides():
    app = FastAPI()

    def get_delivery(data: Annotated[Email | Pickup, Form(discriminator="delivery")]):
        return data

    def nested(delivery: Annotated[Email | Pickup, Depends(get_delivery)]):
        return delivery

    def replacement(page: Annotated[int, Form()]):
        return page

    @app.post("/")
    def submit(
        data: Annotated[Person | Company, Form(discriminator="kind")],
        delivery: Annotated[Email | Pickup, Depends(nested)],
    ):
        return {"contact": data, "delivery": delivery}

    client = TestClient(app)
    contact = {"contact_type": "company", "company_name": "Acme"}
    response = client.post(
        "/", data={**contact, "delivery": "pickup", "location": "Office"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "contact": contact,
        "delivery": {"delivery": "pickup", "location": "Office"},
    }
    app.dependency_overrides[get_delivery] = replacement
    response = client.post("/", data={**contact, "page": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"contact": contact, "delivery": 2}
    response = client.post("/", data={**contact, "page": "2", "location": "Office"})
    assert response.status_code == 200, response.text
    assert response.json() == {"contact": contact, "delivery": 2}
    schema = app.openapi()
    body = schema["components"]["schemas"]["Body_submit__post"]
    assert len(body["allOf"]) == 2


@pytest.mark.parametrize("alias", ["full_name", "nickname"])
def test_alias_choices_activate_only_their_union(alias):
    app = FastAPI()

    class Named(BaseModel):
        name: str = Field(validation_alias=AliasChoices("full_name", "nickname"))

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        contact: Annotated[Named | Company | None, Form()] = None,
    ):
        return contact

    response = TestClient(app).post("/", data={"token": "secret", alias: "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick"}
    schema = app.openapi()
    branch = schema["components"]["schemas"]["Named"]
    assert branch["required"] == ["full_name"]


@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
    reason="validate_by_alias requires Pydantic 2.11",
)
def test_aliases_disabled_in_model_schema():
    app = FastAPI()

    class Named(BaseModel):
        model_config = ConfigDict(validate_by_alias=False)
        name: str = Field(validation_alias=AliasChoices("full_name", "nickname"))

    @app.post("/")
    def submit(
        contact: Annotated[Named | Company, Form()], token: Annotated[str, Form()]
    ):
        return contact

    response = TestClient(app).post("/", data={"token": "secret", "name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick"}
    schemas = app.openapi()["components"]["schemas"]
    assert schemas["Named"] == Named.model_json_schema()


@pytest.mark.parametrize("default", [..., "default"])
def test_unused_aliases_are_forbidden(default):
    app = FastAPI()

    class Named(BaseModel):
        model_config = ConfigDict(extra="forbid")
        token: str
        name: str = Field(
            default=default, validation_alias=AliasChoices("name", "nickname")
        )

    @app.post("/")
    def submit(
        contact: Annotated[Named | Company, Form()], token: Annotated[str, Form()]
    ):
        return contact

    client = TestClient(app)
    response = client.post("/", data={"token": "secret", "nickname": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick", "token": "secret"}
    response = client.post(
        "/", data={"token": "secret", "name": "Rick", "nickname": "Morty"}
    )
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "Named", "nickname"]
    assert error["type"] == "extra_forbidden"
    schema = app.openapi()["components"]["schemas"]["Named"]
    assert schema["additionalProperties"] is False


def test_distinct_input_and_output_schemas():
    app = FastAPI()

    class Named(BaseModel):
        name: str

        @computed_field
        @property
        def uppercase(self) -> str:
            return self.name.upper()

    @app.post("/", response_model=Named | Company)
    def submit(
        contact: Annotated[Named | Company, Form()], token: Annotated[str, Form()]
    ):
        return contact

    response = TestClient(app).post("/", data={"token": "secret", "name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick", "uppercase": "RICK"}
    document = app.openapi()
    schemas = document["components"]["schemas"]
    body = schemas["Body_submit__post"]
    branch_ref = body["allOf"][0]["anyOf"][0]["$ref"]
    assert set(schemas[branch_ref.rsplit("/", 1)[1]]["properties"]) == {"name"}
    output = document["paths"]["/"]["post"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    output_ref = output["anyOf"][0]["$ref"]
    assert set(schemas[output_ref.rsplit("/", 1)[1]]["properties"]) == {
        "name",
        "uppercase",
    }


def test_shared_fields_and_union_before_validator():
    app = FastAPI()
    calls = []

    class Lower(BaseModel):
        left: Literal["lower"]
        count: int = Field(ge=1)

    class Upper(BaseModel):
        right: Literal["upper"]
        count: int = Field(le=10)

    def copy_input(data):
        calls.append(data.copy())
        return data.copy()

    @app.post("/")
    def submit(
        left: Annotated[Lower | Company, BeforeValidator(copy_input), Form()],
        right: Annotated[Upper | Email, Form()],
    ):
        return [left, right]

    client = TestClient(app)
    response = client.post("/", data={"left": "lower", "right": "upper", "count": "5"})
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"left": "lower", "count": 5},
        {"right": "upper", "count": 5},
    ]
    assert calls == [{"left": "lower", "right": "upper", "count": "5"}]
    for count, branch in [("0", "Lower"), ("11", "Upper")]:
        response = client.post(
            "/", data={"left": "lower", "right": "upper", "count": count}
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", branch, "count"]


@pytest.mark.parametrize(
    "extra,expected,expected_repeated",
    [
        ("ignore", None, None),
        (
            "allow",
            {"count": 1, "token": "secret"},
            {"count": 1, "token": "secret", "unknown": ["a", "b"]},
        ),
    ],
)
def test_unknown_fields_ignore_or_allow(extra, expected, expected_repeated):
    app = FastAPI()

    class Count(BaseModel):
        model_config = ConfigDict(extra=extra)
        count: int = 1

    class Label(BaseModel):
        model_config = ConfigDict(extra=extra)
        label: str = "default"

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        data: Annotated[Count | Label | None, Form(union_mode="left_to_right")] = None,
    ):
        return data

    client = TestClient(app)
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() == expected
    response = client.post("/", data={"token": "secret", "unknown": ["a", "b"]})
    assert response.status_code == 200, response.text
    assert response.json() == expected_repeated


def test_optional_union_with_mixed_extra_configurations():
    app = FastAPI()

    class Named(BaseModel):
        name: str

    class Count(BaseModel):
        model_config = ConfigDict(extra="allow")
        count: int = 1

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        data: Annotated[Named | Count | None, Form()] = None,
    ):
        return data

    response = TestClient(app).post("/", data={"token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() == {"count": 1, "token": "secret"}
    schema = app.openapi()["components"]["schemas"]["Body_submit__post"]
    assert schema["allOf"][0]["anyOf"][0] == {"maxProperties": 0}


def test_json_and_original_model_schemas_are_unchanged():
    response = client.post(
        "/json",
        json={"contact": {"contact_type": "person", "name": "Rick"}, "token": "secret"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["enabled"] is True
    schemas = app.openapi()["components"]["schemas"]
    assert set(schemas["Person"]["properties"]) == {
        "contact_type",
        "name",
        "tags",
        "enabled",
    }
    assert "additionalProperties" not in schemas["Person"]
    assert "token" not in Person.model_fields


def test_openapi_multiple_unions():
    document = app.openapi()
    body = document["paths"]["/combined"]["post"]["requestBody"]
    assert body["required"] is True
    schemas = document["components"]["schemas"]
    schema = schemas["Body_combined_combined_post"]
    assert schema["required"] == ["token"]
    assert set(schema["properties"]) == {"token"}
    assert len(schema["allOf"]) == 3
    contact, delivery, settings = schema["allOf"]
    assert contact["discriminator"]["mapping"] == {
        "person": "#/components/schemas/Person",
        "company": "#/components/schemas/Company",
    }
    assert len(contact["oneOf"]) == len(delivery["oneOf"]) == 2
    assert settings["$ref"] == "#/components/schemas/Settings"
    person = schemas[contact["oneOf"][0]["$ref"].rsplit("/", 1)[1]]
    assert person["required"] == ["contact_type", "name"]
    assert "token" not in person["properties"]
    assert "location" not in person["properties"]
    assert "company_name" not in person["properties"]
    multipart = document["paths"]["/files"]["post"]["requestBody"]
    assert set(multipart["content"]) == {"multipart/form-data"}
    assert schemas["Body_files_files_post"]["required"] == ["avatar"]


def test_openapi_optional_unions():
    schema = app.openapi()["components"]["schemas"]["Body_optional_optional_post"]
    assert schema["required"] == ["token"]
    assert len(schema["allOf"]) == 2
    contact, delivery = schema["allOf"]
    absent, present = contact["anyOf"]
    assert {item["required"][0] for item in absent["not"]["anyOf"]} == {
        "contact_type",
        "name",
        "tags",
        "enabled",
        "company_name",
    }
    assert "null" not in str(present)
    assert len(present["anyOf"][0]["oneOf"]) == 2
    assert {item["required"][0] for item in delivery["anyOf"][0]["not"]["anyOf"]} == {
        "delivery",
        "address",
        "location",
    }
