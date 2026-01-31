from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
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
