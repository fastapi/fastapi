from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class User(BaseModel):
    name: str


class UserLogin(User):
    password: str


class OuterModel(BaseModel):
    user: User


class Item(BaseModel):
    name: str
    description: str


class ItemWithPrice(Item):
    price: float


requires_pydantic_v2_13 = pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 13),
    reason="polymorphic_serialization requires Pydantic >= 2.13",
)

only_for_pydantic_below_v2_13 = pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE >= (2, 13),
    reason="This test only applies to Pydantic < 2.13",
)
requires_pydantic_v2_13 = pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 13),
    reason="polymorphic_serialization requires Pydantic >= 2.13",
)

only_for_pydantic_below_v2_13 = pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE >= (2, 13),
    reason="This test only applies to Pydantic < 2.13",
)


def test_default_behavior_filters_subclass_fields():
    app = FastAPI()

    @app.get("/user", response_model=OuterModel)
    def get_user():
        return OuterModel(user=UserLogin(name="pydantic", password="password"))

    response = TestClient(app).get("/user")

    assert response.status_code == 200
    assert response.json() == {"user": {"name": "pydantic"}}


@requires_pydantic_v2_13
def test_polymorphic_flag_includes_subclass_fields():
    app = FastAPI()

    @app.get(
        "/user",
        response_model=OuterModel,
        response_model_polymorphic_serialization=True,
    )
    def get_user():
        return OuterModel(user=UserLogin(name="pydantic", password="password"))

    response = TestClient(app).get("/user")

    assert response.status_code == 200
    assert response.json() == {"user": {"name": "pydantic", "password": "password"}}


@requires_pydantic_v2_13
def test_polymorphic_with_inferred_response_model():
    app = FastAPI()

    @app.get("/user", response_model_polymorphic_serialization=True)
    def get_user() -> OuterModel:
        return OuterModel(user=UserLogin(name="pydantic", password="password"))

    response = TestClient(app).get("/user")

    assert response.status_code == 200
    assert response.json() == {"user": {"name": "pydantic", "password": "password"}}


@requires_pydantic_v2_13
def test_polymorphic_with_fast_json_path():
    app = FastAPI()

    @app.post(
        "/item",
        response_model=Item,
        response_model_polymorphic_serialization=True,
        status_code=201,
    )
    def create_item() -> Item:
        return ItemWithPrice(name="Widget", description="A useful widget", price=9.99)

    response = TestClient(app).post("/item")

    assert response.status_code == 201
    assert response.json() == {
        "name": "Widget",
        "description": "A useful widget",
        "price": 9.99,
    }


@requires_pydantic_v2_13
def test_polymorphic_with_custom_response_class():
    app = FastAPI()

    class CustomJSONResponse(JSONResponse):
        media_type = "application/json"

    @app.get(
        "/user",
        response_model=OuterModel,
        response_model_polymorphic_serialization=True,
        response_class=CustomJSONResponse,
    )
    def get_user():
        return OuterModel(user=UserLogin(name="pydantic", password="password"))

    response = TestClient(app).get("/user")

    assert response.status_code == 200
    assert response.json() == {"user": {"name": "pydantic", "password": "password"}}


@requires_pydantic_v2_13
def test_polymorphic_composes_with_exclude():
    app = FastAPI()

    @app.get(
        "/user",
        response_model=OuterModel,
        response_model_polymorphic_serialization=True,
        response_model_exclude={"user": {"password"}},
    )
    def get_user():
        return OuterModel(user=UserLogin(name="pydantic", password="password"))

    response = TestClient(app).get("/user")

    assert response.status_code == 200
    assert response.json() == {"user": {"name": "pydantic"}}


def test_list_response_filters_subclass_fields_by_default():
    app = FastAPI()

    def generate_items() -> Iterator[Item]:
        yield ItemWithPrice(name="Item1", description="First item", price=10.0)

    @app.get("/items/stream", response_model=list[Item])
    def stream_items():
        return list(generate_items())

    response = TestClient(app).get("/items/stream")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0] == {"name": "Item1", "description": "First item"}


@only_for_pydantic_below_v2_13
def test_raises_error_for_unsupported_pydantic_version():
    app = FastAPI()

    @app.get(
        "/user",
        response_model=OuterModel,
        response_model_polymorphic_serialization=True,
    )
    def get_user():
        return OuterModel(user=UserLogin(name="pydantic", password="password"))

    with pytest.raises(ValueError) as exc_info:
        TestClient(app).get("/user")

    assert "polymorphic_serialization requires Pydantic >= 2.13" in str(exc_info.value)


def test_flag_defaults_to_false():
    app = FastAPI()

    @app.get("/user1", response_model=OuterModel)
    def get_user1():
        return OuterModel(user=UserLogin(name="user1", password="pass1"))

    @app.post("/user2", response_model=OuterModel)
    def post_user2():
        return OuterModel(user=UserLogin(name="user2", password="pass2"))

    client = TestClient(app)

    response1 = client.get("/user1")
    assert response1.json() == {"user": {"name": "user1"}}

    response2 = client.post("/user2")
    assert response2.json() == {"user": {"name": "user2"}}
