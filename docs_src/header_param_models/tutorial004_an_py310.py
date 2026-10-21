from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class ClientHeaders(BaseModel):
    x_client_name: str
    x_client_version: str


@app.get("/items/")
async def read_items(client: Annotated[ClientHeaders | None, Header()] = None):
    return client
