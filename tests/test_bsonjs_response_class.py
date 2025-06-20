import json
import sys

import pytest


@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires minimum python3.9 or higher"
)
def test_bsonjs_serialized_data():
    import bsonjs
    from fastapi import FastAPI
    from fastapi.responses import BSONJSResponse
    from fastapi.testclient import TestClient

    app = FastAPI(default_response_class=BSONJSResponse)

    @app.get("/bsonjs_keys")
    def get_bsonjs_serialized_data():
        return {"key": "Hello World"}

    client = TestClient(app)
    with client:
        response = client.get("/bsonjs_keys")

        assert response.content == bsonjs.loads(
            json.dumps({"key": "Hello World", 1: 1})
        )
