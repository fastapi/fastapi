from typing import Optional, Union

from fastapi import FastAPI, Query
from pydantic import BeforeValidator
from typing_extensions import Annotated

app = FastAPI()


def nullable_str(val: str) -> Union[str, None]:
    if val in ("None", "", "null"):
        return None
    return val


@app.get("/items/")
async def read_items(
    q: Annotated[Optional[str], Query(min_length=3), BeforeValidator(nullable_str)],
):
    return {"q": q}
