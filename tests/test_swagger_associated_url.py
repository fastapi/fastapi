from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(
    docs_url="/my_docs_url",
    redoc_url="/my_redoc_url",
    openapi_prefix="/prefix",
)

client = TestClient(app)


def test_docs_url():
    response = client.get("/my_docs_url")
    assert response.status_code == 200, response.text


def test_redoc_url():
    response = client.get("/my_redoc_url")
    assert response.status_code == 200, response.text


def test_openapi_prefix():
    response = client.get("/prefix/openapi.json")
    assert response.status_code == 200, response.text
