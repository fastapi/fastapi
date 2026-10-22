from typing import Annotated
from urllib.parse import urlencode

import pytest
from fastapi import APIRouter, Depends, FastAPI, File, Form, Query, UploadFile
from fastapi.testclient import TestClient
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


def form_schema(app, path="/", media_type="application/x-www-form-urlencoded"):
    schema = app.openapi()
    body = schema["paths"][path]["post"]["requestBody"]
    ref = body["content"][media_type]["schema"]["$ref"]
    return schema["components"]["schemas"][ref.rsplit("/", 1)[-1]]


def post_form(client, path, fields, multipart):
    if multipart:
        return client.post(path, files=[(key, (None, value)) for key, value in fields])
    return client.post(
        path,
        content=urlencode(fields),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )


@pytest.mark.parametrize("multipart", [False, True])
@pytest.mark.parametrize("path", ["/", "/dependency"])
def test_composed_form_models_ignore_extras(multipart, path):
    app = FastAPI()

    class Profile(BaseModel):
        name: str

    class Preferences(BaseModel):
        limit: int = Field(10, ge=1, description="Result limit")
        tags: list[str] = Field(default_factory=list)

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        return {"profile": profile, "preferences": preferences, "token": token}

    def profile_dependency(profile: Annotated[Profile, Form()]):
        return profile

    @app.post("/dependency")
    def submit_dependency(
        profile: Annotated[Profile, Depends(profile_dependency)],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        return {"profile": profile, "preferences": preferences, "token": token}

    client = TestClient(app)
    fields = [("name", "Rick"), ("token", "secret")]
    response = post_form(
        client, path, fields + [("limit", "2"), ("tags", "a"), ("tags", "b")], multipart
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "profile": {"name": "Rick"},
        "preferences": {"limit": 2, "tags": ["a", "b"]},
        "token": "secret",
    }
    response = post_form(client, path, fields, multipart)
    assert response.status_code == 200, response.text
    assert response.json()["preferences"] == {"limit": 10, "tags": []}
    response = post_form(client, path, fields + [("limit", "0")], multipart)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "limit"]
    response = post_form(
        client, path, fields + [("unknown", "a"), ("unknown", "b")], multipart
    )
    assert response.status_code == 200, response.text
    for key in ("profile", "preferences"):
        assert "unknown" not in response.json()[key]
    response = post_form(client, path, [("token", "secret")], multipart)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "name"]
    schema = form_schema(app, path)
    assert set(schema["properties"]) == {"token"}
    assert schema["required"] == ["token"]
    assert {item["$ref"] for item in schema["allOf"]} == {
        "#/components/schemas/Profile",
        "#/components/schemas/Preferences",
    }
    models = app.openapi()["components"]["schemas"]
    assert models["Preferences"]["properties"]["limit"]["minimum"] == 1
    assert "additionalProperties" not in models["Profile"]


@pytest.mark.parametrize("multipart", [False, True])
@pytest.mark.parametrize("path", ["/", "/dependency"])
def test_composed_form_models_allow_extras(multipart, path):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="allow")
        name: str

    class Preferences(BaseModel):
        model_config = ConfigDict(extra="allow")
        limit: int = Field(10, ge=1)
        tags: list[str] = Field(default_factory=list)

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        return {"profile": profile, "preferences": preferences, "token": token}

    def profile_dependency(profile: Annotated[Profile, Form()]):
        return profile

    @app.post("/dependency")
    def submit_dependency(
        profile: Annotated[Profile, Depends(profile_dependency)],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        return {"profile": profile, "preferences": preferences, "token": token}

    client = TestClient(app)
    fields = [("name", "Rick"), ("token", "secret")]
    response = post_form(
        client, path, fields + [("limit", "2"), ("tags", "a"), ("tags", "b")], multipart
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "profile": {
            "name": "Rick",
            "limit": "2",
            "tags": ["a", "b"],
            "token": "secret",
        },
        "preferences": {
            "limit": 2,
            "tags": ["a", "b"],
            "name": "Rick",
            "token": "secret",
        },
        "token": "secret",
    }
    response = post_form(client, path, fields, multipart)
    assert response.status_code == 200, response.text
    assert response.json()["preferences"] == {
        "limit": 10,
        "tags": [],
        "name": "Rick",
        "token": "secret",
    }
    response = post_form(client, path, fields + [("limit", "0")], multipart)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "limit"]
    response = post_form(
        client, path, fields + [("unknown", "a"), ("unknown", "b")], multipart
    )
    assert response.status_code == 200, response.text
    for key in ("profile", "preferences"):
        assert response.json()[key]["unknown"] == ["a", "b"]
    response = post_form(client, path, [("token", "secret")], multipart)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "name"]
    models = app.openapi()["components"]["schemas"]
    assert models["Profile"]["additionalProperties"] is True
    assert models["Preferences"]["additionalProperties"] is True


