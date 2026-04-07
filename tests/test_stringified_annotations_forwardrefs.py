from __future__ import annotations

from fastapi.testclient import TestClient

from .utils import needs_py310


def _build_app(source: str):
    namespace: dict[str, object] = {}
    exec(source, namespace, namespace)
    return namespace["app"]


@needs_py310
def test_late_defined_annotated_dependency_forwardref_is_not_treated_as_query_param():
    app = _build_app("""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

def get_potato() -> Potato:
    return Potato(color="red", size=10)

@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}

@dataclass
class Potato:
    color: str
    size: int
""")
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"color": "red", "size": 10}

    operation = client.get("/openapi.json").json()["paths"]["/"]["get"]
    assert "parameters" not in operation


@needs_py310
def test_stringified_annotated_dependency_with_defined_type_remains_a_dependency():
    app = _build_app("""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

@dataclass
class Potato:
    color: str
    size: int

def get_potato() -> Potato:
    return Potato(color="gold", size=7)

@app.get("/")
async def read_root(potato: Annotated["Potato", Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}
""")
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"color": "gold", "size": 7}

    operation = client.get("/openapi.json").json()["paths"]["/"]["get"]
    assert "parameters" not in operation


@needs_py310
def test_nested_forwardref_inside_annotated_dependency_preserves_structure():
    app = _build_app("""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

def get_potatoes() -> list[Potato]:
    return [Potato(color="red", size=10), Potato(color="gold", size=7)]

@app.get("/")
async def read_root(potatoes: Annotated[list[Potato], Depends(get_potatoes)]):
    return {
        "items": [{"color": potato.color, "size": potato.size} for potato in potatoes]
    }

@dataclass
class Potato:
    color: str
    size: int
""")
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "items": [
            {"color": "red", "size": 10},
            {"color": "gold", "size": 7},
        ]
    }

    operation = client.get("/openapi.json").json()["paths"]["/"]["get"]
    assert "parameters" not in operation
