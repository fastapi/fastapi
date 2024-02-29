from typing import List, Mapping
import pytest
from fastapi import FastAPI, Query
from fastapi.types import FFQuery


def test_invalid_sequence():
    with pytest.raises(AssertionError):
        app = FastAPI()

        @app.get("/items/")
        def read_items(q: FFQuery[str, List[List[str]]] = Query(default=None)):
            pass  # pragma: no cover
