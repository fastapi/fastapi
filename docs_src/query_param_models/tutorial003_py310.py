from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Pagination(BaseModel):
    limit: int = Field(10, ge=1)
    offset: int = Field(0, ge=0)


class Filters(BaseModel):
    tags: list[str] = []


@app.get("/items/")
def read_items(
    pagination: Pagination = Query(),
    filters: Filters = Query(),
    search: str | None = None,
):
    return {"pagination": pagination, "filters": filters, "search": search}