@pytest.mark.parametrize("multipart", [False, True])
@pytest.mark.parametrize("path", ["/", "/dependency"])
def test_composed_form_models_forbid_extras(multipart, path):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    class Preferences(BaseModel):
        model_config = ConfigDict(extra="forbid")
        limit: int = 10
        tags: list[str] = Field(default_factory=list)

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        pytest.fail("Invalid form data reached the endpoint")  # pragma: no cover

    def profile_dependency(profile: Annotated[Profile, Form()]):
        pytest.fail("Invalid form data reached the dependency")  # pragma: no cover

    @app.post("/dependency")
    def submit_dependency(
        profile: Annotated[Profile, Depends(profile_dependency)],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        pytest.fail("Invalid form data reached the endpoint")  # pragma: no cover

    response = post_form(
        TestClient(app),
        path,
        [
            ("name", "Rick"),
            ("token", "secret"),
            ("limit", "2"),
            ("tags", "a"),
            ("tags", "b"),
        ],
        multipart,
    )
    assert response.status_code == 422
    assert {error["loc"][-1] for error in response.json()["detail"]} == {
        "limit",
        "tags",
        "token",
        "name",
    }
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )
    models = app.openapi()["components"]["schemas"]
    assert models["Profile"]["additionalProperties"] is False
    assert models["Preferences"]["additionalProperties"] is False


