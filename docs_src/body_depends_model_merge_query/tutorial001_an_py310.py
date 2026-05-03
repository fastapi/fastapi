from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Query
from pydantic import BaseModel

app = FastAPI()
catalog_router = APIRouter()


class ProductFiltersBase(BaseModel):
    category: str | None = None


class ProductFiltersFull(ProductFiltersBase):
    in_stock: bool = True


class ProductFiltersPaginated(ProductFiltersBase):
    page: int = 1
    per_page: int = 10


def register_product_list(
    router: APIRouter,
    path: str,
    schema: type[ProductFiltersBase],
):
    @router.get(path)
    def list_products(
        params: Annotated[
            ProductFiltersBase,
            Query(),  # optional
            Depends(schema),
        ],
    ):
        return params

    return list_products


register_product_list(
    catalog_router,
    "/items/",
    ProductFiltersFull,
)
register_product_list(
    catalog_router,
    "/items-paginated/",
    ProductFiltersPaginated,
)
register_product_list(
    catalog_router,
    "/basics/",
    ProductFiltersBase,
)
app.include_router(
    catalog_router,
    prefix="/catalog",
)
