from typing import List, Optional

import pytest
from fastapi import FastAPI, File
from fastapi.testclient import TestClient

from ..utils import needs_pydanticv2

pytestmark = needs_pydanticv2


app = FastAPI()

# =====================================================================================
# File(alias=...)
# Current situation: Works, but schema is wrong
# Optional[List[bytes]] fails due to another issue (likely not related to aliases)

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
    assert detail[0]["msg"] == "Field required"
    assert "file_alias" in detail[0]["loc"]


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", files={"file_alias": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": 7}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_required_field_alias"]
    assert body_schema["properties"] == {
        "file_alias": {"title": "File Alias", "type": "string", "format": "binary"}
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file': {'type': 'string', 'format': 'binary', 'title': 'File'}} ==
    # {'file_alias': {'title': 'File Alias', 'type': 'string', 'format': 'binary'}}


# ------------------------------
# optional field


@app.post("/optional-field-alias", operation_id="optional_field_alias")
async def optional_field_alias(
    file: Optional[bytes] = File(None, alias="file_alias"),
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


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_field_alias"]
    assert body_schema["properties"] == {
        "file_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Alias",
        }
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert
    # {'file': {'anyOf': [{'type': 'string', 'format': 'binary'}, {'type': 'null'}], 'title': 'File'}} ==
    # {'file_alias': {'anyOf': [{'type': 'string', 'format': 'binary'}, {'type': 'null'}], 'title': 'File Alias'}}


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
    assert detail[0]["msg"] == "Field required"
    assert "files_alias" in detail[0]["loc"]


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": [8, 8]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
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
    # Currently fails due to issue with aliases:
    # AssertionError: assert
    # {'files': {'items': {'type': 'string', 'format': 'binary'}, 'type': 'array', 'title': 'Files'}} ==
    # {'files_alias': {'title': 'Files Alias', 'type': 'array', 'items': {'type': 'string', 'format': 'binary'}}}


# ------------------------------
# optional list field


@app.post("/optional-list-field-alias", operation_id="optional_list_field_alias")
async def optional_list_field_alias(
    files: Optional[List[bytes]] = File(None, alias="files_alias"),
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


@pytest.mark.xfail(
    reason="Optional[List[bytes]] File type causes TypeError in FastAPI",
    raises=TypeError,
    strict=False,
)
def test_optional_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    # Currently fails due to some issue (likely unrelated to aliases) with:
    # TypeError: issubclass() arg 1 must be a class

    assert resp.json() == {"file_sizes": [8, 8]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_list_field_alias"]
    assert body_schema["properties"] == {
        "files_alias": {
            "anyOf": [
                {"items": {"type": "string", "format": "binary"}, "type": "array"},
                {"type": "null"},
            ],
            "title": "Files Alias",
        },
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert
    # {'files': {'anyOf': [{'items': {'type': 'string', 'format': 'binary'}, 'type': 'array'}, {'type': 'null'}], 'title': 'Files'}} ==
    # {'files_alias': {'anyOf': [{'items': {'type': 'string', 'format': 'binary'}, 'type': 'array'}, {'type': 'null'}], 'title': 'Files Alias'}}


# =====================================================================================
# File(validation_alias=...)
# Current situation: schema is correct, but doesn't work (parameter name is used)
# Optional[List[bytes]] fails due to another issue (likely not related to aliases)


# ------------------------------
# required field


@app.post(
    "/required-field-validation-alias", operation_id="required_field_validation_alias"
)
async def required_field_validation_alias(
    file: bytes = File(validation_alias="file_val_alias"),
):
    return {"file_size": len(file)}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-validation-alias", files={"file": b"content"})
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias", files={"file_val_alias": b"content"}
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"file_size": 7}


def test_required_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_required_field_validation_alias"
    ]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "title": "File Val Alias",
            "type": "string",
            "format": "binary",
        },
    }


# ------------------------------
# optional field


@app.post(
    "/optional-field-validation-alias", operation_id="optional_field_validation_alias"
)
async def optional_field_validation_alias(
    file: Optional[bytes] = File(None, validation_alias="file_val_alias"),
):
    if file is None:
        return {"file_size": None}
    return {"file_size": len(file)}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-validation-alias", files={"file": b"content"})
    assert resp.json() == {"file_size": None}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file_size': 7} == {'file_size': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias", files={"file_val_alias": b"content"}
    )
    assert resp.json() == {"file_size": 7}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file_size': None} == {'file_size': 7}


def test_optional_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_field_validation_alias"
    ]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Val Alias",
        },
    }


# ------------------------------
# list field


