from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


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

item_examples_list = [dct["value"] for dct in item_examples.values() if "value" in dct]
media_type_extra = {"examples": item_examples}


class Item(BaseModel):
    name: str = Field(examples=["Foo", "Bar"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2, None])

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Bar",
                "price": "35.4",
            },
            "examples": item_examples_list[:1],
        }
    }


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples=item_examples,
        media_type_extra=media_type_extra,
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
