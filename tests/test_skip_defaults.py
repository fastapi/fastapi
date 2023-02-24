from typing import Dict, Optional

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class SubModel(BaseModel):
    a: Optional[str] = "foo"


class Model(BaseModel):
    x: Optional[int]
    sub: SubModel


class ModelSubclass(Model):
    y: int
    z: int = 0
    w: Optional[int] = None


class ModelDefaults(BaseModel):
    w: Optional[str] = None
    x: Optional[str] = None
    y: str = "y"
    z: str = "z"


@app.get("/", response_model=Model, response_model_exclude_unset=True)
def get_root() -> ModelSubclass:
    return ModelSubclass(sub={}, y=1, z=0)


@app.get(
    "/exclude_unset", response_model=ModelDefaults, response_model_exclude_unset=True
)
def get_exclude_unset() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


@app.get(
    "/exclude_defaults",
    response_model=ModelDefaults,
    response_model_exclude_defaults=True,
)
def get_exclude_defaults() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


@app.get(
    "/exclude_none", response_model=ModelDefaults, response_model_exclude_none=True
)
def get_exclude_none() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


@app.get(
    "/exclude_unset_none",
    response_model=ModelDefaults,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
def get_exclude_unset_none() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


client = TestClient(app)


def test_return_defaults():
    response = client.get("/")
    assert response.json() == {"sub": {}}


def test_return_exclude_unset():
    response = client.get("/exclude_unset")
    assert response.json() == {"x": None, "y": "y"}


def test_return_exclude_defaults():
    response = client.get("/exclude_defaults")
    assert response.json() == {}


def test_return_exclude_none():
    response = client.get("/exclude_none")
    assert response.json() == {"y": "y", "z": "z"}


def test_return_exclude_unset_none():
    response = client.get("/exclude_unset_none")
    assert response.json() == {"y": "y"}


@pytest.mark.parametrize(
    "exclude_defaults,exclude_none,exclude_unset,expected",
    [
        (True, False, False, {}),
        (False, True, False, {"y": "y", "z": "z"}),
        (False, False, True, {"x": None, "y": "y"}),
    ],
)
def test_top_level_defaults(
    exclude_defaults: bool,
    exclude_none: bool,
    exclude_unset: bool,
    expected: Dict[str, str],
):
    app = FastAPI(
        default_response_model_exclude_defaults=exclude_defaults,
        default_response_model_exclude_none=exclude_none,
        default_response_model_exclude_unset=exclude_unset,
    )

    @app.get("/")
    def get() -> ModelDefaults:
        return ModelDefaults(x=None, y="y")

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == expected


@pytest.mark.parametrize(
    "exclude_defaults,exclude_none,exclude_unset,expected",
    [
        (True, False, False, {}),
        (False, True, False, {"y": "y", "z": "z"}),
        (False, False, True, {"x": None, "y": "y"}),
    ],
)
def test_router_overrides_default_app(
    exclude_defaults: bool,
    exclude_none: bool,
    exclude_unset: bool,
    expected: Dict[str, str],
):
    app = FastAPI(
        default_response_model_exclude_defaults=not exclude_defaults,
        default_response_model_exclude_none=not exclude_none,
        default_response_model_exclude_unset=not exclude_unset,
    )
    router = APIRouter(
        default_response_model_exclude_defaults=exclude_defaults,
        default_response_model_exclude_none=exclude_none,
        default_response_model_exclude_unset=exclude_unset,
    )

    @router.get("/")
    def get() -> ModelDefaults:
        return ModelDefaults(x=None, y="y")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == expected


@pytest.mark.parametrize(
    "exclude_defaults,exclude_none,exclude_unset,expected",
    [
        (True, False, False, {}),
        (False, True, False, {"y": "y", "z": "z"}),
        (False, False, True, {"x": None, "y": "y"}),
    ],
)
def test_route_overrides_default_router(
    exclude_defaults: bool,
    exclude_none: bool,
    exclude_unset: bool,
    expected: Dict[str, str],
):
    app = FastAPI()
    router = APIRouter(
        default_response_model_exclude_defaults=not exclude_defaults,
        default_response_model_exclude_none=not exclude_none,
        default_response_model_exclude_unset=not exclude_unset,
    )

    @router.get(
        "/",
        response_model_exclude_defaults=exclude_defaults,
        response_model_exclude_none=exclude_none,
        response_model_exclude_unset=exclude_unset,
    )
    def get() -> ModelDefaults:
        return ModelDefaults(x=None, y="y")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == expected