@app.post("/list-field-validation-alias", operation_id="list_field_validation_alias")
async def list_field_validation_alias(
    files: List[bytes] = File(validation_alias="files_val_alias"),
):
    return {"file_sizes": [len(file) for file in files]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_validation_alias"]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "items": {"type": "string", "format": "binary"},
            "title": "Files Val Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


@app.post(
    "/optional-list-field-validation-alias",
    operation_id="optional_list_field_validation_alias",
)
async def optional_list_field_validation_alias(
    files: Optional[List[bytes]] = File(None, validation_alias="files_val_alias"),
):
    if files is None:
        return {"file_sizes": None}
    return {"file_sizes": [len(file) for file in files]}


@pytest.mark.xfail(
    reason="Optional[List[bytes]] File type causes TypeError in FastAPI",
    raises=TypeError,
    strict=False,
)
def test_optional_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    # Currently fails due to some issue (likely unrelated to aliases) with:
    # TypeError: issubclass() arg 1 must be a class

    assert resp.json() == {"file_sizes": None}
    # Will likely fail due to issue with aliases with:
    # AssertionError: assert {'file_sizes': [8, 8]} == {'file_sizes': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.json() == {"file_sizes": [8, 8]}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file_sizes': None} == {'file_sizes': [8, 8]}


def test_optional_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_list_field_validation_alias"
    ]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "anyOf": [
                {"items": {"type": "string", "format": "binary"}, "type": "array"},
                {"type": "null"},
            ],
            "title": "Files Val Alias",
        },
    }


# =====================================================================================
# File(alias=..., validation_alias=...)
# Current situation: Schema is correct (validation_alias), but doesn't work (alias is used)
# Optional[List[bytes]] fails due to another issue (likely not related to aliases)

# ------------------------------
# required field


@app.post(
    "/required-field-alias-and-validation-alias",
    operation_id="required_field_alias_and_validation_alias",
)
async def required_field_alias_and_validation_alias(
    file: bytes = File(alias="file_alias", validation_alias="file_val_alias"),
):
    return {"file_size": len(file)}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", files={"file": b"content"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]
    # Currently fails due to issue with aliases:
    # AssertionError: assert 'file_val_alias' in ['body', 'file_alias']


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", files={"file_alias": b"content"}
    )
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias",
        files={"file_val_alias": b"content"},
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"file_size": 7}


def test_required_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_required_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "title": "File Val Alias",
            "type": "string",
            "format": "binary",
        }
    }


# ------------------------------
# optional field


@app.post(
    "/optional-field-alias-and-validation-alias",
    operation_id="optional_field_alias_and_validation_alias",
)
async def optional_field_alias_and_validation_alias(
    file: Optional[bytes] = File(
        None, alias="file_alias", validation_alias="file_val_alias"
    ),
):
    if file is None:
        return {"file_size": None}
    return {"file_size": len(file)}


def test_optional_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", files={"file": b"content"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", files={"file_alias": b"content"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file_size': 7} == {'file_size': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias",
        files={"file_val_alias": b"content"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": 7}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file_size': None} == {'file_size': 7}


def test_optional_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Val Alias",
        }
    }


# ------------------------------
# list field


@app.post(
    "/list-field-alias-and-validation-alias",
    operation_id="list_field_alias_and_validation_alias",
)
async def list_field_alias_and_validation_alias(
    files: List[bytes] = File(alias="files_alias", validation_alias="files_val_alias"),
):
    return {"file_sizes": [len(file) for file in files]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_val_alias" in detail[0]["loc"]
    # Currently fails due to issue with aliases:
    # AssertionError: assert 'files_val_alias' in ['body', 'files_alias']


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_list_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "items": {"type": "string", "format": "binary"},
            "title": "Files Val Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


@app.post(
    "/optional-list-field-alias-and-validation-alias",
    operation_id="optional_list_field_alias_and_validation_alias",
)
async def optional_list_field_alias_and_validation_alias(
    files: Optional[List[bytes]] = File(
        None, alias="files_alias", validation_alias="files_val_alias"
    ),
):
    if files is None:
        return {"file_sizes": None}
    return {"file_sizes": [len(file) for file in files]}


def test_optional_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}


@pytest.mark.xfail(
    reason="Optional[List[bytes]] File type causes TypeError in FastAPI",
    raises=TypeError,
    strict=False,
)
def test_optional_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    # Currently fails due to some issue (likely unrelated to aliases) with:
    # TypeError: issubclass() arg 1 must be a class

    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}
    # Will likely fail due to issue with aliases:
    # AssertionError: assert {'file_sizes': [8, 8]} == {'file_sizes': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": [8, 8]}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'file_sizes': None} == {'file_sizes': [8, 8]}


def test_optional_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_list_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "anyOf": [
                {"items": {"type": "string", "format": "binary"}, "type": "array"},
                {"type": "null"},
            ],
            "title": "Files Val Alias",
        },
    }


# =====================================================================================
# File(alias=..., validation_alias=...)  # alias == validation_alias
# The only working solution (current workaround)
# TODO: remove when issue with File field aliases is fixed


@app.post("/workaround", operation_id="workaround")
async def workaround(
    file: bytes = File(alias="file_alias", validation_alias="file_alias"),
):
    return {"file_size": len(file)}


def test_workaround_by_name():
    client = TestClient(app)
    resp = client.post("/workaround", files={"file": b"content"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_alias" in detail[0]["loc"]


def test_workaround_by_alias():
    client = TestClient(app)
    resp = client.post("/workaround", files={"file_alias": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": 7}


def test_workaround_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_workaround"]
    assert body_schema["properties"] == {
        "file_alias": {"title": "File Alias", "type": "string", "format": "binary"}
    }
