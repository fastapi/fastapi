import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .utils import skip_py38


@skip_py38
@pytest.mark.parametrize(
    "test_type,expect",
    [
        (list[int], [1, 2, 3]),
        (dict[str, list[int]], {"a": [1, 2, 3], "b": [4, 5, 6]}),
        (set[int], {1, 2, 3}),
        (tuple[int], (1, 2, 3)),
    ],
)
def test_typing(test_type, expect):
    app = FastAPI()

    @app.get("/", response_model=test_type)
    def get_endpoint():
        return expect

    res = TestClient(app).get("/")
    assert res.status_code == 200
    assert res.json() == expect
