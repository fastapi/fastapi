from typing import Annotated, Optional

import pytest
from fastapi import Depends, FastAPI, File, Form, UploadFile
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
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
    absent = (
        {"maxProperties": 0}
        if extra in ("allow", "forbid")
        else {
            "not": {
                "anyOf": [
                    {"required": [name]} for name in ["age", "enabled", "name", "tags"]
                ]
            }
        }
    )
    assert schema["allOf"] == [
        {
            "anyOf": [
                absent,
                {
                    "anyOf": [{"$ref": "#/components/schemas/Profile"}],
                    "title": "Profile",
                },
            ]
        }
    ]
    assert app.openapi()["components"]["schemas"]["Profile"]["required"] == [
        "name",
        "age",
    ]
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
    absent = (
        {"maxProperties": 0}
        if extra in ("allow", "forbid")
        else {
            "not": {
                "anyOf": [
                    {"required": [name]} for name in ["age", "enabled", "name", "tags"]
                ]
            }
        }
    )
    assert schema["allOf"] == [
        {
            "anyOf": [
                absent,
                {
                    "anyOf": [{"$ref": "#/components/schemas/Profile"}],
                    "title": "Profile",
                },
            ]
        }
    ]
    assert app.openapi()["components"]["schemas"]["Profile"]["required"] == [
        "name",
        "age",
    ]
    response = TestClient(app).post(
        "/", data={"token": "secret", "name": "Rick", "age": "70"}
    )
    assert response.status_code == (422 if extra == "forbid" else 200), response.text


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
        if profile is not None and avatar is not None:
            assert profile.model_extra is not None
            assert profile.model_extra["avatar"] is avatar
            return {
                **profile.model_dump(exclude={"avatar"}),
                "avatar": {"filename": avatar.filename},
            }
        return profile

    client = TestClient(app)
    response = client.post(
        "/", data={"token": "secret"}, files={"avatar": ("image.png", b"image")}
    )
    if extra == "ignore":
        assert response.status_code == 200, response.text
        assert response.json() is None
    elif extra == "forbid":
        assert response.status_code == 422
        assert {
            error["loc"][-1]
            for error in response.json()["detail"]
            if error["type"] == "extra_forbidden"
        } == {"token", "avatar"}
    elif required_name:
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "name"]
    else:
        assert response.status_code == 200, response.text
        assert response.json()["token"] == "secret"
        assert response.json()["avatar"]["filename"] == "image.png"
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
            {
                "name": "default",
                "enabled": False,
                "token": "secret",
                "unknown": ["", "a"],
            }
            if extra == "allow"
            else None
        )
    response = client.post("/", data={"token": "secret", "name": ""})
    if required_name or extra == "forbid":
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == [
            "body",
            "name" if required_name else "token",
        ]
    else:
        assert response.status_code == 200, response.text
        assert response.json() == {
            "name": "default",
            "enabled": False,
            **({"token": "secret"} if extra == "allow" else {}),
        }


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
    assert "required" not in schema
    absent = (
        {"maxProperties": 0}
        if extra in ("allow", "forbid")
        else {"not": {"anyOf": [{"required": ["name"]}]}}
    )
    assert schema["allOf"] == [
        {"not": absent},
        {"anyOf": [{"$ref": "#/components/schemas/Settings"}], "title": "Settings"},
    ]


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
    assert response.status_code == 422
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )
    assert response.json()["detail"][-1]["loc"] == ["body", "age"]


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

    @app.post("/json")
    def json_body(profile: Profile):
        return profile

    client = TestClient(app)
    response = client.post("/json", json={"name": "Rick", "department": "Science"})
    assert response.status_code == 200, response.text
    assert response.json() == {"display_name": "Rick", "department": "Science"}
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
    model_schema = app.openapi()["components"]["schemas"]["Profile"]
    assert model_schema["required"] == ["display_name", "department"]
    present = schema["allOf"][1] if required else schema["allOf"][0]["anyOf"][1]
    assert present["anyOf"][0] == {
        **model_schema,
        "required": ["department"],
        "allOf": [{"anyOf": [{"required": ["display_name"]}, {"required": ["name"]}]}],
    }
    for key in ("display_name", "name"):
        data = {key: "Rick", "department": "Science"}
        assert client.post("/", data=data).status_code == 200
        assert client.post("/", data={key: "Rick"}).status_code == 422


def test_standalone_optional_form_model_alias_schema():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        name: str = Field(alias="display_name")

    @app.post("/")
    def submit(profile: Annotated[Profile | None, Form()] = None):
        return profile

    client = TestClient(app)
    _, schema = form_schema(app)
    present = schema["allOf"][0]["anyOf"][1]["anyOf"][0]
    assert present["required"] == []
    assert present["allOf"] == [
        {"anyOf": [{"required": ["display_name"]}, {"required": ["name"]}]}
    ]
    for data in ({}, {"name": "Rick"}, {"display_name": "Rick"}):
        assert client.post("/", data=data).status_code == 200


@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
    reason="validate_by_alias requires Pydantic 2.11+",
)
@pytest.mark.parametrize(
    "field_info",
    [
        Field(alias="display_name"),
        Field(validation_alias=AliasChoices("display_name", "nickname")),
    ],
)
def test_form_model_schema_with_disabled_aliases(field_info):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(validate_by_alias=False)
        name: str = field_info
        department: str = "Science"

    @app.post("/optional")
    def optional(profile: Annotated[Profile | None, Form()] = None):
        return profile.name if profile is not None else None

    @app.post("/composed")
    def composed(
        profile: Annotated[Profile, Form()], token: Annotated[str, Form()] = "secret"
    ):
        return profile.name

    @app.post("/json")
    def json_body(profile: Profile):
        return profile

    client = TestClient(app)
    response = client.post("/json", json={"name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == Profile(name="Rick").model_dump(by_alias=True)
    for path in ("/optional", "/composed"):
        response = client.post(path, data={"name": "Rick"})
        assert response.status_code == 200, response.text
        assert response.json() == "Rick"
    assert client.post("/composed", data={"display_name": "Rick"}).status_code == 422
    _, optional_schema = form_schema(app, "/optional")
    _, composed_schema = form_schema(app, "/composed")
    optional_model = optional_schema["allOf"][0]["anyOf"][1]["anyOf"][0]
    composed_model = composed_schema["allOf"][0]
    assert optional_model == composed_model
    schemas = app.openapi()["components"]["schemas"]
    ref_name = composed_model.get("$ref", "").rsplit("/", 1)[-1]
    composed_model = schemas.get(ref_name, composed_model)
    assert set(composed_model["properties"]) == {"name", "department"}
    assert composed_model["required"] == ["name"]
    assert schemas["Profile"] == Profile.model_json_schema()


def test_dependency_override_names():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    def dependency(token: Annotated[str, Form()] = "secret"):
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
    assert client.post("/").json() is None
    response = client.post("/", data={"token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"][-1]["loc"] == ["body", "token"]
    app.dependency_overrides[dependency] = override
    response = client.post("/", data={"new_token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"][-1]["loc"] == ["body", "new_token"]
    assert response.json()["detail"][-1]["type"] == "extra_forbidden"


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
    absent = {"maxProperties": 0} if extra in ("allow", "forbid") else {}
    present = {"anyOf": [{"$ref": "#/components/schemas/Empty"}], "title": "Model"}
    if required:
        assert schema["allOf"] == [{"not": absent}, present]
    else:
        assert schema["allOf"] == [{"anyOf": [absent, present]}]
    assert app.openapi()["components"]["schemas"]["Empty"]["properties"] == {}
