from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

if TYPE_CHECKING:
    from pydantic import BaseModel  # pragma: no cover

app = FastAPI()


@app.get("/")
def read_root(item: BaseModel) -> dict: ...
