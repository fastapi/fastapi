from typing import List, Union

from fastapi import FastAPI, Header
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Annotated[Union[List[str], None], Header()] = None):
    return {"X-Token values": x_token}
