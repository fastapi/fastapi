from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root(potato: Potato) -> Potato: ...


@dataclass  # pragma: no cover
class Potato:
    color: str
    size: int
