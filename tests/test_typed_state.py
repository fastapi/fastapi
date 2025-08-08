from contextlib import asynccontextmanager
from typing import TypedDict

import pytest
from fastapi import Depends, FastAPI, TypedState
from fastapi.testclient import TestClient


class MyState(TypedDict):
    param_1: str
    param_2: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    state = MyState(param_1="example", param_2=42)
    yield state


app = FastAPI(lifespan=lifespan)


@app.get("/read")
async def read_state(state: TypedState[MyState]):
    return {"param_1": state._state["param_1"], "param_2": state._state["param_2"]}


async def update_state(state: TypedState[MyState]):
    state._state["param_1"] = "Updated"


@app.get("/updated-state", dependencies=[Depends(update_state)])
async def read_updated_state(state: TypedState[MyState]):
    return {"param_1": state._state["param_1"], "param_2": state._state["param_2"]}


@app.get("/read-attribute-access")
async def read_attribute(state: TypedState[MyState]):
    # This way it's not typed, but attribute access works
    return {
        "param_1": state.param_1,
        "param_2": state.param_2,
    }


async def update_state_attribute_access(state: TypedState[MyState]):
    state.param_1 = "Updated"  # This way it's not typed, but attribute access works


@app.get(
    "/updated-state-attribute-access",
    dependencies=[Depends(update_state_attribute_access)],
)
async def read_updated_attribute(state: TypedState[MyState]):
    # This way it's not typed, but attribute access works
    return {
        "param_1": state.param_1,
        "param_2": state.param_2,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/read",
        "/read-attribute-access",
    ],
)
def test_read(path: str):
    with TestClient(app) as client:
        response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"param_1": "example", "param_2": 42}


@pytest.mark.parametrize(
    "path",
    [
        "/updated-state",
        "/updated-state-attribute-access",
    ],
)
def test_read_updated_state_state(path: str):
    with TestClient(app) as client:
        response = client.get("/updated-state")
    assert response.status_code == 200
    assert response.json() == {"param_1": "Updated", "param_2": 42}


def test_openapi_schema():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema == {
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/read": {
                "get": {
                    "operationId": "read_state_read_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Read State",
                },
            },
            "/read-attribute-access": {
                "get": {
                    "operationId": "read_attribute_read_attribute_access_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Read Attribute",
                },
            },
            "/updated-state": {
                "get": {
                    "operationId": "read_updated_state_updated_state_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Read Updated State",
                },
            },
            "/updated-state-attribute-access": {
                "get": {
                    "operationId": "read_updated_attribute_updated_state_attribute_access_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Read Updated Attribute",
                },
            },
        },
    }
