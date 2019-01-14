from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["items"])
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}", tags=["items"])
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}
