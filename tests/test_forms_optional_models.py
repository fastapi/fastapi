from typing import Annotated, Optional

import pytest
from fastapi import Depends, FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


def form_schema(app, path="/"):
    schema = app.openapi()
    body = schema["paths"][path]["post"]["requestBody"]
    content = next(iter(body["content"].values()))
    ref = content["schema"]["$ref"]
    return body, schema["components"]["schemas"][ref.rsplit("/", 1)[-1]]


def test_optional_form_model():
    app = FastAPI()

    class Profile(BaseModel):
        name: str
        age: int
        tags: list[str] = Field(default_factory=list)
        enabled: bool = True

    @app.post("/")
    def submit(profile: Annotated[Profile | None, Form()] = None):
        return profile

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"name": "Rick", "age": "70", "tags": ["a", "b"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Rick",
        "age": 70,
        "tags": ["a", "b"],
        "enabled": False,
    }
    response = client.post("/", data={"name": "Rick", "age": "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "age"]
    for fields in ({"name": ""}, {"tags": "a"}, {"enabled": "false"}):
        response = client.post("/", data=fields)
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["body", "name"],
            ["body", "age"],
        ]


def test_optional_form_model_with_other_form_field():
    app = FastAPI()

    class Profile(BaseModel):
        name: str
        age: int

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        profile: Annotated[Profile | None, Form()] = None,
    ):
        return profile

    client = TestClient(app)
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"token": "secret", "name": "Rick", "age": "70"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick", "age": 70}
    response = client.post("/", data={"token": "secret", "name": "Rick"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "age"]


def test_optional_form_model_in_dependency():
    app = FastAPI()

    class Profile(BaseModel):
        name: str
        age: int

    def profile_dependency(profile: Annotated[Profile | None, Form()] = None):
        return profile

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        profile: Annotated[Profile | None, Depends(profile_dependency)],
    ):
        return profile

    client = TestClient(app)
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"token": "secret", "name": "Rick", "age": "70"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick", "age": 70}
    response = client.post("/", data={"token": "secret", "name": "Rick"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "age"]


def test_optional_form_model_multipart():
    app = FastAPI()

    class Profile(BaseModel):
        name: str
        age: int
        tags: list[str] = Field(default_factory=list)
        enabled: bool = True

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        profile: Annotated[Profile | None, Form()] = None,
    ):
        return profile

    client = TestClient(app)
    response = client.post("/", files={"token": (None, "secret")})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post(
        "/",
        files=[
            ("token", (None, "secret")),
            ("name", (None, "Rick")),
            ("age", (None, "70")),
            ("tags", (None, "a")),
            ("tags", (None, "b")),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Rick",
        "age": 70,
        "tags": ["a", "b"],
        "enabled": False,
    }
    response = client.post(
        "/",
        files={
            "token": (None, "secret"),
            "name": (None, "Rick"),
            "age": (None, "invalid"),
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "age"]
    for fields in (
        {"token": (None, "secret"), "name": (None, "")},
        {"token": (None, "secret"), "tags": (None, "a")},
        {"token": (None, "secret"), "enabled": (None, "false")},
    ):
        response = client.post("/", files=fields)
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["body", "name"],
            ["body", "age"],
        ]


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
def test_optional_form_model_schema(extra):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra=extra)
        name: str
        age: int
        tags: list[str] = Field(default_factory=list)
        enabled: bool = True

    @app.post("/")
    def submit(profile: Annotated[Profile | None, Form()] = None):
        return profile

    body, schema = form_schema(app)
    assert "required" not in body
    assert "required" not in schema
    absent = {
        "not": {
            "anyOf": [
                {"required": ["name"]},
                {"required": ["age"]},
                {"required": ["tags"]},
                {"required": ["enabled"]},
            ]
        }
    }
    if extra == "allow":
        absent.update(properties={}, additionalProperties=False)
    assert schema["allOf"] == [{"anyOf": [absent, {"required": ["name", "age"]}]}]
    response = TestClient(app).post("/", data={"name": "Rick", "age": "70"})
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
def test_optional_form_model_with_other_form_field_schema(extra):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra=extra)
        name: str
        age: int
        tags: list[str] = Field(default_factory=list)
        enabled: bool = True

    @app.post("/")
    def submit(
        token: Annotated[str, Form()],
        profile: Annotated[Profile | None, Form()] = None,
    ):
        return profile

    body, schema = form_schema(app)
    assert body["required"] is True
    assert schema["required"] == ["token"]
    absent = {
        "not": {
            "anyOf": [
                {"required": ["name"]},
                {"required": ["age"]},
                {"required": ["tags"]},
                {"required": ["enabled"]},
            ]
        }
    }
    if extra == "allow":
        absent.update(properties={"token": {}}, additionalProperties=False)
    assert schema["allOf"] == [{"anyOf": [absent, {"required": ["name", "age"]}]}]
    response = TestClient(app).post(
        "/", data={"token": "secret", "name": "Rick", "age": "70"}
    )
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
@pytest.mark.parametrize("required_name", [False, True])
def test_unknown_fields_and_sibling_models(extra, required_name):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra=extra)
        name: str = Field() if required_name else Field("default")
        enabled: bool = True

    class Credentials(BaseModel):
        token: str

    @app.post("/")
    def submit(
        credentials: Annotated[Credentials, Form()],
        avatar: Annotated[UploadFile | None, File()] = None,
        profile: Annotated[Profile | None, Form()] = None,
    ):
        return profile

    client = TestClient(app)
    response = client.post(
        "/", data={"token": "secret"}, files={"avatar": ("image.png", b"image")}
    )
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"token": "secret", "unknown": ["", "a"]})
    if extra == "forbid":
        assert response.status_code == 422
        assert response.json()["detail"][-1]["loc"] == ["body", "unknown"]
    elif extra == "allow" and required_name:
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "name"]
    else:
        assert response.status_code == 200, response.text
        assert response.json() == (
            {"name": "default", "enabled": False, "unknown": ["", "a"]}
            if extra == "allow"
            else None
        )
    response = client.post("/", data={"token": "secret", "name": ""})
    if required_name:
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "name"]
    else:
        assert response.status_code == 200, response.text
        assert response.json() == {"name": "default", "enabled": False}


