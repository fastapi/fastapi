from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends, FastAPI

if TYPE_CHECKING:
    from pydantic import BaseModel  # pragma: no cover

app = FastAPI()


def get_thing(item: BaseModel) -> None: ...


@app.get("/")
def read_root(thing=Depends(get_thing)) -> dict: ...
