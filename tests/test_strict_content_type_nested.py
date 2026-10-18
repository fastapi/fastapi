from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

# Lax app with nested routers, inner overrides to strict

app_nested = FastAPI(strict_content_type=False)  # lax app
outer_router = APIRouter(prefix="/outer")  # inherits lax from app
inner_strict = APIRouter(prefix="/strict", strict_content_type=True)
inner_default = APIRouter(prefix="/default")


@inner_strict.post("/items/")
async def inner_strict_post(data: dict):
    return data


@inner_default.post("/items/")
async def inner_default_post(data: dict):
    return data


outer_router.include_router(inner_strict)
outer_router.include_router(inner_default)
app_nested.include_router(outer_router)

client_nested = TestClient(app_nested)


def test_strict_inner_on_lax_app_rejects_no_content_type():
    response = client_nested.post("/outer/strict/items/", content='{"key": "value"}')
    assert response.status_code == 422


def test_default_inner_inherits_lax_from_app():
    response = client_nested.post("/outer/default/items/", content='{"key": "value"}')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


def test_strict_inner_accepts_json_content_type():
    response = client_nested.post("/outer/strict/items/", json={"key": "value"})
    assert response.status_code == 200


def test_default_inner_accepts_json_content_type():
    response = client_nested.post("/outer/default/items/", json={"key": "value"})
    assert response.status_code == 200


# Strict app -> lax outer router -> strict inner router

app_mixed = FastAPI(strict_content_type=True)
mixed_outer = APIRouter(prefix="/outer", strict_content_type=False)
mixed_inner = APIRouter(prefix="/inner", strict_content_type=True)


@mixed_outer.post("/items/")
async def mixed_outer_post(data: dict):
    return data


@mixed_inner.post("/items/")
async def mixed_inner_post(data: dict):
    return data


mixed_outer.include_router(mixed_inner)
app_mixed.include_router(mixed_outer)

client_mixed = TestClient(app_mixed)


def test_lax_outer_on_strict_app_accepts_no_content_type():
    response = client_mixed.post("/outer/items/", content='{"key": "value"}')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


def test_strict_inner_on_lax_outer_rejects_no_content_type():
    response = client_mixed.post("/outer/inner/items/", content='{"key": "value"}')
    assert response.status_code == 422


def test_lax_outer_accepts_json_content_type():
    response = client_mixed.post("/outer/items/", json={"key": "value"})
    assert response.status_code == 200


def test_strict_inner_on_lax_outer_accepts_json_content_type():
    response = client_mixed.post("/outer/inner/items/", json={"key": "value"})
    assert response.status_code == 200
