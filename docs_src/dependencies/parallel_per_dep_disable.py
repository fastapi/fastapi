from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI(depends_default_parallelizable=True)

async def dep_seq() -> int:
    return 1

@app.get("/users")
async def read_users(
    x: Annotated[int, Depends(dep_seq, parallelizable=False)],
):
    return {"x": x}
