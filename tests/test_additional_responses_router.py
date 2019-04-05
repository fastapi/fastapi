from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient

app = FastAPI()
router = APIRouter()


@router.get("/a", responses={501: {"description": "Error 1"}})
async def a():
    return "a"


@router.get("/b", responses={502: {"description": "Error 2"}})
async def b():
    return "b"


@router.get("/c", responses={501: {"description": "Error 3"}})
async def c():
    return "c"


app.include_router(router)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/a": {
            "get": {
                "responses": {
                    "501": {"description": "Error 1"},
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                },
                "summary": "A Get",
                "operationId": "a_a_get",
            }
        },
        "/b": {
            "get": {
                "responses": {
                    "502": {"description": "Error 2"},
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                },
                "summary": "B Get",
                "operationId": "b_b_get",
            }
        },
        "/c": {
            "get": {
                "responses": {
                    "501": {"description": "Error 3"},
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                },
                "summary": "C Get",
                "operationId": "c_c_get",
            }
        },
    },
}

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_a():
    response = client.get("/a")
    assert response.status_code == 200
    assert response.json() == "a"


def test_b():
    response = client.get("/b")
    assert response.status_code == 200
    assert response.json() == "b"


def test_c():
    response = client.get("/c")
    assert response.status_code == 200
    assert response.json() == "c"
