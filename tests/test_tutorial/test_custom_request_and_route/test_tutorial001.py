import gzip
import json

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from docs_src.custom_request_and_route.tutorial001 import app


@app.get("/check-class")
async def check_gzip_request(request: Request):
    return {"request_class": type(request).__name__}


client = TestClient(app)


@pytest.mark.parametrize("compress", [True, False])
def test_gzip_request(compress):
    n = 1000
    headers = {}
    body = [1] * n
    data = json.dumps(body).encode()
    if compress:
        data = gzip.compress(data)
        headers["Content-Encoding"] = "gzip"
    headers["Content-Type"] = "application/json"
    response = client.post("/sum", data=data, headers=headers)
    assert response.json() == {"sum": n}


def test_request_class():
    response = client.get("/check-class")
    assert response.json() == {"request_class": "GzipRequest"}
