from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": "false"})


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert "syntaxHighlight: false," in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
