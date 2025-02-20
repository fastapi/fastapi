from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing_extensions import Annotated

from .utils import needs_py312

pytestmark = needs_py312

app = FastAPI()


async def get_foo1() -> str:
    return "foo1"


async def get_foo2() -> str:
    return "foo2"


async def get_foo3(x: str = "x") -> str:
    return f"foo3_{x}"


async def get_foo4(y: str = "y") -> str:
    return f"foo4_{y}"


Foo1 = Annotated[str, Depends(get_foo1)]
type Foo2 = Annotated[str, Depends(get_foo2)]
Foo3 = Annotated[str, Depends(get_foo3)]
type Foo4 = Annotated[str, Depends(get_foo4)]


@app.get("/")
async def root(foo1: Foo1, foo2: Foo2, foo3: Foo3, foo4: Foo4):
    return {"foo1": foo1, "foo2": foo2, "foo3": foo3, "foo4": foo4}


client = TestClient(app)


def test_type_alias_depends():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "foo1": "foo1",
        "foo2": "foo2",
        "foo3": "foo3_x",
        "foo4": "foo4_y",
    }
