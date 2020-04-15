from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "case1": {
                "summary": "valid test case",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "case2": {
                "summary": "valid test case with type coersion",
                "value": {
                    "name": "Bar",
                    "description": "Another very nice Item",
                    "price": "35.4",
                    "tax": 3.2,
                },
            },
            "case3": {
                "summary": "invalid test case with wrong type",
                "value": {
                    "name": "Baz",
                    "description": "One more very nice Item",
                    "price": "thirty five point four",
                    "tax": 3.2,
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
