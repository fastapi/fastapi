from typing import Annotated
from fastapi import FastAPI, Security

app = FastAPI(depends_default_parallelizable=True)

async def get_api_key() -> str:
    return "secret"

@app.get("/secure")
async def secure(
    k1: Annotated[str, Security(get_api_key, scopes=["a"], parallelizable=True)],
    k2: Annotated[str, Security(get_api_key, scopes=["b"], parallelizable=True)],
):
    return {"ok": True, "k1": k1, "k2": k2}
