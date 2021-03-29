from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    hidden_header: Optional[str] = Header(None, include_in_schema=False)
):
    return {"hidden_header": hidden_header}
