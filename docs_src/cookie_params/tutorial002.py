from typing import Optional

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(
    hidden_cookie: Optional[str] = Cookie(None, include_in_schema=False)
):
    return {"hidden_cookie": hidden_cookie}
