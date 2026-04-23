from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends, FastAPI

if TYPE_CHECKING:
    from sqlalchemy.orm import Session  # pragma: no cover

app = FastAPI()


def get_db() -> Session:
    return "fake_db"  # type: ignore[return-value]


@app.get("/")
def read_root(db=Depends(get_db)) -> dict:
    return {"db": str(db)}
