import pytest
from fastapi import FastAPI
from fastapi.middleware.timing import TimingMiddleware
from fastapi.testclient import TestClient


@pytest.fixture
def app_with_default_middleware():
    app = FastAPI()
    app.add_middleware(TimingMiddleware)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: str | None = None):
        return {"item_id": item_id, "q": q}

    return app


@pytest.fixture
def app_with_custom_header():
    app = FastAPI()
    app.add_middleware(TimingMiddleware, header_name="X-Custom-Time")

    @app.get("/")
    async def root():
        return {"message": "Custom Header"}

    return app


def test_response_header_exists(app_with_default_middleware):
    client = TestClient(app_with_default_middleware)
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers


def test_response_header_value_is_positive(app_with_default_middleware):
    client = TestClient(app_with_default_middleware)
    response = client.get("/")
    assert response.status_code == 200
    process_time = float(response.headers["X-Process-Time"])
    assert process_time > 0


def test_custom_header_name(app_with_custom_header):
    client = TestClient(app_with_custom_header)
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Custom-Time" in response.headers
    assert "X-Process-Time" not in response.headers
    process_time = float(response.headers["X-Custom-Time"])
    assert process_time > 0


def test_middleware_does_not_affect_response_content(app_with_default_middleware):
    client = TestClient(app_with_default_middleware)
    response = client.get("/items/42?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "test"}
    assert "X-Process-Time" in response.headers


def test_multiple_requests_have_independent_timing(app_with_default_middleware):
    client = TestClient(app_with_default_middleware)
    response1 = client.get("/")
    response2 = client.get("/items/1")

    assert response1.status_code == 200
    assert response2.status_code == 200

    time1 = float(response1.headers["X-Process-Time"])
    time2 = float(response2.headers["X-Process-Time"])

    assert time1 > 0
    assert time2 > 0
