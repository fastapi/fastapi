import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client_and_mod",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_client_and_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.kubernetes_probes.{request.param}")
    # Reset state
    mod.app_state.is_ready = False
    mod.app_state.db_healthy = True
    return mod


def test_liveness_probe(client_and_mod):
    mod = client_and_mod
    with TestClient(mod.app) as client:
        response = client.get("/livez")
        assert response.status_code == 200, response.text
        assert response.json() == {"status": "ok"}


def test_readiness_probe_success(client_and_mod):
    mod = client_and_mod
    with TestClient(mod.app) as client:
        response = client.get("/readyz")
        assert response.status_code == 200, response.text
        assert response.json() == {"status": "ready", "database": True}


def test_readiness_probe_db_unhealthy(client_and_mod):
    mod = client_and_mod
    with TestClient(mod.app) as client:
        mod.app_state.db_healthy = False
        response = client.get("/readyz")
        assert response.status_code == 503, response.text
        assert response.json() == {"detail": "Database connection is unhealthy"}


def test_readiness_probe_startup_not_ready(client_and_mod):
    mod = client_and_mod
    mod.app_state.is_ready = False
    # Use client without entering lifespan context manager
    client = TestClient(mod.app)
    response = client.get("/readyz")
    assert response.status_code == 503, response.text
    assert response.json() == {"detail": "Application is still starting up"}


def test_openapi_schema(client_and_mod):
    mod = client_and_mod
    with TestClient(mod.app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
        schema = response.json()
        assert "/livez" in schema["paths"]
        assert "/readyz" in schema["paths"]
        assert "503" in schema["paths"]["/readyz"]["get"]["responses"]
