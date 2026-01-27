
import pytest
from fastapi import FastAPI, Query


def test_invalid_sequence():
    with pytest.raises(AssertionError):
        app = FastAPI()

        @app.get("/items/")
        def read_items(q: dict[str, list[list[str]]] = Query(default=None)):
            pass  # pragma: no cover
