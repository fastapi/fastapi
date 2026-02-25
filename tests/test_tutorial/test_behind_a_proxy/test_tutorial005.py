import pytest
from fastapi.testclient import TestClient

from docs_src.behind_a_proxy.tutorial005_py310 import app

client = TestClient(app)


@pytest.mark.parametrize(
    "root_path, requested_path, expected_root_path",
    [
        ("/api/v1", "/api/v1/app", "/api/v1"),
        ("/backend/v1", "/backend/v1/app", "/backend/v1"),
        ("/backend/v1/", "/backend/v1/app", "/backend/v1"),
        (None, "/app", ""),
    ],
)
def test_forwarded_prefix_middleware(
    root_path: str,
    requested_path: str,
    expected_root_path: str,
):
    client = TestClient(app)
    headers = {}
    if root_path:
        headers["x-forwarded-prefix"] = root_path
    response = client.get(requested_path, headers=headers)
    assert response.status_code == 200
    assert response.json()["path"] == requested_path
    assert response.json()["root_path"] == expected_root_path


@pytest.mark.parametrize(
    "prefix",
    [
        "/api/v1",
        "/backend/v1",
    ],
)
def test_openapi_servers(prefix: str):
    client = TestClient(app)
    headers = {"x-forwarded-prefix": f"{prefix}"}
    response = client.get(f"{prefix}/openapi.json", headers=headers)
    assert response.status_code == 200
    openapi_data = response.json()
    assert "servers" in openapi_data
    assert openapi_data["servers"] == [{"url": prefix}]


@pytest.mark.parametrize(
    "root_path, requested_path, expected_openapi_url",
    [
        ("/api/v1", "/api/v1/docs", "/api/v1/openapi.json"),
        (None, "/docs", "/openapi.json"),
    ],
)
def test_swagger_docs_openapi_url(
    root_path: str, requested_path: str, expected_openapi_url: str
):
    client = TestClient(app)
    headers = {}
    if root_path:
        headers["x-forwarded-prefix"] = root_path
    response = client.get(requested_path, headers=headers)
    assert response.status_code == 200
    assert expected_openapi_url in response.text
