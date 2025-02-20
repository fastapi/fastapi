from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing_extensions import Annotated, TypeAliasType


async def get_foo1() -> str:
    return "foo1"


async def get_foo2(x: str = "x") -> str:
    return f"foo2_{x}"


Foo1 = Annotated[str, Depends(get_foo1)]
Foo2 = Annotated[str, Depends(get_foo2)]


async def get_bar1() -> str:
    return "bar1"


async def get_bar2(y: str = "y") -> str:
    return f"bar2_{y}"


# Equivalent to:
# type Bar1 = Annotated[str, Depends(get_bar1)]
# type Bar2 = Annotated[str, Depends(get_bar2)]
Bar1 = TypeAliasType("Bar1", Annotated[str, Depends(get_bar1)])
Bar2 = TypeAliasType("Bar2", Annotated[str, Depends(get_bar2)])


def test_type_alias_depends():
    app = FastAPI()

    @app.get("/")
    async def root(foo1: Foo1, foo2: Foo2, bar1: Bar1, bar2: Bar2):
        return {"foo1": foo1, "foo2": foo2, "bar1": bar1, "bar2": bar2}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "foo1": "foo1",
        "foo2": "foo2_x",
        "bar1": "bar1",
        "bar2": "bar2_y",
    }
