import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial004_py310", "tutorial004_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")
    return TestClient(mod.app)


def test_form_model_and_file(client: TestClient):
    response = client.post(
        "/profiles/", data={"name": "Rick"}, files={"avatar": ("avatar.png", b"image")}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"profile": {"name": "Rick"}, "filename": "avatar.png"}


def test_missing_file(client: TestClient):
    response = client.post("/profiles/", data={"name": "Rick"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "avatar"]


def test_openapi(client: TestClient):
    schema = client.get("/openapi.json").json()
    body = schema["paths"]["/profiles/"]["post"]["requestBody"]
    assert set(body["content"]) == {"multipart/form-data"}
    model = schema["components"]["schemas"]["Body_create_profile_profiles__post"]
    assert model["properties"] == {
        "avatar": {
            "type": "string",
            "contentMediaType": "application/octet-stream",
            "title": "Avatar",
        },
    }
    assert model["required"] == ["avatar"]
    assert model["allOf"][0]["$ref"] == "#/components/schemas/Profile"
    assert schema["components"]["schemas"]["Profile"]["required"] == ["name"]
