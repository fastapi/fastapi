from fastapi import FastAPI
from fastapi.testclient import TestClient

FAVICON_URL = "https://www.google.com/favicon.ico"
app = FastAPI(favicon_url=FAVICON_URL)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui_loads_custom_logo():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    print(response.text)
    assert FAVICON_URL in response.text


def test_redoc_ui_loads_custom_logo():
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    print(response.text)
    assert FAVICON_URL in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
