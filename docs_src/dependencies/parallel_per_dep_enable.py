from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI(depends_default_parallelizable=False)

async def dep_a() -> int:
    return 1

async def dep_b() -> int:
    return 2

@app.get("/items")
async def read_items(
    a: Annotated[int, Depends(dep_a, parallelizable=True)],
    b: Annotated[int, Depends(dep_b, parallelizable=True)],
):
    return {"a": a, "b": b}