def test_model_defaults_checkboxes_and_validators_are_independent():
    app = FastAPI()
    inputs = []

    class Settings(BaseModel):
        label: str = "default"
        enabled: bool = True
        tags: list[str] = Field(default_factory=list)

        @model_validator(mode="before")
        @classmethod
        def check_input(cls, value):
            inputs.append(value.copy())
            return value

        @model_validator(mode="after")
        def check_label(self):
            if self.label == "invalid":
                raise ValueError("Invalid label")
            return self

    class OtherSettings(BaseModel):
        label: str = "other"
        enabled: str = "other"

    @app.post("/")
    def submit(
        settings: Annotated[Settings, Form()],
        other: Annotated[OtherSettings, Form()],
        token: Annotated[str, Form()] = "secret",
    ):
        return {
            "settings": settings,
            "other": other,
            "fields_set": sorted(settings.model_fields_set),
            "other_fields_set": sorted(other.model_fields_set),
        }

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "settings": {"label": "default", "enabled": False, "tags": []},
        "other": {"label": "other", "enabled": "other"},
        "fields_set": ["enabled"],
        "other_fields_set": [],
    }
    response = client.post(
        "/", data={"label": "", "enabled": "", "tags": ["", "a"], "token": "ok"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "settings": {"label": "default", "enabled": True, "tags": ["", "a"]},
        "other": {"label": "other", "enabled": "other"},
        "fields_set": ["tags"],
        "other_fields_set": [],
    }
    assert inputs[-1]["token"] == "ok"
    response = client.post("/", data={"label": "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body"]


@pytest.mark.parametrize("required_first", [False, True])
def test_aliases_shared_fields_and_cached_models(required_first):
    app = FastAPI()

    class First(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        value: int = Field(alias="first", description="First value")
        shared: int = Field() if required_first else Field(10)

    class Second(BaseModel):
        value: int = Field(alias="second")
        shared: int = Field(10) if required_first else Field()

    @app.post("/")
    def submit(first: Annotated[First, Form()], second: Annotated[Second, Form()]):
        return [first, second]

    @app.post("/single")
    def single(data: Annotated[First, Form()]):
        return data

    @app.post("/json")
    def json_body(first: First, second: Second):
        return [first, second]

    client = TestClient(app)
    response = client.post("/", data={"value": "1", "second": "2", "shared": "3"})
    assert response.status_code == 200, response.text
    expected = [{"first": 1, "shared": 3}, {"second": 2, "shared": 3}]
    assert response.json() == expected
    assert client.post("/", data={"first": "1", "second": "2"}).status_code == 422
    schema = form_schema(app)
    original_schema = app.openapi()["components"]["schemas"]["First"]
    assert schema["allOf"] == [
        {
            **original_schema,
            "required": ["shared"] if required_first else [],
            "allOf": [{"anyOf": [{"required": ["first"]}, {"required": ["value"]}]}],
        },
        {"$ref": "#/components/schemas/Second"},
    ]
    assert set(form_schema(app, "/single")["properties"]) == {"first", "shared"}
    assert set(form_schema(app, "/json", "application/json")["properties"]) == {
        "first",
        "second",
    }
    assert First.model_fields["value"].alias == "first"
    assert First.model_fields["shared"].alias is None
    assert First.model_fields["shared"].is_required() is required_first
    response = client.post("/single", data={"first": "4", "shared": "5"})
    assert response.status_code == 200, response.text
    assert response.json() == {"first": 4, "shared": 5}
    response = client.post(
        "/json",
        json={"first": {"first": 1, "shared": 3}, "second": {"second": 2, "shared": 3}},
    )
    assert response.status_code == 200, response.text


def test_shared_alias_choices_keep_shapes_and_unused_extras():
    app = FastAPI()

    class Many(BaseModel):
        model_config = ConfigDict(extra="forbid")
        names: list[str] = Field(validation_alias=AliasChoices("names", "legacy"))

    class One(BaseModel):
        text: str = Field(alias="legacy")

    @app.post("/")
    def submit(
        many: Annotated[Many, Form()],
        one: Annotated[One, Form()],
        legacy: Annotated[str, Form()],
    ):
        return {"many": many, "one": one, "last": legacy}

    client = TestClient(app)
    response = client.post("/", data={"legacy": ["first", "last"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "many": {"names": ["first", "last"]},
        "one": {"legacy": "last"},
        "last": "last",
    }
    response = client.post("/", data={"names": "first", "legacy": "last"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "legacy"]


def test_nested_dependencies_overrides_and_request_locations():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    class Preferences(BaseModel):
        limit: int = 10

    def preferences(data: Annotated[Preferences, Form()]):
        return data.limit

    def replacement(page: Annotated[int, Form()] = 1):
        return page

    def nested(value: Annotated[int, Depends(preferences)]):
        return value

    def token(token: Annotated[str, Form()] = "secret"):
        return token

    router = APIRouter(dependencies=[Depends(token)])

    @router.post("/")
    def submit(
        data: Annotated[Profile, Form()],
        value: Annotated[int, Depends(nested)],
        query: Annotated[str, Query()] = "default",
    ):
        return {"data": data, "value": value}

    app.include_router(router)
    client = TestClient(app)
    response = client.post("/?query=ok", data={"name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"data": {"name": "Rick"}, "value": 10}
    fields = {"name": "Rick", "token": "secret"}
    response = client.post("/?query=ok", data={**fields, "limit": "2"})
    assert response.status_code == 422
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )
    assert {error["loc"][-1] for error in response.json()["detail"]} == {
        "token",
        "limit",
    }
    app.dependency_overrides[preferences] = replacement
    response = client.post("/?query=ok", data={**fields, "page": "3"})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["body", "token"],
        ["body", "page"],
    ]
    assert all(
        error["type"] == "extra_forbidden" for error in response.json()["detail"]
    )


@pytest.mark.parametrize("content", [b"", b"hello"])
def test_form_model_and_files_shared_with_dependencies(content):
    app = FastAPI()

    class Profile(BaseModel):
        name: str

    def inspect_files(
        profile: Annotated[Profile, Form()], files: Annotated[list[bytes], File()]
    ):
        return {"profile": profile, "files": [file.decode() for file in files]}

    @app.post("/")
    async def submit(
        inspected: Annotated[dict, Depends(inspect_files)],
        profile: Annotated[Profile, Form()],
        files: Annotated[list[UploadFile], File()],
        last: Annotated[bytes, File(alias="files")],
    ):
        return {
            "inspected": inspected,
            "profile": profile,
            "positions": [file.file.tell() for file in files],
            "files": [(await file.read()).decode() for file in files],
            "last": last.decode(),
        }

    client = TestClient(app)
    response = client.post(
        "/",
        data={"name": "Rick"},
        files=[("files", ("one.txt", b"one")), ("files", ("two.txt", content))],
    )
    assert response.status_code == 200, response.text
    expected_files = ["one", content.decode()]
    assert response.json() == {
        "inspected": {"profile": {"name": "Rick"}, "files": expected_files},
        "profile": {"name": "Rick"},
        "positions": [0, 0],
        "files": expected_files,
        "last": content.decode(),
    }
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 422
    assert all(error["loc"] == ["body", "files"] for error in response.json()["detail"])
    schema = form_schema(app, media_type="multipart/form-data")
    assert set(schema["properties"]) == {"files"}
    assert schema["required"] == ["files"]
    assert schema["properties"]["files"]["type"] == "array"
    assert any(
        item.get("properties", {}).get("files", {}).get("type") == "string"
        for item in schema["allOf"]
    )


def test_models_with_the_same_parameter_name_in_dependencies():
    app = FastAPI()

    class First(BaseModel):
        first: int

    class Second(BaseModel):
        second: int

    def dependency(data: Annotated[First, Form()]):
        return data

    @app.post("/")
    def submit(
        data: Annotated[Second, Form()], first: Annotated[First, Depends(dependency)]
    ):
        return [first, data]

    response = TestClient(app).post("/", data={"first": "1", "second": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"first": 1}, {"second": 2}]
    assert {item["$ref"] for item in form_schema(app)["allOf"]} == {
        "#/components/schemas/First",
        "#/components/schemas/Second",
    }


def test_optional_file_with_a_form_model():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()],
        attachment: Annotated[bytes | None, File()] = None,
    ):
        return {"profile": profile, "attachment": attachment}

    client = TestClient(app)
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"profile": {"name": "Rick"}, "attachment": None}
    response = client.post(
        "/", data={"name": "Rick"}, files={"attachment": ("empty.txt", b"")}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "attachment"]
    assert response.json()["detail"][0]["type"] == "extra_forbidden"
    schema = form_schema(app, media_type="multipart/form-data")
    assert "required" not in schema
    assert schema["allOf"][0]["$ref"] == "#/components/schemas/Profile"
    assert (
        app.openapi()["components"]["schemas"]["Profile"]["additionalProperties"]
        is False
    )


def test_dependency_override_adds_a_form_parameter():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    def token():
        return "default"

    def replacement(token: Annotated[str, Form()]):
        return token

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()], value: Annotated[str, Depends(token)]
    ):
        return {"profile": profile, "token": value}

    client = TestClient(app)
    app.dependency_overrides[token] = replacement
    response = client.post("/", data={"name": "Rick", "token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "token"]
    assert response.json()["detail"][0]["type"] == "extra_forbidden"
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "token"]
    app.dependency_overrides.clear()
    response = client.post("/", data={"name": "Rick", "token": "secret"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "token"]
    response = client.post("/", data={"name": "Rick"})
    assert response.status_code == 200, response.text
    assert response.json() == {"profile": {"name": "Rick"}, "token": "default"}


def test_forbid_models_can_validate_the_same_fields():
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str
        age: int

    class Adult(Profile):
        age: int = Field(ge=18)

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()],
        adult: Annotated[Adult, Form()],
        name: Annotated[str, Form()],
    ):
        return [profile, adult, name]

    client = TestClient(app)
    response = client.post("/", data={"name": "Rick", "age": "70"})
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "Rick", "age": 70},
        {"name": "Rick", "age": 70},
        "Rick",
    ]
    response = client.post("/", data={"name": "Rick", "age": "17"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "greater_than_equal"
    response = client.post("/", data={"name": "Rick", "age": "70", "token": "secret"})
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["body", "token"],
        ["body", "token"],
    ]
    schemas = app.openapi()["components"]["schemas"]
    assert {item["$ref"] for item in schemas["Body_submit__post"]["allOf"]} == {
        "#/components/schemas/Profile",
        "#/components/schemas/Adult",
    }
    assert schemas["Profile"]["additionalProperties"] is False
    assert schemas["Adult"]["additionalProperties"] is False
