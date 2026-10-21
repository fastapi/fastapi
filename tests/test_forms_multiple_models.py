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


@pytest.mark.parametrize("multipart", [False, True])
@pytest.mark.parametrize("in_dependency", [False, True])
@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
def test_composed_form_models(multipart, in_dependency, extra):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra=extra)
        name: str

    class Preferences(BaseModel):
        model_config = ConfigDict(extra=extra)
        limit: int = Field(10, ge=1, description="Result limit")
        tags: list[str] = Field(default_factory=list)

    def profile_dependency(profile: Annotated[Profile, Form()]):
        return profile

    marker = Depends(profile_dependency) if in_dependency else Form()

    @app.post("/")
    def submit(
        profile: Annotated[Profile, marker],
        preferences: Annotated[Preferences, Form()],
        token: Annotated[str, Form()],
    ):
        return {"profile": profile, "preferences": preferences, "token": token}

    client = TestClient(app)

    def send(fields):
        if multipart:
            return client.post("/", files=[(k, (None, v)) for k, v in fields])
        return client.post(
            "/",
            content=urlencode(fields),
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

    fields = [("name", "Rick"), ("token", "secret")]
    response = send(fields + [("limit", "2"), ("tags", "a"), ("tags", "b")])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "profile": {"name": "Rick"},
        "preferences": {"limit": 2, "tags": ["a", "b"]},
        "token": "secret",
    }
    response = send(fields)
    assert response.status_code == 200, response.text
    assert response.json()["preferences"] == {"limit": 10, "tags": []}
    response = send(fields + [("limit", "0")])
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "limit"]
    response = send(fields + [("unknown", "a"), ("unknown", "b")])
    if extra == "forbid":
        assert response.status_code == 422
        assert [error["loc"] for error in response.json()["detail"]] == [
            ["body", "unknown"],
            ["body", "unknown"],
        ]
    else:
        assert response.status_code == 200, response.text
        for key in ("profile", "preferences"):
            if extra == "allow":
                assert response.json()[key]["unknown"] == ["a", "b"]
            else:
                assert "unknown" not in response.json()[key]
    response = send([("token", "secret")])
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "name"]
    schema = form_schema(app)
    assert set(schema["properties"]) == {"name", "limit", "tags", "token"}
    assert set(schema["required"]) == {"name", "token"}
    assert schema["properties"]["limit"] == {
        "type": "integer",
        "minimum": 1,
        "title": "Limit",
        "description": "Result limit",
        "default": 10,
    }
    if extra == "forbid":
        assert schema["additionalProperties"] is False
    elif extra == "allow":
        assert schema["additionalProperties"] is True


def test_model_defaults_checkboxes_and_validators_are_independent():
    app = FastAPI()

    class Settings(BaseModel):
        label: str = "default"
        enabled: bool = True
        tags: list[str] = Field(default_factory=list)

        @model_validator(mode="before")
        @classmethod
        def check_input(cls, value):
            assert "token" not in value
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
    response = client.post("/", data={"label": "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body"]


@pytest.mark.parametrize("required_first", [False, True])
def test_aliases_shared_fields_and_cached_models(required_first):
    app = FastAPI()

    class First(BaseModel):
        model_config = ConfigDict(extra="forbid", populate_by_name=True)
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
    assert set(schema["properties"]) == {"first", "second", "shared"}
    assert set(schema["required"]) == {"first", "second", "shared"}
    assert "default" not in schema["properties"]["shared"]
    assert schema["additionalProperties"] is False
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
        model_config = ConfigDict(extra="forbid")
        limit: int

    def preferences(data: Annotated[Preferences, Form()]):
        return data.limit

    def replacement(page: Annotated[int, Form()] = 1):
        return page

    def nested(value: Annotated[int, Depends(preferences)]):
        return value

    def token(token: Annotated[str, Form()]):
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
    fields = {"name": "Rick", "token": "secret"}
    response = client.post("/?query=ok", data={**fields, "limit": "2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"data": {"name": "Rick"}, "value": 2}
    assert set(form_schema(app)["properties"]) == {"name", "limit", "token"}
    app.dependency_overrides[preferences] = replacement
    response = client.post("/", data={**fields, "page": "3"})
    assert response.status_code == 200, response.text
    assert response.json()["value"] == 3
    for unknown in ("limit", "query"):
        response = client.post("/", data={**fields, unknown: "2"})
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", unknown]
    app.dependency_overrides.clear()
    assert client.post("/", data={**fields, "limit": "4"}).status_code == 200


@pytest.mark.parametrize("content", [b"", b"hello"])
def test_form_model_and_files_shared_with_dependencies(content):
    app = FastAPI()

    class Profile(BaseModel):
        model_config = ConfigDict(extra="forbid")
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
    assert set(schema["properties"]) == {"name", "files"}
    assert set(schema["required"]) == {"name", "files"}
    assert schema["properties"]["files"]["type"] == "array"
    assert schema["additionalProperties"] is False


def test_models_with_the_same_parameter_name_in_dependencies():
    app = FastAPI()

    class First(BaseModel):
        model_config = ConfigDict(extra="forbid")
        first: int

    class Second(BaseModel):
        model_config = ConfigDict(extra="forbid")
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
    assert set(form_schema(app)["properties"]) == {"first", "second"}


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
    assert response.status_code == 200, response.text
    assert response.json() == {"profile": {"name": "Rick"}, "attachment": ""}
    assert form_schema(app, media_type="multipart/form-data")["required"] == ["name"]


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
    assert response.status_code == 200, response.text
    assert response.json() == {"profile": {"name": "Rick"}, "token": "secret"}
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
