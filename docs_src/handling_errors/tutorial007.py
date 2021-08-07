import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: Optional[float] = None


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    logging.exception(
        "%s %s\nRequest:%s\nResponse:%s",
        request.method,
        request.url,
        exc.request_body,
        exc.response_body,
    )
    return PlainTextResponse(status_code=500)


@app.post("/items", response_model=Item)
async def read_item(item: Item):
    item.price = "something went wrong"
    return item
