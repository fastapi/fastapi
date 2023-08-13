from typing import Annotated, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[Optional[str], Header()] = None):
    return {"User-Agent": user_agent}
