from typing import Optional

from fastapi import FastAPI, File
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/files")
async def upload_files(files: Optional[list[bytes]] = File(None)):
    if files is None:
        return {"files_count": 0}
    return {"files_count": len(files), "sizes": [len(f) for f in files]}


def test_optional_bytes_list():
    client = TestClient(app)
    response = client.post(
        "/files",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert response.status_code == 200
    assert response.json() == {"files_count": 2, "sizes": [8, 8]}


def test_optional_bytes_list_no_files():
    client = TestClient(app)
    response = client.post("/files")
    assert response.status_code == 200
    assert response.json() == {"files_count": 0}
