from typing import Annotated, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    strange_header: Annotated[Optional[str], Header(convert_underscores=False)] = None
):
    return {"strange_header": strange_header}
