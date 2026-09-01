from typing import Annotated, Sequence

from fastapi import Depends, FastAPI, Form, Query
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


def test_pep695_type_alias_query_and_form_sequence():
    app = FastAPI()

    SequenceAlias = TypeAliasType("SequenceAlias", Sequence[int])
    FormAlias = TypeAliasType("FormAlias", list[int])

    @app.get("/query")
    async def get_with_query(values: SequenceAlias = Query(...)) -> list[int]:
        return values

    @app.post("/form")
    async def post_with_form(values: FormAlias = Form(...)) -> list[int]:
        return values

    client = TestClient(app)

    response = client.get("/query", params={"values": ["1", "2", "3"]})
    assert response.status_code == 200
    assert response.json() == [1, 2, 3]

    response = client.post("/form", data={"values": ["1", "2", "3"]})
    assert response.status_code == 200
    assert response.json() == [1, 2, 3]
