from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class ClientHeaders(BaseModel):
    x_client_name: str
    x_client_version: str


@app.get("/items/")
async def read_items(client: ClientHeaders | None = Header(default=None)):
    return client
