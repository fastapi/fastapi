from typing import Annotated, Literal

from fastapi import Body, Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import TypeAliasType


async def some_value() -> int:
    return 123


DependedValue = TypeAliasType(
    "DependedValue", Annotated[int, Depends(some_value)], type_params=()
)


def test_pep695_type_dependencies():
    app = FastAPI()

    @app.get("/")
    async def get_with_dep(value: DependedValue) -> str:  # noqa
        return f"value: {value}"

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"value: 123"'


def test_pep695_type_alias_body_keeps_named_ref():
    """A bare PEP 695 ``TypeAliasType`` used as a body parameter should generate
    the same named OpenAPI component (``$ref``) as the equivalent
    ``Annotated[Alias, Body()]`` form.

    Regression test for https://github.com/fastapi/fastapi/issues/15855
    """
    app = FastAPI()

    class Cat(BaseModel):
        pet_type: Literal["cat"]
        meows: int

    class Dog(BaseModel):
        pet_type: Literal["dog"]
        barks: float

    Pet = TypeAliasType(
        "Pet",
        Annotated[Cat | Dog, Field(discriminator="pet_type")],
        type_params=(),
    )

    @app.post("/bare")
    def bare(pet: Pet):
        return pet

    @app.post("/body")
    def body(pet: Annotated[Pet, Body()]):
        return pet

    client = TestClient(app)
    schema = client.get("/openapi.json").json()

    def request_body_schema(path: str):
        return schema["paths"][path]["post"]["requestBody"]["content"][
            "application/json"
        ]["schema"]

    expected_ref = {"$ref": "#/components/schemas/Pet"}
    # The explicit Annotated[..., Body()] form already keeps the named ref today.
    assert request_body_schema("/body") == expected_ref
    # The bare alias form must produce the same named ref (was inlined before the fix).
    assert request_body_schema("/bare") == expected_ref
    assert "Pet" in schema["components"]["schemas"]

    # The discriminated union still validates and serializes correctly.
    response = client.post("/bare", json={"pet_type": "cat", "meows": 3})
    assert response.status_code == 200, response.text
    assert response.json() == {"pet_type": "cat", "meows": 3}

    response = client.post("/bare", json={"pet_type": "dog", "barks": 1.5})
    assert response.status_code == 200, response.text
    assert response.json() == {"pet_type": "dog", "barks": 1.5}

    response = client.post("/bare", json={"pet_type": "lizard"})
    assert response.status_code == 422, response.text

    # The explicit Annotated[..., Body()] form behaves identically.
    response = client.post("/body", json={"pet_type": "dog", "barks": 1.5})
    assert response.status_code == 200, response.text
    assert response.json() == {"pet_type": "dog", "barks": 1.5}
