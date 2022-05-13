from typing import List, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Optional[List[str]] = Header(default=None)):
    return {"X-Token values": x_token}
