from typing import Annotated

import re

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[
        int | str,
        Query(union_mode="left_to_right"),
    ] = "default",
    tags: Annotated[
        list[str],
        Query(fail_fast=True),
    ] = ["default"],
    count: Annotated[
        int,
        Query(validate_default=True),
    ] = 1,
    label: Annotated[
        str,
        Query(
            pattern=re.compile("^abc$", re.IGNORECASE),
        ),
    ] = "ABC",
):
    return {
        "q": q,
        "tags": tags,
        "count": count,
        "label": label,
    }
