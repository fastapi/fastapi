from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Optional[list[str]] = Header(None)):
    return {"X-Token values": x_token}
