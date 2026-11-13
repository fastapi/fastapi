from datetime import date

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class DateRange(BaseModel):
    start: date
    end: date


@app.get("/items/")
async def read_items(
    limit: int = 10,
    date_range: DateRange | None = Query(default=None),
):
    return {"limit": limit, "date_range": date_range}
