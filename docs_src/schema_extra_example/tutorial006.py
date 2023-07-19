"""Creating examples that are useful in Swagger UI were removed in v0.100.0
for all parameter types.
I recommend trying this example app in both to see how it changes.
"""

from enum import Enum
from typing import Dict, Union

from fastapi import Body, FastAPI, Header, HTTPException, Path, Query, Request, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


ITEM_STORE = {}

item_examples = {
    "normal": {
        "summary": "A normal example",
        "description": "A **normal** item works correctly.",
        "value": {
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    },
    "converted": {
        "summary": "An example with converted data",
        "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
        "value": {
            "name": "Bar",
            "price": "35.4",
        },
    },
    "invalid": {
        "summary": "Invalid data is rejected with an error",
        "value": {
            "name": "Baz",
            "price": "thirty five point four",
        },
    },
}


class ErrorModel(BaseModel):
    detail: Union[str, Dict[str, str]]


class ErrorCode(str, Enum):
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    ANYTHING_BUT_GEOJSON = "ANYTHING_BUT_GEOJSON"
    BAD_HEADER = "BAD_HEADER"


@app.post(
    "/items/{item_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.UNSUPPORTED_FORMAT: {
                            "summary": "The format is not recognized.",
                            "value": {"detail": ErrorCode.UNSUPPORTED_FORMAT},
                        },
                        ErrorCode.ANYTHING_BUT_GEOJSON: {
                            "summary": (
                                "Amazingly, this format is supported on AGOL"
                                "but not on any desktop software made by ESRI."
                            ),
                            "value": {
                                "detail": {
                                    "code": ErrorCode.ANYTHING_BUT_GEOJSON,
                                    "reason": "Likely on purpose.",
                                }
                            },
                        },
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.BAD_HEADER: {
                            "summary": ("This header crashes the server. It's bad."),
                            "value": {
                                "detail": {
                                    "code": ErrorCode.BAD_HEADER,
                                    "reason": "Likely on purpose.",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def post_item(
    request: Request,
    *,
    item_id: int = Path(
        examples={
            "id as int": {"value": 5},
            "id as string": {"value": "5"},
            "invalid id": {"value": "anything else"},
        }
    ),
    item: Item = Body(examples=item_examples),
    f: Union[str, None] = Query(
        "wkt",
        examples={
            "text (default)": {"value": "wkt"},
            "response as json": {"value": "json"},
            "format 3": {"summary": "response as geojson", "value": "geojson"},
        },
    ),
    strange_header: str
    | None = Header(
        default=None,
        convert_underscores=False,
        examples={
            "good": {"value": "some long string"},
            "bad": {"summary": "this one's bad", "value": "bad header"},
        },
    ),
):
    if f == "geojson":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ANYTHING_BUT_GEOJSON,
                "reason": "None given, but you can keep asking for it if you really want.",
            },
        )
    elif f not in ("wkt", "json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": ErrorCode.UNSUPPORTED_FORMAT},
        )

    assert request.headers["strange_header"] == strange_header

    if strange_header == "bad header":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": ErrorCode.BAD_HEADER, "detail": "stop doing that."},
        )

    ITEM_STORE[item_id] = item

    assert [isinstance(id, int) for id in ITEM_STORE.keys()]

    return ITEM_STORE[item_id]
