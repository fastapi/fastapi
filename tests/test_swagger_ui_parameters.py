import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def good_client():
    app = FastAPI(
        swagger_ui_parameters={
            "syntaxHighlight": False,
            "syntaxHighlight.theme": "obsidian",
        }
    )

    @app.get("/items/")
    async def read_items():
        return {"id": "foo"}

    client = TestClient(app)

    return client


@pytest.fixture(scope="module")
def bad_client():
    app = FastAPI(
        swagger_ui_parameters={
            # Sets are not JSON serializable
            "badParameter": {"bar"},
        }
    )

    @app.get("/items/")
    async def read_items():
        return {"id": "foo"}

    client = TestClient(app)

    return client


def test_swagger_ui(good_client):
    response = good_client.get("/docs")
    assert response.status_code == 200, response.text
    assert "syntaxHighlight: false," in response.text
    assert 'syntaxHighlight.theme: "obsidian",' in response.text


def test_response(good_client):
    response = good_client.get("/items/")
    assert response.json() == {"id": "foo"}


def test_bad_value(bad_client):
    with pytest.raises(TypeError):
        bad_client.get("/docs")
