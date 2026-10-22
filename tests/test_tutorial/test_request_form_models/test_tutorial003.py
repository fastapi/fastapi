import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial003_py310", "tutorial003_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")
    return TestClient(mod.app)


def test_form_models(client: TestClient):
    response = client.post(
        "/profiles/",
        data={"name": "Rick", "tags": ["python", "fastapi"], "token": "secret"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "profile": {"name": "Rick"},
        "preferences": {"tags": ["python", "fastapi"]},
        "token": "secret",
    }
    response = client.post("/profiles/", data={"name": "Rick", "token": "secret"})
    assert response.status_code == 200, response.text
    assert response.json()["preferences"] == {"tags": []}


def test_openapi(client: TestClient):
    schema = client.get("/openapi.json").json()
    body = schema["components"]["schemas"]["Body_create_profile_profiles__post"]
    assert set(body["properties"]) == {"token"}
    assert body["required"] == ["token"]
    assert {item["$ref"] for item in body["allOf"]} == {
        "#/components/schemas/Profile",
        "#/components/schemas/Preferences",
    }
    assert schema["components"]["schemas"]["Profile"]["required"] == ["name"]
