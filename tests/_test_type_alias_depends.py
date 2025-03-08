from fastapi import Depends, FastAPI
from typing_extensions import Annotated


async def get_foo1() -> str:
    return "foo1"


async def get_foo2(x: str = "x") -> str:
    return f"foo2_{x}"


async def get_bar1() -> str:
    return "bar1"


async def get_bar2(y: str = "y") -> str:
    return f"bar2_{y}"


Foo1 = Annotated[str, Depends(get_foo1)]
Foo2 = Annotated[str, Depends(get_foo2)]
type Bar1 = Annotated[str, Depends(get_bar1)]
type Bar2 = Annotated[str, Depends(get_bar2)]

app = FastAPI()


@app.get("/")
async def root(foo1: Foo1, foo2: Foo2, bar1: Bar1, bar2: Bar2):
    return {"foo1": foo1, "foo2": foo2, "bar1": bar1, "bar2": bar2}
