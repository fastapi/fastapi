from typing import Annotated

import pytest
from fastapi import Depends, FastAPI, Security
from fastapi.testclient import TestClient


@pytest.fixture(name="call_counter")
def call_counter_fixture():
    return {"count": 0}


@pytest.fixture(name="app")
def app_fixture(call_counter: dict[str, int]):
    def get_db():
        call_counter["count"] += 1
        return f"db_{call_counter['count']}"

    def get_user(db: Annotated[str, Depends(get_db)]):
        return "user"

    app = FastAPI()

    @app.get("/")
    def endpoint(
        db: Annotated[str, Depends(get_db)],
        user: Annotated[str, Security(get_user, scopes=["read"])],
    ):
        return {"db": db}

    return app


@pytest.fixture(name="client")
def client_fixture(app: FastAPI):
    return TestClient(app)


def test_security_scopes_dependency_called_once(
    client: TestClient, call_counter: dict[str, int]
):
    response = client.get("/")

    assert response.status_code == 200
    assert call_counter["count"] == 1