@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
@pytest.mark.parametrize("required_field", [False, True])
def test_required_nullable_model(extra, required_field):
    app = FastAPI()

    class Settings(BaseModel):
        model_config = ConfigDict(extra=extra)
        name: str = Field() if required_field else Field("default")

    @app.post("/")
    def submit(settings: Annotated[Settings | None, Form()]):
        return settings

    @app.post("/plain")
    def plain(settings: Annotated[Settings, Form()]):
        return settings

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
    ]
    response = client.post("/", data={"name": ""})
    assert response.status_code == (422 if required_field else 200)
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick"}
    response = client.post("/plain")
    assert response.status_code == (422 if required_field else 200)
    response = client.post("/", data={"unknown": "x"})
    assert response.status_code == (
        200 if extra == "allow" and not required_field else 422
    )
    body, schema = form_schema(app)
    assert body["required"] is True
    if required_field:
        assert schema["required"] == ["name"]
        assert "allOf" not in schema
    else:
        assert "required" not in schema
        absent = {"not": {"anyOf": [{"required": ["name"]}]}}
        if extra == "allow":
            absent.update(properties={}, additionalProperties=False)
        assert schema["allOf"] == [{"not": absent}]


def test_defaults_factories_and_validators():
    app = FastAPI()
    calls = []

    class Profile(BaseModel):
        name: str = "default"
        enabled: bool = True
        tags: list[str] = Field(default_factory=list)

        @model_validator(mode="after")
        def validate_name(self):
            calls.append(self.name)
            return self

    default = Profile(name="parameter default")

    def factory():
        calls.append("factory")
        return Profile(name="factory default")

    @app.post("/")
    def submit(profile: Annotated[Profile | None, Form()] = default):
        assert profile is not None
        profile.tags.append("new")
        return profile

    @app.post("/factory")
    def from_factory(
        profile: Annotated[Profile | None, Form(default_factory=factory)],
    ):
        return profile

    @app.post("/validated-default")
    def validated_default(
        profile: Annotated[Profile | None, Form(validate_default=True)] = default,
    ):
        return profile

    client = TestClient(app)
    calls.clear()
    for _ in range(2):
        response = client.post("/")
        assert response.status_code == 200, response.text
        assert response.json() == {
            "name": "parameter default",
            "enabled": True,
            "tags": ["new"],
        }
    assert default.tags == []
    assert calls == []
    for _ in range(2):
        response = client.post("/factory")
        assert response.status_code == 200, response.text
        assert response.json()["enabled"] is True
    assert calls == ["factory", "factory default", "factory", "factory default"]
    calls.clear()
    response = client.post("/factory", data={"name": "submitted"})
    assert response.status_code == 200, response.text
    assert response.json()["enabled"] is False
    assert calls == ["submitted"]
    calls.clear()
    response = client.post("/validated-default")
    assert response.status_code == 200, response.text
    assert calls == ["parameter default"]
    assert "required" not in form_schema(app)[0]
    assert "required" not in form_schema(app, "/factory")[0]


