from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()
items_router = APIRouter()


class ItemBase(BaseModel):
    name: str


class Gadget(ItemBase):
    description: str


class Part(ItemBase):
    sku: str


def register_post_route(
    router: APIRouter,
    path: str,
    schema: type[ItemBase],
):
    @router.post(path)
    def create_entity(
        entity: Annotated[
            ItemBase,
            Body(),
            Depends(schema),
        ],
    ):
        return entity

    return create_entity


register_post_route(
    items_router,
    "/objects/gadgets/",
    Gadget,
)
register_post_route(
    items_router,
    "/objects/parts/",
    Part,
)
app.include_router(
    items_router,
    prefix="/items",
)
