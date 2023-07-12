from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


item_examples = {
    "Example Item": {
        "value": {
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        }
    },
    "Example Item; coerce string to float": {
        "value": {
            "name": "Bar",
            "price": "35.4",
        }
    },
    "Raise validation error for 'price'": {
        "value": {
            "name": "Baz",
            "price": "thirty five point four",
        }
    },
}


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples=[dct["value"] for dct in item_examples.values()],
        media_type_extra={"examples": item_examples},
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
