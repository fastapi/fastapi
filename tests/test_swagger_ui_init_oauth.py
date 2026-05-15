from fastapi import FastAPI
from fastapi.testclient import TestClient

swagger_ui_init_oauth = {"clientId": "the-foo-clients", "appName": "The Predendapp"}

app = FastAPI(swagger_ui_init_oauth=swagger_ui_init_oauth)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    print(response.text)
    assert "ui.initOAuth" in response.text
    assert '"appName": "The Predendapp"' in response.text
    assert '"clientId": "the-foo-clients"' in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
