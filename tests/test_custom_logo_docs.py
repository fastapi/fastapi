from fastapi import FastAPI
from fastapi.testclient import TestClient

FAVICON_URL = "data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22"
"http%3A//www.w3.org/2000/svg%22%20width%3D%2232%22%20height%3D%2232%"
"22%20viewBox%3D%220%200%2032%2032%22%3E%3Ccircle%20cx%3D%2216%22%20c"
"y%3D%2216%22%20r%3D%2214%22%20fill%3D%22%23009688%22/%3E%3Ctext%20x%"
"3D%2250%25%22%20y%3D%2255%25%22%20font-size%3D%2216%22%20font-family"
"%3D%22Arial%2C%20sans-serif%22%20fill%3D%22white%22%20text-anchor%3D"
"%22middle%22%20dominant-baseline%3D%22middle%22%3EF%3C/text%3E%3C/svg%3E"
app = FastAPI(favicon_url=FAVICON_URL)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui_loads_custom_logo():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert FAVICON_URL in response.text


def test_redoc_ui_loads_custom_logo():
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    assert FAVICON_URL in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