@pytest.mark.parametrize("key", ["display_name", "nickname", "name"])
def test_aliases_and_shared_fields(key):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid", populate_by_name=True)
        name: str = Field(validation_alias=AliasChoices("display_name", "nickname"))

    class Other(BaseModel):
        name: str
        age: int

    @app.post("/")
    def submit(
        profile: Annotated[Profile | None, Form()] = None,
        other: Annotated[Other | None, Form()] = None,
    ):
        return [profile, other]

    client = TestClient(app)
    response = client.post("/", data={key: "Rick"})
    if key == "name":
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "age"]
    else:
        assert response.status_code == 200, response.text
        assert response.json() == [{"name": "Rick"}, None]
    response = client.post("/", data={key: "Rick", "name": "Rick", "age": "70"})
    if key == "name":
        assert response.status_code == 200, response.text
        assert response.json() == [{"name": "Rick"}, {"name": "Rick", "age": 70}]
    else:
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "extra_forbidden"


@pytest.mark.parametrize("alias_choices", [False, True])
@pytest.mark.parametrize("required", [False, True])
def test_shared_alias_activates_group_in_schema(alias_choices, required):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(populate_by_name=not alias_choices)
        name: str = Field(
            alias="display_name",
            validation_alias=AliasChoices("display_name", "name")
            if alias_choices
            else None,
        )
        department: str

    class Account(BaseModel):
        name: str

    @app.post("/")
    def submit(
        profile: Profile | None = Form(default=... if required else None),
        account: Annotated[Account | None, Form()] = None,
    ):
        return [profile, account]

    client = TestClient(app)
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "department"]
    response = client.post("/", data={"name": "Rick", "department": "Science"})
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"display_name": "Rick", "department": "Science"},
        {"name": "Rick"},
    ]
    _, schema = form_schema(app)
    name_requirement = {
        "anyOf": [{"required": ["display_name"]}, {"required": ["name"]}]
    }
    if required:
        assert schema["required"] == ["department"]
        assert schema["allOf"][0] == name_requirement
    else:
        assert "required" not in schema
        assert schema["allOf"][0] == {
            "anyOf": [
                {
                    "not": {
                        "anyOf": [
                            {"required": ["display_name"]},
                            {"required": ["name"]},
                            {"required": ["department"]},
                        ]
                    }
                },
                {"required": ["department"], "allOf": [name_requirement]},
            ]
        }


def test_dependency_override_names():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    def dependency(token: Annotated[str, Form()]):
        return token

    def override(new_token: Annotated[str, Form()]):
        return new_token

    @app.post("/")
    def submit(
        token: Annotated[str, Depends(dependency)],
        profile: Annotated[Profile | None, Form()] = None,
    ):
        return profile

    client = TestClient(app)
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    app.dependency_overrides[dependency] = override
    response = client.post("/", data={"new_token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() is None
    response = client.post("/", data={"new_token": "secret", "token": "old"})
    assert response.status_code == 422
    assert response.json()["detail"][-1]["loc"] == ["body", "token"]


def test_typing_optional():
    app = FastAPI()

    class Profile(BaseModel):
        name: str

    @app.post("/")
    def submit(profile: Annotated[Optional[Profile], Form()] = None):  # noqa: UP045
        return profile

    client = TestClient(app)
    assert client.post("/").json() is None
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick"}


def test_file_fields_and_empty_upload():
    app = FastAPI()

    class Attachment(BaseModel):
        content: UploadFile

    @app.post("/")
    def submit(attachment: Annotated[Attachment | None, Form()] = None):
        if attachment is not None:
            return {
                "filename": attachment.content.filename,
                "size": attachment.content.size,
            }
        return None

    client = TestClient(app)
    assert client.post("/").json() is None
    response = client.post("/", files={"content": ("empty.txt", b"")})
    assert response.status_code == 200, response.text
    assert response.json() == {"filename": "empty.txt", "size": 0}
    response = client.post(
        "/",
        content=(
            '--boundary\r\nContent-Disposition: form-data; name="content"; '
            'filename=""\r\nContent-Type: application/octet-stream\r\n\r\n'
            "\r\n--boundary--\r\n"
        ),
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "content"]


@pytest.mark.parametrize("required", [False, True])
@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
def test_model_without_declared_fields(required, extra):
    app = FastAPI()

    class Empty(BaseModel):
        model_config = ConfigDict(extra=extra)

    @app.post("/")
    def submit(model: Empty | None = Form(default=... if required else None)):
        return model

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == (422 if required else 200)
    response = client.post("/", data={"unknown": "value"})
    if extra == "forbid" or (required and extra == "ignore"):
        assert response.status_code == 422
    else:
        assert response.status_code == 200, response.text
        assert response.json() == ({"unknown": "value"} if extra == "allow" else None)
    body, schema = form_schema(app)
    assert body.get("required", False) == required
    assert schema["properties"] == {}
    if required:
        assert schema["allOf"] == [
            {
                "not": {"properties": {}, "additionalProperties": False}
                if extra == "allow"
                else {}
            }
        ]
    else:
        assert "allOf" not in schema
