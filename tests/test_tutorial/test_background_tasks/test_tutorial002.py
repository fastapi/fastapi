import importlib
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial002_py39",
        pytest.param("tutorial002_py310", marks=needs_py310),
        "tutorial002_an_py39",
        pytest.param("tutorial002_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.background_tasks.{request.param}")

    client = TestClient(mod.app)
    return client


def test(client: TestClient):
    log = Path("log.txt")
    if log.is_file():
        os.remove(log)  # pragma: no cover
    response = client.post("/send-notification/foo@example.com?q=some-query")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Message sent"}
    with open("./log.txt") as f:
        assert "found query: some-query\nmessage to foo@example.com" in f.read()
