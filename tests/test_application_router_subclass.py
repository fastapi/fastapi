import pytest
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.testclient import TestClient


class SubclassedRouter(APIRouter):
    def add_api_route(self, path, endpoint, *args, methods=None, **kwargs):
        if methods and "GET" in methods:
            super().add_api_route(path, endpoint, *args, methods=["HEAD"], **kwargs)
        super().add_api_route(path, endpoint, *args, methods=methods, **kwargs)


vanilla_app = FastAPI()


@vanilla_app.get("/")
def vanilla_root():
    return {"welcome": "Welcome to vanilla FastAPI!"}


vanilla_client = TestClient(vanilla_app)

customized_app = FastAPI(router_class=SubclassedRouter)


@customized_app.get("/")
def customized_root():
    return {"welcome": "Welcome to customized FastAPI!"}


customized_client = TestClient(customized_app)


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [("/", 200, {"welcome": "Welcome to vanilla FastAPI!"})],
)
def test_vanilla_router_get(path, expected_status, expected_response):
    response = vanilla_client.get(path)
    assert response.status_code == expected_status
    assert response.json() == {"welcome": "Welcome to vanilla FastAPI!"}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [("/", 405, None)],
)
def test_vanilla_router_head(path, expected_status, expected_response):
    response = vanilla_client.head(path)
    assert response.status_code == expected_status
    assert not response.content


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [("/", 200, {"welcome": "Welcome to customized FastAPI!"})],
)
def test_customized_router_get(path, expected_status, expected_response):
    response = customized_client.get(path)
    assert response.status_code == expected_status
    assert response.json() == {"welcome": "Welcome to customized FastAPI!"}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [("/", 200, None)],
)
def test_customized_router_head(path, expected_status, expected_response):
    response = customized_client.head(path)
    assert response.status_code == expected_status
    assert not response.content
