from typing import Union

from fastapi import FastAPI, Header
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(
    strange_header: Annotated[
        Union[str, None], Header(convert_underscores=False)
    ] = None
):
    return {"strange_header": strange_header}
