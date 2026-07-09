from typing import List, Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


class SubModel(BaseModel):
    name: str
    value: int = 42


class MainModel(BaseModel):
    id: int
    title: str
    sub: SubModel
    items: List[SubModel]
    maybe: Optional[str] = None
    _sa_instance_state: str = "should-be-removed"


def test_basemodel_serialization_correctness():
    sub = SubModel(name="test")
    model = MainModel(
        id=1,
        title="hello",
        sub=sub,
        items=[sub, SubModel(name="another", value=10)],
    )

    # 1. Standard serialization
    encoded = jsonable_encoder(model)
    assert encoded == {
        "id": 1,
        "title": "hello",
        "sub": {"name": "test", "value": 42},
        "items": [
            {"name": "test", "value": 42},
            {"name": "another", "value": 10},
        ],
        "maybe": None,
    }

    # 2. Exclude none
    encoded_exclude_none = jsonable_encoder(model, exclude_none=True)
    assert "maybe" not in encoded_exclude_none

    # 3. Include and Exclude parameter filtering
    encoded_filtered = jsonable_encoder(model, include={"id", "title"})
    assert encoded_filtered == {"id": 1, "title": "hello"}

    encoded_excluded = jsonable_encoder(model, exclude={"sub", "items"})
    assert "sub" not in encoded_excluded
    assert "items" not in encoded_excluded
