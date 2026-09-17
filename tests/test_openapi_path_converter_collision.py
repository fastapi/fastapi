import warnings

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_collision_emits_warning():
    app = FastAPI()

    @app.get("/items/{item_id:int}")
    def get_int(item_id: int):
        return {"id": item_id}

    @app.get("/items/{item_id:str}")
    def get_str(item_id: str):
        return {"id": item_id}

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        client.get("/openapi.json")

    assert len(caught_warnings) == 1
    assert "Duplicate OpenAPI path" in str(caught_warnings[0].message)
    assert "/items/{item_id}" in str(caught_warnings[0].message)


def test_no_collision_no_warning():
    app = FastAPI()

    @app.get("/items/{item_id:int}")
    def get_int(item_id: int):
        return {"id": item_id}

    @app.get("/items/{name:str}")
    def get_str(name: str):
        return {"id": name}

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        client.get("/openapi.json")

    assert not any(
        "Duplicate OpenAPI path" in str(warning.message) for warning in caught_warnings
    )


def test_collision_spec_contains_normalized_path():
    app = FastAPI()

    @app.get("/toto/{tata:str}")
    def tutu(tata: str) -> str:
        return tata

    @app.get("/toto/{tata:int}")
    def titi(tata: int) -> int:
        return tata

    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/toto/{tata}" in response.json()["paths"]


def test_webhook_collision_emits_warning():
    app = FastAPI()

    @app.webhooks.post("/events/{event_id:int}")
    def post_int(event_id: int):
        return {"id": event_id}

    @app.webhooks.post("/events/{event_id:str}")
    def post_str(event_id: str):
        return {"id": event_id}

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        client.get("/openapi.json")

    assert len(caught_warnings) == 1
    assert "Duplicate OpenAPI path" in str(caught_warnings[0].message)
    assert "/events/{event_id}" in str(caught_warnings[0].message)
