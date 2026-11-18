import pytest
from fastapi.testclient import TestClient

from docs_src.request_body_limits.tutorial002 import app

client = TestClient(app)


@pytest.mark.parametrize("multipart", [False, True])
def test_form_limits(multipart):
    value = "x" * (1024 * 1024 + 1)

    def submit(path: str, fields: dict[str, str]):
        if multipart:
            return client.post(path, files={k: (None, v) for k, v in fields.items()})
        return client.post(path, data=fields)

    assert submit("/notes", {"text": "ok"}).json() == {"size": 2}
    assert submit("/notes", {"text": value}).status_code == 400
    assert submit("/documents", {"text": value}).json() == {"size": len(value)}
    fields = {"text": "ok", **{str(i): "v" for i in range(4)}}
    assert submit("/documents", fields).json() == {"size": 2}
    assert submit("/documents", {**fields, "extra": "v"}).status_code == 400
