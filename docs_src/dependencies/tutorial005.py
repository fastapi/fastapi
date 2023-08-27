from enum import Enum, auto
from typing import Union

from fastapi import Cookie, Depends, EndPoint, FastAPI

app = FastAPI()


def query_extractor(q: Union[str, None] = None):
    return q


class EndPointEnum(Enum):
    READ_ITEMS = auto()


def query_or_cookie_extractor(
    endpoint: EndPointEnum = EndPoint(),
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    assert endpoint is EndPointEnum.READ_ITEMS  # for read_query endpoint!
    if not q:
        return last_query
    return q


@app.get("/items/", endpoint_enum=EndPointEnum.READ_ITEMS)
async def read_query(
    query_or_default: str = Depends(query_or_cookie_extractor),
    endpoint: EndPointEnum = EndPoint(),
):
    assert endpoint is EndPointEnum.READ_ITEMS  # for read_query endpoint!
    return {"q_or_cookie": query_or_default}
