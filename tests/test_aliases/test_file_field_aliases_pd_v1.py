from typing import List, Optional

from fastapi import FastAPI, File
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient

from ..utils import needs_pydanticv1

pytestmark = needs_pydanticv1

app = FastAPI()

# =====================================================================================
# File(alias=...)
# Current situation: Works

# ------------------------------
# required field


@app.post("/required-field-alias", operation_id="required_field_alias")
async def required_field_alias(file: bytes = File(alias="file_alias")):
    return {"file_size": len(file)}


def test_required_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias", files={"file": b"content"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "file_alias" in detail[0]["loc"]


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", files={"file_alias": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": 7}


def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_required_field_alias"]
    assert body_schema["properties"] == {
        "file_alias": {"title": "File Alias", "type": "string", "format": "binary"}
    }


# ------------------------------
# optional field

if not PYDANTIC_V2:

    @app.post("/optional-field-alias", operation_id="optional_field_alias")
    async def optional_field_alias(
        file: Optional[bytes] = File(None, alias="file_alias", nullable=True),
    ):
        if file is None:
            return {"file_size": None}
        return {"file_size": len(file)}


def test_optional_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", files={"file": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


def test_optional_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", files={"file_alias": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": 7}


def test_optional_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_field_alias"]
    assert body_schema["properties"] == {
        "file_alias": {
            "type": "string",
            "nullable": True,
            "format": "binary",
            "title": "File Alias",
        }
    }


# ------------------------------
# list field


@app.post("/list-field-alias", operation_id="list_field_alias")
async def list_field_alias(files: List[bytes] = File(alias="files_alias")):
    return {"file_sizes": [len(file) for file in files]}


def test_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias", files=[("files", b"content1"), ("files", b"content2")]
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "files_alias" in detail[0]["loc"]


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_alias"]
    assert body_schema["properties"] == {
        "files_alias": {
            "title": "Files Alias",
            "type": "array",
            "items": {"type": "string", "format": "binary"},
        }
    }


# ------------------------------
# optional list field


if not PYDANTIC_V2:

    @app.post("/optional-list-field-alias", operation_id="optional_list_field_alias")
    async def optional_list_field_alias(
        files: Optional[List[bytes]] = File(None, alias="files_alias", nullable=True),
    ):
        if files is None:
            return {"file_sizes": None}
        return {"file_sizes": [len(file) for file in files]}


def test_optional_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}


def test_optional_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.json() == {"file_sizes": [8, 8]}


def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_list_field_alias"]
    assert body_schema["properties"] == {
        "files_alias": {
            "items": {"format": "binary", "type": "string"},
            "nullable": True,
            "title": "Files Alias",
            "type": "array",
        },
    }
