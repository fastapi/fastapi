from typing import List

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: List[str] = Header(None)):
    return {"X-Token values": x_token}
