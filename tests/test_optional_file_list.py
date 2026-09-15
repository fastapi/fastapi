from fastapi import FastAPI, File
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/files")
async def upload_files(files: list[bytes] | None = File(None)):
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


def test_optional_bytes_list_empty_form_value():
    client = TestClient(app)
    response = client.post("/files", data={"files": ""})
    assert response.status_code == 200


def test_annotated_bytes_list_empty_form_value():
    from typing import Annotated

    app_annotated = FastAPI()

    @app_annotated.post("/files-annotated")
    async def upload_files_annotated(
        files: Annotated[list[bytes] | None, File()] = None,
    ):
        return {"files": files}

    client = TestClient(app_annotated)
    response = client.post("/files-annotated", data={"files": ""})
    assert response.status_code == 200


def test_required_bytes_list_empty_form_value():
    from typing import Annotated

    app_required = FastAPI()

    @app_required.post("/files-required")
    async def upload_files_required(
        files: Annotated[list[bytes], File()],
    ):
        return {"files": files}

    client = TestClient(app_required)
    response = client.post("/files-required", data={"files": ""})
    assert response.status_code == 200
