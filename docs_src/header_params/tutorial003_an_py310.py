from typing import Annotated, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Annotated[Optional[list[str]], Header()] = None):
    return {"X-Token values": x_token}
