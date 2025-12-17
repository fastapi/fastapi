"""Test case for issue #13056: Can't use `Annotated` with `ForwardRef`"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color='red', size=10)


@app.get('/')
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {'color': potato.color, 'size': potato.size}


@dataclass
class Potato:
    color: str
    size: int


client = TestClient(app)


def test_annotated_forward_ref():
    """Test that forward references work correctly with Annotated dependencies."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert data == {'color': 'red', 'size': 10}


def test_openapi_schema():
    """Test that OpenAPI schema is generated correctly."""
    response = client.get('/openapi.json')
    assert response.status_code == 200
    schema = response.json()
    # The root path should NOT have query parameters for potato
    # It should only be a dependency
    root_path = schema['paths']['/']['get']
    # Check that potato is not a query parameter
    parameters = root_path.get('parameters', [])
    potato_params = [p for p in parameters if 'potato' in p.get('name', '').lower()]
    assert len(potato_params) == 0, f"Potato should not appear as a query parameter: {potato_params}"


if __name__ == "__main__":
    test_annotated_forward_ref()
    test_openapi_schema()
    print("All tests passed!")
