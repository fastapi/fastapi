from fastapi import FastAPI
from starlette.testclient import TestClient

swagger_ui_app_name = "some_app_name"
app = FastAPI(swagger_ui_app_name=swagger_ui_app_name)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text
    print(client.base_url)
    assert "clientId" not in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
