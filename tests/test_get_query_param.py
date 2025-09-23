import pytest
from starlette.requests import Request
from fastapi.routing import get_query_param
from starlette.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/demo")
async def demo(request: Request):
    value = get_query_param(request, "name", default="guest")
    return {"name": value}

client = TestClient(app)


def test_existing_query_param():
    response = client.get("/demo?name=josh")
    assert response.json() == {"name": "josh"}


def test_missing_query_param_returns_default():
    response = client.get("/demo")
    assert response.json() == {"name": "guest"}
