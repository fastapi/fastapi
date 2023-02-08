import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(servers=[{"url": "localhost:8000"}])

main_api_text = {"message": "Hello World from main app"}
sub_api_text = {"message": "Hello World from sub API"}


@app.get("/app")
def read_main():
    return main_api_text


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return sub_api_text


app.mount("/subapi", subapi)

client = TestClient(app)


def test_app_response():
    response = client.get("/app")
    assert response.status_code == 200, response.text
    assert json.loads(response.text) == main_api_text


def test_sub_app_response():
    response = client.get("/subapi/sub")
    assert response.status_code == 200, response.text
    assert json.loads(response.text) == sub_api_text


def test_app_openapi_response():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text


def test_sub_app_openapi_response():
    response = client.get("/subapi/openapi.json")
    assert response.status_code == 200, response.text


def test_sub_app_openapi_servers():
    sub_servers = [{"url": "/subapi"}] + [
        {"url": server["url"] + "/subapi"} for server in app.servers
    ]
    assert sub_servers == subapi.servers
