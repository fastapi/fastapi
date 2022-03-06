from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.testclient import TestClient

swagger_ui_oauth2_redirect_url = "/docs/redirect"

app = FastAPI()
sub_app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    )

@sub_app.get("/items/")
async def read_items():
    return {"id": "foo"}

@sub_app.get("/openapi.json")
async def openapi():
    return get_openapi(
        title="Custom OpenAPI",
        version="0.1",
        routes=sub_app.routes,
        prefix="/sub_app",
    )

app.mount("/sub_app", sub_app)


client = TestClient(app)


def test_sub_app_open_api():
    response = client.get("/sub_app/openapi.json")
    assert response.status_code == 200, response.json()
    assert response.headers["content-type"] == "application/json"
    paths = list(response.json()["paths"].keys())
    assert paths == [
            "/sub_app/items/", "/sub_app/openapi.json",]
